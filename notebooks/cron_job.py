import requests
import csv
import logging
import os
import logging.handlers
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_percentage_error


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# 🔹 Station Information
Velachery = "Velachery Res. Area"
Velachery_OUTPUT = os.path.join(REPO_ROOT, "data/cron_job_data/velachery_cron_output.csv")

alandur = "Alandur Bus Depot"
alandur_OUTPUT = os.path.join(REPO_ROOT, "static/data/alandur_cron_output.csv")
alandur_DAILY_AQI = os.path.join(REPO_ROOT, "static/data/alandur_daily.csv")

Manali = "Manali Village"
Manali_OUTPUT = os.path.join(REPO_ROOT, "data/cron_job_data/manali_cron_output.csv")

stations = [(Velachery, Velachery_OUTPUT), (alandur, alandur_OUTPUT), (Manali, Manali_OUTPUT)]
FORECAST_alandur_DAILY_AQI = os.path.join(REPO_ROOT, "static/data/forecast_alandur_daily_aqi.csv")

ORDER, SEASONAL_ORDER = (1, 0, 1), (1, 0, 1, 7)

# 🔹 API Token
def get_api_token():
    return '66f8e6976ba9c150deb7dd9ae09171437ab1a304'

# 🔹 Logger Setup
def setLogger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    os.makedirs("logs", exist_ok=True)
    logger_file_handler = logging.handlers.RotatingFileHandler(
        f"logs/{datetime.now().strftime('%d-%m-%Y')}.log",
        maxBytes=1024 * 1024,
        backupCount=1,
        encoding="utf8",
    )
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger_file_handler.setFormatter(formatter)
    logger.addHandler(logger_file_handler)
    return logger

# 🔹 Fetch AQI Data & Save to CSV
def setData(station, output_file, logger, TOKEN):
    try:
        url = "https://api.waqi.info/search/?token=" + TOKEN + "&keyword=" + station
        response = requests.get(url)

        if response.status_code == 200:
            res = response.json()
            if not res["data"]:
                logger.info(f"No data found for {station}")
                return
            
            station_data = res["data"][0]
            result = [station_data['aqi'], station_data['station']['name'], pd.to_datetime(station_data['time']['stime'])]

            # Ensure AQI is a number
            try:
                int(result[0])
            except ValueError:
                logger.info(f"Invalid AQI value for {station}")
                return
            
            # Prevent duplicate timestamps
            new_timestamp = result[2]
            if os.path.exists(output_file):
                existing_data = pd.read_csv(output_file)
                if new_timestamp in existing_data['datetime'].values:
                    logger.info(f"Timestamp {new_timestamp} already exists for {station}")
                    return

            # Append new data
            with open(output_file, 'a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(result)

            logger.info(f"Data written for {station}: {result}")

        else:
            logger.info(f"API Error for {station}: {response.status_code} - {response.text}")

    except Exception as e:
        logger.exception(f"Exception in setData for {station}: {e}")

# 🔹 Convert Hourly AQI to Daily AQI
def writeData(station_hourly_aqi, station_daily_aqi):
    try:
        # Read hourly data
        df_api = pd.read_csv(station_hourly_aqi)
        df_api['datetime'] = pd.to_datetime(df_api['datetime'])
        df_api.set_index('datetime', inplace=True)
        df_daily = df_api['AQI'].resample('D').mean()

        # Read existing daily data
        if os.path.exists(station_daily_aqi):
            df_existing = pd.read_csv(station_daily_aqi, parse_dates=['Datetime'])
            df_existing.set_index('Datetime', inplace=True)
        else:
            df_existing = pd.DataFrame(columns=['AQI'])

        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        yesterday_ts = pd.Timestamp(yesterday)  # ✅ Convert to Timestamp

        if yesterday_ts not in df_existing.index:
            if yesterday_ts in df_daily.index:  # ✅ Ensure yesterday's data exists
                new_entry = pd.DataFrame({'AQI': [df_daily.loc[yesterday_ts]]}, index=[yesterday_ts])
                df_existing = pd.concat([df_existing, new_entry])

                df_existing.to_csv(station_daily_aqi, index=True, index_label="Datetime")
                print(f"Daily AQI written for {yesterday}")
                logger.info(f"Daily AQI written for {yesterday}")
            else:
                print(f"No AQI data available for {yesterday}")
                logger.info(f"No AQI data available for {yesterday}")
        else:
            print(f"Data for {yesterday} already exists")
            logger.info(f"Data for {yesterday} already exists")

    except Exception as e:
        logger.exception(f"Exception in writeData: {e}")

# 🔹 Retrain SARIMA Model & Forecast
def retrain_model(order, seasonal_order, station_daily_aqi):
    try:
        df = pd.read_csv(station_daily_aqi)

        # Debugging step
        print("Columns in CSV:", df.columns)
        
        # Ensure 'Datetime' column exists
        df.columns = df.columns.str.strip()  # Remove unwanted spaces
        if 'Datetime' not in df.columns:
            logger.error(f"Column 'Datetime' not found in {station_daily_aqi}. Available columns: {df.columns}")
            return
        
        df['Datetime'] = pd.to_datetime(df['Datetime'])
        df.set_index('Datetime', inplace=True)
        df.ffill(inplace=True)  # Fill missing values

        # Split data
        train_end = df.index[-1] - timedelta(days=5)
        train_data, test_data = df.loc[:train_end, 'AQI'], df.loc[train_end + timedelta(days=1):, 'AQI']

        # Train SARIMA Model
        model = SARIMAX(train_data, order=order, seasonal_order=seasonal_order)
        model_fit = model.fit()
        predictions = model_fit.forecast(len(test_data))
        MAPE = mean_absolute_percentage_error(test_data, predictions) * 100

        logger.info(f"Model retrained, MAPE: {MAPE}%")

        if MAPE <= 30:
            full_model = SARIMAX(df['AQI'], order=order, seasonal_order=seasonal_order)
            full_model_fit = full_model.fit()
            future_forecast = full_model_fit.forecast(5)

            # ✅ Fix: Proper date index for forecast
            future_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=5, freq='D')

            # ✅ Round AQI values
            forecast_df = pd.DataFrame({
                'Datetime': future_dates, 
                'AQI': np.round(future_forecast.values, 2)
            })

            forecast_df.to_csv(FORECAST_alandur_DAILY_AQI, index=False)
            logger.info(f"Forecast written to {FORECAST_alandur_DAILY_AQI}")

    except Exception as e:
        logger.exception(f"Exception in retrain_model: {e}")

# 🔹 Main Execution
if __name__ == "__main__":
    logger = setLogger()
    TOKEN = get_api_token()

    for station, station_location in stations:
        setData(station, station_location, logger, TOKEN)

    if datetime.utcnow().hour == 20:
        writeData(alandur_OUTPUT, alandur_DAILY_AQI)
        retrain_model(ORDER, SEASONAL_ORDER, alandur_DAILY_AQI)
