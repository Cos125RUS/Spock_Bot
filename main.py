import time
import datetime as dt
import logging
import random
from aiogram import Bot, Dispatcher, executor, types
from os import path
from img_count import *

# 'UTF-8-sig'
logging.basicConfig(level=logging.INFO, filename="bot_log.csv", filemode="w",
                    format="%(asctime)s: %(levelname)s %(funcName)s-%(lineno)d %(message)s")

MSG = "{}, Жмякни кнопку внизу, и я скину тебе мою фотку=)"

bot = Bot("6012678486:AAEkMXJOmBjStU1kbadh6yuTBhDIdkoh7oo")
dp = Dispatcher(bot=bot)
img_count = counter()


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    user_bot = message.from_user.is_bot
    user_message = message.text
    logging.info(f'{user_id=} {user_bot=} {user_message=}')
    await message.reply(f"Привет, человек!")
    await message.reply(f"Как сам?")
    time.sleep(1)
    btns = types.ReplyKeyboardMarkup(row_width=1)
    btn_photo = types.KeyboardButton('/Photo')
    btns.add(btn_photo)
    await bot.send_message(user_id, MSG.format(user_name), reply_markup=btns)


@dp.message_handler(commands=['Photo'])
async def photo_handler(message: types.Message):
    answers = ["Смотри, это я", "Вот, глянь на это", "Как я здесь получился?", "Вот это моё любимое",
               "Тебе не кажется, что эта шкура слегка меня полнит?", "Гляди как я хорош!",
               "Как же круто блестит моя шерсть", "Лублю бегать", "Не самый мой лучший ракурс",
               "Я зайча-собача", "Не правда ли я лучшая собака на свете?", "А у меня щенячьи глазки",
               "Повелитель шерсти!", "Иногда меня путают с меховым ковриком", "Люблю гулять, кушать и спать",
               "Вот тебе моя плюшевая жопка", "Завистники называют меня тараканом",
               "Собираю пожертвование мандаринами", "Мечтаю о новой игрушке", "Когда-то я был щеночком",
               "Да-да, меня все любят", "Подумываю об актёрской карьере", "Я рыжая морда"]
    ans = random.randint(0, len(answers) - 1)
    # count_img = counter()
    num = random.randint(0, img_count)
    name = f'photo\{num}.jpg'
    print(f'{dt.datetime.now()}\t{message.from_user.id}\t{message.from_user.full_name}'
          f'\t{name.replace("photo", "")}')
    loger((dt.datetime.now(), message.chat.id, message.from_user.full_name, 'Give'))
    with open(name, 'rb') as img:
        await bot.send_photo(message.from_user.id, img)
    await bot.send_message(message.from_user.id, answers[ans])


@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
    global img_count
    chatId = message.chat.id
    check = {413687869: "Валера", 582499322: "Таня", 493072257: "Паша", 562407291: "Тома"}
    if chatId in check.keys():
        # newPhoto = counter()
        print(f'{dt.datetime.now()}\t{chatId}\t{message.chat.full_name}\tnew photo {img_count}.jpg')
        loger((dt.datetime.now(), chatId, message.chat.full_name, 'Take'))
        # await message.photo[-1].download(f'photo\{img_count}.jpg')
        await message.photo[-1].download(f'photo\{counting()}.jpg')
        await bot.send_message(message.from_user.id, 'М-м-м, да я красавчик!')
    else:
        print(f'{dt.datetime.now()}\t{chatId}\t{message.from_user.full_name}\tTrying to send a photo')
        loger((dt.datetime.now(), chatId, message.chat.full_name, 'Trying send'))


def counting():
    global img_count
    img_count += 1
    return img_count - 1


# def counter():
#     count = 0
#     while path.isfile(f'photo\{count}.jpg'):
#         count += 1
#     return count


def loger(data):
    time, userID, userName, act = data
    log = f'{time};{userID};{userName};{act}\n'
    with open('activity_log.csv', 'a') as file:
        file.write(log)


if __name__ == '__main__':
    print("Server start")
    executor.start_polling(dp)
