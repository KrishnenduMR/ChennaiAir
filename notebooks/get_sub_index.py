def get_PM25_subindex(x):
    if x <= 60:
        return x * 50 / 60
    elif x <= 120:
        return 50 + (x - 60) * 50 / 60
    elif x <= 180:
        return 100 + (x - 120) * 100 / 60
    elif x <= 240:
        return 200 + (x - 180) * 100 / 60
    elif x <= 500:
        return 300 + (x - 240) * 100 / 260
    else:
        return 400 + (x - 500) * 100 / 260

def get_PM10_subindex(x):
    if x <= 100:
        return x * 50 / 100
    elif x <= 200:
        return 50 + (x - 100) * 50 / 100
    elif x <= 350:
        return 100 + (x - 200) * 100 / 150
    elif x <= 430:
        return 200 + (x - 350) * 100 / 80
    elif x <= 600:
        return 300 + (x - 430) * 100 / 170
    else:
        return 400 + (x - 600) * 100 / 170

def get_SO2_subindex(x):
    if x <= 80:
        return x * 50 / 80
    elif x <= 160:
        return 50 + (x - 80) * 50 / 80
    elif x <= 800:
        return 100 + (x - 160) * 100 / 640
    elif x <= 1600:
        return 200 + (x - 800) * 100 / 800
    elif x <= 3200:
        return 300 + (x - 1600) * 100 / 1600
    else:
        return 400 + (x - 3200) * 100 / 1600

def get_NOx_subindex(x):
    if x <= 80:
        return x * 50 / 80
    elif x <= 160:
        return 50 + (x - 80) * 50 / 80
    elif x <= 320:
        return 100 + (x - 160) * 100 / 160
    elif x <= 400:
        return 200 + (x - 320) * 100 / 80
    elif x <= 600:
        return 300 + (x - 400) * 100 / 200
    else:
        return 400 + (x - 600) * 100 / 200

def get_CO_subindex(x):
    if x <= 2000:
        return x * 50 / 2000
    elif x <= 4000:
        return 50 + (x - 2000) * 50 / 2000
    elif x <= 10000:
        return 100 + (x - 4000) * 100 / 6000
    elif x <= 17000:
        return 200 + (x - 10000) * 100 / 7000
    elif x <= 34000:
        return 300 + (x - 17000) * 100 / 17000
    else:
        return 400 + (x - 34000) * 100 / 17000

def get_O3_subindex(x):
    if x <= 100:
        return x * 50 / 100
    elif x <= 200:
        return 50 + (x - 100) * 50 / 100
    elif x <= 336:
        return 100 + (x - 200) * 100 / 136
    elif x <= 416:
        return 200 + (x - 336) * 100 / 80
    elif x <= 1496:
        return 300 + (x - 416) * 100 / 1080
    else:
        return 400 + (x - 1496) * 100 / 1080