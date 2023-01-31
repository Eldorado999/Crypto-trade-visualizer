# Метод должен получать: сообщение от бота
# Метод должен выдавать:
#   монетную пару в формате "BTCUSDT"
#   первую дату в формате: datetime
#   частоту построения графика в формате: "1min", "5min", "15min", "30min", "1H", "2H", "4H", "6H", "8H", "12H", "1D",
#                                         "3D", "1W", "1M"
#   множитель ширины свечей width_mult (int)
#   список цен open длиной 151
#   список цен close длиной 151
#   список цен high длиной 151
#   список цен low длиной 151
#   список arrows


import json
import requests
from datetime import datetime


def parse_msg(message):
    try:
        message = message[message.find("{"):]
        message = message[:message.rfind("}") + 1]
        return json.loads(message)
    except Exception as e:
        print(e)
        return None


def get_spot(symbol, tick_interval, first, last):
    url = 'https://api.binance.com/api/v3/klines?symbol=' + symbol + '&interval=' + tick_interval + '&startTime=' + \
          str(first) + '&endTime=' + str(last)
    return requests.get(url).json()


def get_futures(symbol, tick_interval, first, last):
    url = 'https://fapi.binance.com/fapi/v1/klines?symbol=' + symbol + '&interval=' + tick_interval + '&startTime=' + \
          str(first) + '&endTime=' + str(last)
    return requests.get(url).json()


def get_data(json_object, trade):
    global klines
    try:
        symbol = str(json_object["symbol"])
        time_list = []
        max_time = 0
        min_time = 9999999999999
        for i in json_object["orders"]:
            _time = int(i['time'])
            time_list.append(_time)
            if _time > max_time:
                max_time = _time
            if _time < min_time:
                min_time = _time
        scale_sec_x1000 = max_time - min_time
        scale_sec = scale_sec_x1000 / 1000
        if scale_sec <= 60 * 130:
            int_mult = 1000 * 60
            first = min_time - 15 * int_mult
            last = first + 150 * int_mult
            tick_interval = '1m'
            freq = '1min'
            width_mult = 1
        elif 60 * 130 < scale_sec <= 300 * 130:
            int_mult = 1000 * 60 * 5
            first = min_time - 15 * int_mult
            last = first + 150 * int_mult
            tick_interval = '5m'
            freq = '5min'
            width_mult = 5
        elif 300 * 130 < scale_sec <= 900 * 130:
            int_mult = 1000 * 60 * 15
            first = min_time - 15 * int_mult
            last = first + 150 * int_mult
            tick_interval = '15m'
            freq = '15min'
            width_mult = 15
        elif 900 * 130 < scale_sec <= 1800 * 130:
            int_mult = 1000 * 60 * 30
            first = min_time - 15 * int_mult
            last = first + 150 * int_mult
            tick_interval = '30m'
            freq = '30min'
            width_mult = 30
        elif 1800 * 130 < scale_sec <= 3600 * 130:
            int_mult = 1000 * 3600
            first = min_time - 15 * int_mult
            last = first + 150 * int_mult
            tick_interval = '1h'
            freq = '1H'
            width_mult = 60
        elif 3600 * 130 < scale_sec <= 7200 * 130:
            int_mult = 1000 * 3600 * 2
            first = min_time - 15 * int_mult
            last = first + 150 * int_mult
            tick_interval = '2h'
            freq = '2H'
            width_mult = 60 * 2
        elif 7200 * 130 < scale_sec <= 14400 * 130:
            int_mult = 1000 * 3600 * 4
            first = min_time - 15 * int_mult
            last = first + 150 * int_mult
            tick_interval = '4h'
            freq = '4H'
            width_mult = 60 * 4
        elif 14400 * 130 < scale_sec <= 21600 * 130:
            int_mult = 1000 * 3600 * 6
            first = min_time - 15 * int_mult
            last = first + 150 * int_mult
            tick_interval = '6h'
            freq = '6H'
            width_mult = 60 * 6
        elif 21600 * 130 < scale_sec <= 28800 * 130:
            int_mult = 1000 * 3600 * 8
            first = min_time - 15 * int_mult
            last = first + 150 * int_mult
            tick_interval = '8h'
            freq = '8H'
            width_mult = 60 * 8
        elif 28800 * 130 < scale_sec <= 43200 * 130:
            int_mult = 1000 * 3600 * 12
            first = min_time - 15 * int_mult
            last = first + 150 * int_mult
            tick_interval = '12h'
            freq = '12H'
            width_mult = 60 * 12
        elif 43200 * 130 < scale_sec <= 86400 * 130:
            int_mult = 1000 * 86400
            first = min_time - 15 * int_mult
            last = first + 150 * int_mult
            tick_interval = '1d'
            freq = '1D'
            width_mult = 60 * 24
        elif 86400 * 130 < scale_sec <= 259200 * 130:
            int_mult = 1000 * 86400 * 3
            first = min_time - 15 * int_mult
            last = first + 150 * int_mult
            tick_interval = '3d'
            freq = '3D'
            width_mult = 60 * 24 * 3
        elif 259200 * 130 < scale_sec <= 604800 * 130:
            int_mult = 1000 * 604800
            first = min_time - 15 * int_mult
            last = first + 150 * int_mult
            tick_interval = '3d'
            freq = '1W'
            width_mult = 60 * 24 * 7
        elif 604800 * 130 < scale_sec <= 2592000 * 130:
            int_mult = 1000 * 2592000
            first = min_time - 15 * int_mult
            last = first + 150 * int_mult
            tick_interval = '1M'
            freq = '1M'
            width_mult = 43200
        else:
            print('more 130 month, impossible to create graph')
            return 'Too long period'
        _open = []
        _close = []
        high = []
        low = []
        if trade == 'SPOT':
            klines = get_spot(symbol, tick_interval, first, last)
        elif trade == 'FUTURES':
            klines = get_futures(symbol, tick_interval, first, last)
        else:
            klines = 'Должно быть указано SPOT или FUTURES'
        for i in klines:
            _open.append(float(i[1]))
            _close.append(float(i[4]))
            high.append(float(i[2]))
            low.append(float(i[3]))
        arrows = []
        for i in json_object["orders"]:
            k = [i["side"], i["price"], datetime.utcfromtimestamp(i["time"] / 1000)]
            arrows.append(k)
        return [symbol, datetime.utcfromtimestamp(int(klines[0][0]) / 1000), freq, width_mult, _open,
                _close, high, low, arrows]
    except Exception as e:
        print(e)
        return 'Ошибка:\n' + str(klines) + '\n' + str(e)
