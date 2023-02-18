import time
import datetime as dt
import logging
import random
from aiogram import Bot, Dispatcher, executor, types
from img_count import *

# 'UTF-8-sig'
logging.basicConfig(level=logging.INFO, filename="bot_log.csv", filemode="w",
                    format="%(asctime)s: %(levelname)s %(funcName)s-%(lineno)d %(message)s")

MSG = "{}, Жмякни кнопку внизу, и я скину тебе мою фотку=)"

# bot = Bot("5643214927:AAHBaSv6StJppul8z1F1y8oS-dGLakVBC-k") # TestBot
bot = Bot("6012678486:AAEkMXJOmBjStU1kbadh6yuTBhDIdkoh7oo")
dp = Dispatcher(bot=bot)
img_count = counter()
flag: bool


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
    btns = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
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
               "Да-да, меня все любят", "Подумываю об актёрской карьере", "Я рыжая морда",
               "Может, купишь мне сосиску в тесте?", "Ожидаю получить новую игрушку на день рождения",
               "Познакомишь меня с какой-нибудь сучкой?)", "Надеюсь, ты не из кошатников?",
               "Я шерстяной монстр!", "Я меховой монстр!",
               "А это правда, что за собачью шерсть кто-то готов доплачивать?",
               "Сведёш меня с покупателями собачьей шерсти?", "Люблю хруст пластиковой бутылки:)",
               "Большую часть дня я сплю", "У меня всегда есть время на сон", "Во сне меня кормили котлетами",
               "Расскажи, какова котлета на вкус?", "Люблю хрустеть пластиковой бутылкой по утрам=)",
               "Я плюшевая жопка=)", "Вот тебе моя милая рыжая мордашка=)"]
    ans = random.randint(0, len(answers) - 1)
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
    global flag
    flag = True
    chatId = message.chat.id
    check = {413687869: "Валера", 582499322: "Таня", 493072257: "Паша", 562407291: "Тома"}
    if chatId in check.keys():
        print(f'{dt.datetime.now()}\t{chatId}\t{message.chat.full_name}\tnew photo {img_count}.jpg')
        loger((dt.datetime.now(), chatId, message.chat.full_name, 'Take'))
        await message.photo[-1].download(f'photo\{counting()}.jpg')
        # await message.photo[-1].download(f'Tests\{counting()}.jpg') # Test
        await bot.send_message(message.from_user.id, get_answers(check[chatId]))
    else:
        print(f'{dt.datetime.now()}\t{chatId}\t{message.from_user.full_name}\tTrying to send a photo')
        loger((dt.datetime.now(), chatId, message.chat.full_name, 'Trying send'))



def counting():
    global img_count
    img_count += 1
    return img_count - 1


def loger(data):
    time, userID, userName, act = data
    log = f'{time};{userID};{userName};{act}\n'
    with open('activity_log.csv', 'a') as file:
        file.write(log)


def get_answers(name):
    global flag
    if flag:
        flag = False
        options = ['М-м-м, да я красавчик!', 'Боже, как я хорош!', 'Просто лучший!',
                   'Говорят, телефон высасывает душу.\nЧто ж, пусть высосет из меня всю=)',
                   'А-у-у-у-у-у!']
        rand = random.randint(0, len(options) - 1)
        answer = options[rand] + f'\nСпасибо, {name}\nЕсть ещё?)'
        return answer


if __name__ == '__main__':
    print("Server start")
    executor.start_polling(dp)
