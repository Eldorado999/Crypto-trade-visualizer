import matplotlib.pyplot as plt
from matplotlib import dates
import pandas as pd
from datetime import timedelta
from operator import itemgetter


def draw_graph(data, user_id):
    pair = data[0]
    date = data[1]
    freq = data[2]
    width_mult = data[3]
    _open = data[4]
    _close = data[5]
    high = data[6]
    low = data[7]
    arrows = data[8]
    if len(_open) == 0:
        return 'Wrong data'
    try:
        prices = pd.DataFrame({'open': _open,
                               'close': _close,
                               'high': high,
                               'low': low},
                              index=pd.date_range(date, periods=len(_open), freq=freq, tz='UTC'))

        title = f'{pair} - {freq} - BINANCE'
        fig = plt.figure(figsize=(14, 7), facecolor='#eee')
        ax = fig.add_subplot()
        fig.suptitle(title, fontsize=20)
        ax.set_ylabel('Price', fontsize=14)
        ax.patch.set_facecolor('#000000')

        up = prices[prices.close >= prices.open]
        down = prices[prices.close < prices.open]
        width = .0007 * width_mult
        width2 = .000075 * width_mult
        col1 = 'green'
        col2 = 'red'

        ax.bar(up.index, up.close - up.open, width, bottom=up.open, color=col1)
        ax.bar(up.index, up.high - up.close, width2, bottom=up.close, color=col1)
        ax.bar(up.index, up.low - up.open, width2, bottom=up.open, color=col1)
        ax.bar(down.index, down.close - down.open, width, bottom=down.open, color=col2)
        ax.bar(down.index, down.high - down.open, width2, bottom=down.open, color=col2)
        ax.bar(down.index, down.low - down.close, width2, bottom=down.close, color=col2)

        if len(arrows) > 0:
            arrows = sorted(arrows, key=itemgetter(1), reverse=True)
            sorted_arrows = []
            for arrow in arrows:
                k = 0
                for i in range(len(prices)):
                    q = prices.index[i].to_pydatetime().replace(tzinfo=None)
                    if (arrow[2] - q) >= timedelta(days=0):
                        k = i
                j = 0
                for i in sorted_arrows:
                    if i[0] == arrow[0] and i[2] == k:
                        i[3] = str(i[3]) + '\n' + str(arrow[1])
                        j = 1
                if j == 0:
                    sorted_arrows.append([arrow[0], arrow[1], k, arrow[1]])
            sorted_arrows = sorted(sorted_arrows, key=itemgetter(2))
            miny = min(low)
            maxy = max(high)
            one_percent = (maxy - miny) / 100
            blocked = []
            for arrow in sorted_arrows:
                str_count = str(arrow[3]).count('\n') + 1
                arrow_obj = prices.iloc[[arrow[2]]]
                if arrow[0] == 'SELL':
                    ax.text(arrow_obj.index, arrow[1], "↓",
                            color='#FFFFFF', fontweight='bold', ha='center', va='bottom', fontsize=12)
                    ycord = arrow[1] + 3 * one_percent
                    check = 0
                    while check != len(blocked):
                        if blocked[check][0] < arrow[2] < blocked[check][1]:
                            if blocked[check][2] - str_count * 3 * one_percent < ycord < blocked[check][3]:
                                ycord = ycord + 0.5 * one_percent
                                check = 0
                            else:
                                check += 1
                        else:
                            check += 1
                    ax.text(arrow_obj.index, ycord, f"{arrow[3]}",
                            color='#FFFFFF', fontweight='bold', ha='center', va='bottom', fontsize=9)
                    blocked.append([arrow[2] - 8, arrow[2] + 8, ycord, ycord + str_count * 3 * one_percent])
                elif arrow[0] == 'BUY':
                    ax.text(arrow_obj.index, arrow[1], "↑",
                            color='#FFFFFF', fontweight='heavy', ha='center', va='top', fontsize=12)
                    ycord = arrow[1] - 3 * one_percent - 3 * one_percent * str_count
                    check = 0
                    while check != len(blocked):
                        if blocked[check][0] < arrow[2] < blocked[check][1]:
                            if blocked[check][2] - str_count * 3 * one_percent < ycord < blocked[check][3]:
                                ycord = ycord - 0.5 * one_percent
                                check = 0
                            else:
                                check += 1
                        else:
                            check += 1
                    ax.text(arrow_obj.index, ycord, f"{arrow[3]}",
                            color='#FFFFFF', fontweight='bold', ha='center', va='bottom', fontsize=9)
                    blocked.append([arrow[2] - 8, arrow[2] + 8, ycord, ycord + str_count * 3 * one_percent])

        ax.minorticks_on()
        ax.xaxis.set_ticks(prices.index, minor=True)
        major_ticks = []
        j = 0
        for i in prices.index:
            if j % 15 == 0:
                major_ticks.append(i)
            j += 1
        ax.xaxis.set_ticks(major_ticks)
        ax.grid(which='major', color='#aaa', alpha=0.5)
        ax.grid(which='minor', color='#aaa', ls=':', alpha=0.5)
        ax.yaxis.set_major_locator(plt.MaxNLocator(15))
        ax.yaxis.set_minor_locator(plt.NullLocator())
        ax.xaxis.set_major_formatter(dates.DateFormatter('%d/%m/%y\n%H:%M'))
        ax.set_axisbelow(True)

        plt.savefig(f'{str(user_id)}.png')
        return 'Done'
    except Exception as e:
        print(e)
        return None
