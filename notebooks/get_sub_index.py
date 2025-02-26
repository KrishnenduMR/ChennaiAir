
from decimal import Decimal

# AQI Sub-index Calculation Functions
def get_PM25_subindex(x):
    x = Decimal(x)
    if x <= 30: return round(x * 50 / 30)
    elif x <= 60: return round(50 + (x - 30) * 50 / 30)
    elif x <= 90: return round(100 + (x - 60) * 100 / 30)
    elif x <= 120: return round(200 + (x - 90) * 100 / 30)
    elif x <= 250: return round(300 + (x - 120) * 100 / 130)
    else: return round(400 + (x - 250) * 100 / 130)

def get_PM10_subindex(x):
    x = Decimal(x)
    if x <= 50: return round(x * 50 / 50)
    elif x <= 100: return round(50 + (x - 50) * 50 / 50)
    elif x <= 250: return round(100 + (x - 100) * 100 / 150)
    elif x <= 350: return round(200 + (x - 250) * 100 / 100)
    elif x <= 430: return round(300 + (x - 350) * 100 / 80)
    else: return round(400 + (x - 430) * 100 / 80)

def get_SO2_subindex(x):
    x = Decimal(x)
    if x <= 40: return round(x * 50 / 40)
    elif x <= 80: return round(50 + (x - 40) * 50 / 40)
    elif x <= 380: return round(100 + (x - 80) * 100 / 300)
    elif x <= 800: return round(200 + (x - 380) * 100 / 420)
    elif x <= 1600: return round(300 + (x - 800) * 100 / 800)
    else: return round(400 + (x - 1600) * 100 / 800)

def get_NOx_subindex(x):
    x = Decimal(x)
    if x <= 40: return round(x * 50 / 40)
    elif x <= 80: return round(50 + (x - 40) * 50 / 40)
    elif x <= 180: return round(100 + (x - 80) * 100 / 100)
    elif x <= 280: return round(200 + (x - 180) * 100 / 100)
    elif x <= 400: return round(300 + (x - 280) * 100 / 120)
    else: return round(400 + (x - 400) * 100 / 120)

def get_CO_subindex(x):
    x = Decimal(x) / 1000  # Convert µg/m³ to mg/m³
    if x <= 1: return round(x * 50 / 1)
    elif x <= 2: return round(50 + (x - 1) * 50 / 1)
    elif x <= 10: return round(100 + (x - 2) * 100 / 8)
    elif x <= 17: return round(200 + (x - 10) * 100 / 7)
    elif x <= 34: return round(300 + (x - 17) * 100 / 17)
    else: return round(400 + (x - 34) * 100 / 17)

def get_O3_subindex(x):
    x = Decimal(x)
    if x <= 50: return round(x * 50 / 50)
    elif x <= 100: return round(50 + (x - 50) * 50 / 50)
    elif x <= 168: return round(100 + (x - 100) * 100 / 68)
    elif x <= 208: return round(200 + (x - 168) * 100 / 40)
    elif x <= 748: return round(300 + (x - 208) * 100 / 540)
    else: return round(400 + (x - 748) * 100 / 540)
