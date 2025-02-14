from decimal import Decimal

def get_PM25_subindex(x):
    x = Decimal(x)
    if x <= 60:
        return x * Decimal(50) / 60
    elif x <= 120:
        return Decimal(50) + (x - 60) * Decimal(50) / 60
    elif x <= 180:
        return Decimal(100) + (x - 120) * Decimal(100) / 60
    elif x <= 240:
        return Decimal(200) + (x - 180) * Decimal(100) / 60
    elif x <= 500:
        return Decimal(300) + (x - 240) * Decimal(100) / 260
    else:
        return Decimal(400) + (x - 500) * Decimal(100) / 260

def get_PM10_subindex(x):
    x = Decimal(x)
    if x <= 100:
        return x * Decimal(50) / 100
    elif x <= 200:
        return Decimal(50) + (x - 100) * Decimal(50) / 100
    elif x <= 350:
        return Decimal(100) + (x - 200) * Decimal(100) / 150
    elif x <= 430:
        return Decimal(200) + (x - 350) * Decimal(100) / 80
    elif x <= 600:
        return Decimal(300) + (x - 430) * Decimal(100) / 170
    else:
        return Decimal(400) + (x - 600) * Decimal(100) / 170

def get_SO2_subindex(x):
    x = Decimal(x)
    if x <= 80:
        return x * Decimal(50) / 80
    elif x <= 160:
        return Decimal(50) + (x - 80) * Decimal(50) / 80
    elif x <= 800:
        return Decimal(100) + (x - 160) * Decimal(100) / 640
    elif x <= 1600:
        return Decimal(200) + (x - 800) * Decimal(100) / 800
    elif x <= 3200:
        return Decimal(300) + (x - 1600) * Decimal(100) / 1600
    else:
        return Decimal(400) + (x - 3200) * Decimal(100) / 1600

def get_NOx_subindex(x):
    x = Decimal(x)
    if x <= 80:
        return x * Decimal(50) / 80
    elif x <= 160:
        return Decimal(50) + (x - 80) * Decimal(50) / 80
    elif x <= 320:
        return Decimal(100) + (x - 160) * Decimal(100) / 160
    elif x <= 400:
        return Decimal(200) + (x - 320) * Decimal(100) / 80
    elif x <= 600:
        return Decimal(300) + (x - 400) * Decimal(100) / 200
    else:
        return Decimal(400) + (x - 600) * Decimal(100) / 200

def get_CO_subindex(x):
    if x <= 1000:  # 1 mg/m³ = 1000 µg/m³
        return x * 50 / 1000
    elif x <= 2000:
        return 50 + (x - 1000) * 50 / 1000
    elif x <= 10000:
        return 100 + (x - 2000) * 100 / 8000
    elif x <= 17000:
        return 200 + (x - 10000) * 100 / 7000
    elif x <= 34000:
        return 300 + (x - 17000) * 100 / 17000
    elif x > 34000:
        return 400 + (x - 34000) * 100 / 17000
    else:
        return 0

def get_O3_subindex(x):
    x = Decimal(x)
    if x <= 100:
        return x * Decimal(50) / 100
    elif x <= 200:
        return Decimal(50) + (x - 100) * Decimal(50) / 100
    elif x <= 336:
        return Decimal(100) + (x - 200) * Decimal(100) / 136
    elif x <= 416:
        return Decimal(200) + (x - 336) * Decimal(100) / 80
    elif x <= 1496:
        return Decimal(300) + (x - 416) * Decimal(100) / 1080
    else:
        return Decimal(400) + (x - 1496) * Decimal(100) / 1080
