import requests
import csv
from datetime import datetime, timedelta
import logging
import os
import logging.handlers

# Data analysis
import pandas as pd
import numpy as np

# Time Series
from datetime import datetime, timedelta
from statsmodels.tsa.arima.model import ARIMA 
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Metrics for model evaluation
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error

# 🔹 Station Information
Velachery = "Velachery Res. Area"
Velachery_OUTPUT = "../data/cron_job_data/velachery_cron_output.csv"

alandur = "Alandur Bus Depot"
alandur_OUTPUT = "../static/data/alandur_cron_output.csv"
alandur_DAILY_AQI = "../static/data/alandur_daily.csv"

Manali = "Manali Village"
Manali_OUTPUT = "../data/cron_job_data/manali_cron_output.csv"

stations = [(Velachery, Velachery_OUTPUT), (alandur, alandur_OUTPUT), (Manali, Manali_OUTPUT)]
FORECAST_alandur_DAILY_AQI = "../static/data/forecast_alandur_daily_aqi.csv"

ORDER, SEASONAL_ORDER = (0, 3, 15),  (0, 0, 0, 7)

# 🔹 API Token
def get_api_token():
    return '66f8e6976ba9c150deb7dd9ae09171437ab1a304'

# 🔹 Logger Setup
def setLogger():
    '''
    This function sets the logger to the logs directory.
    Every day, a new file gets created.
    '''
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
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
            result = []
            if station.lower() in (res["data"][0]['station']['name']).lower():
                result.append(res["data"][0]['aqi'])
                result.append(res["data"][0]['station']['name'])
                result.append(pd.to_datetime(res["data"][0]['time']['stime']))

            # Ensure AQI is a number
            try:
                int(result[0])
            except Exception as exception:
                # logger.info(f"setData function - AQI is not an integer. Exception {type(exception).__name__} has occured for station=> {station}")
                print(f"setData function - AQI is not an integer. Exception {type(exception).__name__} has occured for station=> {station}")
                return
            
            # Prevent duplicate timestamps
            new_timestamp = (res["data"][0]['time']['stime'])
            csv_file_path = output_file

            # Check if the new timestamp is already present
            with open(csv_file_path, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                # Assuming the timestamp is in the 3rd column
                existing_timestamps = [row[2] for row in csv_reader]

            if new_timestamp not in existing_timestamps:
                with open(csv_file_path, 'a', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(result)
                logger.info(f"station=> {station}, result => {result}")
                print(f"station=> {station}, result => {result}")
                print(f'The hourly data has been written to {csv_file_path} with Timestamp: {new_timestamp}')
                logger.info(f'The hourly data has been written to {csv_file_path} with Timestamp: {new_timestamp}')
            else:
                print(f'Timestamp {new_timestamp} already present in {csv_file_path}, not appending.')
                logger.info(f'Timestamp {new_timestamp} already present in {csv_file_path}, not appending.')
        else:
            print(f"setData function - Error: {response.status_code} - {response.text}")
            logger.info(f"setData function - Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"setData function - Exception {type(e).__name__} has occured for station=> {station}")
        

# 🔹 Retrain SARIMA Model & Forecast
def retrain_model(order, seasonal_order, station_daily_aqi):
    '''
    This function is called daily once at 1 AM. 
    It takes into account today's AQI and re-trains the model.
    We check the model's performance by splitting data into train & test data, then train the model and calculate MAPE.
    We consider entire data (no splitting into train & test) and re-train our model & forecast for the next 5 days.
    '''

    # Read the data & clean it.
    daily_aqi = pd.read_csv(station_daily_aqi)
    daily_aqi['Datetime'] = pd.to_datetime(daily_aqi['Datetime'])
    daily_aqi.set_index('Datetime', inplace=True)
    daily_aqi.index = pd.to_datetime(daily_aqi.index)
    daily_aqi.ffill(inplace=True)

    df = daily_aqi
    
    # Split into train & test
    train_end = df.index[-1] - timedelta(days=5)  # Except last 5 days
    print(f"train_end=> {train_end}")
    logger.info(f'Re-training the model & train_end is {train_end}')
    
    train_data = df.loc[:train_end, 'AQI']
    test_data = df.loc[train_end + timedelta(days=1):, 'AQI']

    # Train the model
    model = SARIMAX(train_data, order=order, seasonal_order=seasonal_order)
    model_fit = model.fit()

    predictions = model_fit.forecast(len(test_data))
    predictions = pd.Series(predictions, index=test_data.index)
    
    # Calculate MAPE
    MAPE = round(mean_absolute_percentage_error(test_data, predictions) * 100, 2)  # Round it off to two decimal points
    print(f"\n\nMAPE=> {MAPE}")
    logger.info(f'Retrained the model & MAPE is {MAPE}%')

    # Calculate MAE
    MAE = mean_absolute_error(test_data, predictions)
    print(f"\n\nMAE=> {MAE}")
    logger.info(f'Retrained the model & MAE is {MAE}')

    train_data = df.loc[:, 'AQI']
    model = SARIMAX(train_data, order=order, seasonal_order=seasonal_order)
    model_fit = model.fit()
    predictions = model_fit.forecast(len(test_data))
    predictions = pd.Series(predictions)
    print(f"\n\nForecast=> \n{predictions}")
    logger.info(f"Forecast=> \n{predictions}")

    # Save the forecast
    try:
        containsNaN = predictions.isna().sum()
        if containsNaN == 0:
            with open(FORECAST_alandur_DAILY_AQI, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['Datetime', 'AQI'])
                for i in range(5):
                    csv_writer.writerow([predictions.index[i].date(), round(predictions.values[i])])
                # Log the predictions to view in future.
                print(f'The forecast data has been written to {FORECAST_alandur_DAILY_AQI}')
                logger.info(f'The forecast data has been written to {FORECAST_alandur_DAILY_AQI}')
        else:
            print(f'retrain_model function - The forecast data has NaNs.')
            logger.info(f'retrain_model function - The forecast data has NaNs.')
    
    except Exception as e:
        print(f"retrain_model function - Model is not retrained. Please look into the issue - Exception {type(e).__name__} has occured.")
        logger.info(f"retrain_model function - Model is not retrained. Please look into the issue - Exception {type(e).__name__} has occured.")


# 🔹 Convert Hourly AQI to Daily AQI
def writeData(station_hourly_aqi, station_daily_aqi):
    """
    Updates the daily AQI by taking the mean of today's AQI (not yesterday's).
    Ensures there are no duplicate rows for today.
    This function is called at 2 AM, 11 AM, and 5 PM.
    """

    # Load hourly AQI data
    df_hourly = pd.read_csv(station_hourly_aqi, parse_dates=['datetime'])
    df_hourly.columns = ['AQI', 'Station', 'Datetime']
    df_hourly.set_index('Datetime', inplace=True)

    # Compute today's mean AQI
    today = datetime.now().date()
    today_mean = df_hourly[df_hourly.index.date == today]['AQI'].mean()

    if not np.isnan(today_mean):
        # Load existing daily AQI data
        if os.path.exists(station_daily_aqi):
            df_daily = pd.read_csv(station_daily_aqi, parse_dates=['Datetime'])
            df_daily['Datetime'] = df_daily['Datetime'].dt.date  # Convert to date only

            # Remove today's existing entry if present
            df_daily = df_daily[df_daily['Datetime'] != today]
        else:
            df_daily = pd.DataFrame(columns=['Datetime', 'AQI'])

        # Append today's AQI
        df_new = pd.DataFrame([[today, round(today_mean, 1)]], columns=['Datetime', 'AQI'])
        df_daily = pd.concat([df_daily, df_new], ignore_index=True)

        # Save updated data
        df_daily.to_csv(station_daily_aqi, index=False)

        print(f"Updated daily AQI: {today} => {round(today_mean, 1)}")
        logger.info(f"Updated daily AQI: {today} => {round(today_mean, 1)}")
    else:
        print("writeData: No data available to compute today's AQI.")
        logger.warning("writeData: No data available to compute today's AQI.")

# 🔹 Main Execution
if __name__ == "__main__":
    logger = setLogger()
    TOKEN = get_api_token()

    for station, station_location in stations:
        setData(station, station_location, logger, TOKEN)

    # Log current time
    print(f"datetime.now() => {datetime.now()}")

    # Read daily AQI data
    daily_AQI = pd.read_csv(alandur_DAILY_AQI, parse_dates=["Datetime"])
    daily_AQI['Datetime'] = pd.to_datetime(daily_AQI['Datetime'])
    daily_AQI.set_index('Datetime', inplace=True)

    # Call writeData every hour
    print("Calling writeData function. Time =>", datetime.now().hour)
    logger.info("Calling writeData function.")
    writeData(alandur_OUTPUT, alandur_DAILY_AQI)

    # Retrain only at 5 AM, 1 PM, and 10 PM
    if datetime.now().hour in [5, 13, 22]:
        print("Calling retrain_model function. Time =>", datetime.now().hour)
        logger.info("Calling retrain_model function.")
        retrain_model(ORDER, SEASONAL_ORDER, alandur_DAILY_AQI)
