import os
import telebot

from telebot import types
from moduleReplicateApi import ReplicateInterface, paint_style

BOT_TOKEN = "6392729850:AAEVu3IXyY5oHC0kVg37bloYnt4gbRC1dE0"


SAVE_FOLDER = "photos/"
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)
bot = telebot.TeleBot(BOT_TOKEN)

USER_CHOISEN = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    items = []
    for i in paint_style.keys():
        items += [types.KeyboardButton(i)]

    markup.add(*items)
    with open("holst.png", 'rb') as f:
        bot.send_photo(message.chat.id, f)
    bot.reply_to(message, "Привет, вот твой холст. Выбери стиль и отправь свой набросок", reply_markup=markup)

@bot.message_handler(content_types=['photo'])
def save_photo(message):
    user_id = message.from_user.id
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_extension = file_info.file_path.split(".")[-1]
    file_path = os.path.join(SAVE_FOLDER, f"{user_id}.{file_extension}")
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_path, 'wb') as f:
        f.write(downloaded_file)
    bot.reply_to(message, "Фотография принята! Подождите 10 сек")

    style = "Realism"
    if message.chat.id in USER_CHOISEN:
        style = USER_CHOISEN[message.chat.id]
        print(message.chat.id, style)

    img = genimage(paint_style[style], file_path)

    with open(img + ".png", 'rb') as f:
        bot.send_photo(message.chat.id, f)
def genimage(prompt, imgpath):
    imgname = ReplicateInterface("r8_C30jBlJbQmFsWrEruydQqLYQOE93K7T3MU9Xf").imageInpaiting(prompt,imgpath)
    return imgname


@bot.message_handler(func=lambda message: message.text in list(paint_style.keys()))
def handle_choice(message):
    choice = message.text
    user_id = message.from_user.id

    USER_CHOISEN[user_id] = choice

    response = f"Вы выбрали prompt: {choice}."
    bot.reply_to(message, response)


bot.polling()

