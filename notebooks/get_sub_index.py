from decimal import Decimal

def get_PM25_subindex(x):
    x = Decimal(x)
    if x <= 30:
        return x * Decimal(50) / 30
    elif x <= 60:
        return Decimal(50) + (x - 30) * Decimal(50) / 30
    elif x <= 90:
        return Decimal(100) + (x - 60) * Decimal(100) / 30
    elif x <= 120:
        return Decimal(200) + (x - 90) * Decimal(100) / 30
    elif x <= 250:
        return Decimal(300) + (x - 120) * Decimal(100) / 130
    else:
        return Decimal(400) + (x - 250) * Decimal(100) / 130

def get_PM10_subindex(x):
    x = Decimal(x)
    if x <= 50:
        return x * Decimal(50) / 50
    elif x <= 100:
        return Decimal(50) + (x - 50) * Decimal(50) / 50
    elif x <= 250:
        return Decimal(100) + (x - 100) * Decimal(100) / 150
    elif x <= 350:
        return Decimal(200) + (x - 250) * Decimal(100) / 100
    elif x <= 430:
        return Decimal(300) + (x - 350) * Decimal(100) / 80
    else:
        return Decimal(400) + (x - 430) * Decimal(100) / 80

def get_SO2_subindex(x):
    x = Decimal(x)
    if x <= 40:
        return x * Decimal(50) / 40
    elif x <= 80:
        return Decimal(50) + (x - 40) * Decimal(50) / 40
    elif x <= 380:
        return Decimal(100) + (x - 80) * Decimal(100) / 300
    elif x <= 800:
        return Decimal(200) + (x - 380) * Decimal(100) / 420
    elif x <= 1600:
        return Decimal(300) + (x - 800) * Decimal(100) / 800
    else:
        return Decimal(400) + (x - 1600) * Decimal(100) / 800

def get_NOx_subindex(x):
    x = Decimal(x)
    if x <= 40:
        return x * Decimal(50) / 40
    elif x <= 80:
        return Decimal(50) + (x - 40) * Decimal(50) / 40
    elif x <= 180:
        return Decimal(100) + (x - 80) * Decimal(100) / 100
    elif x <= 280:
        return Decimal(200) + (x - 180) * Decimal(100) / 100
    elif x <= 400:
        return Decimal(300) + (x - 280) * Decimal(100) / 120
    else:
        return Decimal(400) + (x - 400) * Decimal(100) / 120

def get_CO_subindex(x):
    x = Decimal(x)
    if x <= 1:
        return x * Decimal(50) / 1
    elif x <= 2:
        return Decimal(50) + (x - 1) * Decimal(50) / 1
    elif x <= 10:
        return Decimal(100) + (x - 2) * Decimal(100) / 8
    elif x <= 17:
        return Decimal(200) + (x - 10) * Decimal(100) / 7
    elif x <= 34:
        return Decimal(300) + (x - 17) * Decimal(100) / 17
    else:
        return Decimal(400) + (x - 34) * Decimal(100) / 17

def get_O3_subindex(x):
    x = Decimal(x)
    if x <= 50:
        return x * Decimal(50) / 50
    elif x <= 100:
        return Decimal(50) + (x - 50) * Decimal(50) / 50
    elif x <= 168:
        return Decimal(100) + (x - 100) * Decimal(100) / 68
    elif x <= 208:
        return Decimal(200) + (x - 168) * Decimal(100) / 40
    elif x <= 748:
        return Decimal(300) + (x - 208) * Decimal(100) / 540
    else:
        return Decimal(400) + (x - 748) * Decimal(100) / 540

def calculate_aqi(row):
    """ Calculate AQI using the worst sub-index method """
    sub_indices = {}

    if "PM2.5 (µg/m³)" in row and row["PM2.5 (µg/m³)"] is not None:
        sub_indices["PM2.5"] = get_PM25_subindex(row["PM2.5 (µg/m³)"])
    
    if "PM10 (µg/m³)" in row and row["PM10 (µg/m³)"] is not None:
        sub_indices["PM10"] = get_PM10_subindex(row["PM10 (µg/m³)"])

    if "SO2 (µg/m³)" in row and row["SO2 (µg/m³)"] is not None:
        sub_indices["SO2"] = get_SO2_subindex(row["SO2 (µg/m³)"])

    if "NOx (µg/m³)" in row and row["NOx (µg/m³)"] is not None:
        sub_indices["NOx"] = get_NOx_subindex(row["NOx (µg/m³)"])

    if "CO (µg/m³)" in row and row["CO (µg/m³)"] is not None:
        sub_indices["CO"] = get_CO_subindex(row["CO (µg/m³)"] / 1000)  # Convert µg/m³ to mg/m³

    if "Ozone (µg/m³)" in row and row["Ozone (µg/m³)"] is not None:
        sub_indices["Ozone"] = get_O3_subindex(row["Ozone (µg/m³)"])

    # Check if enough data is available for AQI calculation
    if len(sub_indices) < 3 or not any(pollutant in sub_indices for pollutant in ["PM2.5", "PM10"]):
        return None  # Insufficient data for AQI

    # AQI is the highest sub-index
    return max(sub_indices.values())

# Example usage:
sample_data = {
    "PM2.5 (µg/m³)": 21.2,
    "PM10 (µg/m³)": 219,
    "NOx (µg/m³)": 4.236,
    "SO2 (µg/m³)": 4.226,
    "CO (µg/m³)": 18.245,
    "Ozone (µg/m³)": 35.04,
}

aqi_value = calculate_aqi(sample_data)
print(f"AQI: {aqi_value}")
