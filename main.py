import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import BOT_TOKEN
from banan import parse_msg, get_data
from draw import draw_graph


logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(text_contains='visualize_trade')
async def give_graph(message: types.Message):
    json_object = parse_msg(message.text)
    if json_object is None:
        await bot.send_message(message.from_user.id, 'Не могу распознать json в сообщении')
        print('Не могу распознать json в сообщении')
    else:
        if 'SPOT' in message.text:
            _data = get_data(json_object, 'SPOT')
        elif 'FUTURES' in message.text:
            _data = get_data(json_object, 'FUTURES')
        else:
            _data = 'Ошибка:\nВ сообщении должно быть указано SPOT или FUTURES'
        if 'Ошибка' in _data:
            await bot.send_message(message.from_user.id, 'Ошибка в получении данных с бинанса по указанным параметрам\n'
                                   + _data)
            print('Ошибка в получении данных с бинанса по указанным параметрам')
        elif _data == 'Too long period':
            await bot.send_message(message.from_user.id, 'Указанный период превышает 130 месяцев, не могу нарисовать '
                                                         'график')
            print('Указанный период превышает 130 месяцев, не могу нарисовать график')
        else:
            draw_result = draw_graph(_data, message.from_user.id)
            if draw_result is None:
                await bot.send_message(message.from_user.id,
                                       'Данные с binance получены. Ошибка визуализации')
                print('Данные с binance получены. Ошибка визуализации')
            elif draw_result == 'Wrong data':
                await bot.send_message(message.from_user.id, 'С binance пришли пустые значения')
                print('С binance пришли пустые значения')
            elif draw_result == 'Done':
                await bot.send_document(message.from_user.id, open(f'{str(message.from_user.id)}.png', 'rb'))
                await bot.send_photo(message.from_user.id, open(f'{str(message.from_user.id)}.png', 'rb'))
                print('Success')
                os.remove(f'{str(message.from_user.id)}.png')
            else:
                await bot.send_message(message.from_user.id, 'Неизвестная ошибка в визуализации')
                print('Неизвестная ошибка в визуализации')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
