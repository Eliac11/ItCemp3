import os
import telebot
from moduleReplicateApi import ReplicateInterface, paint_style

BOT_TOKEN = "6392729850:AAEVu3IXyY5oHC0kVg37bloYnt4gbRC1dE0"


SAVE_FOLDER = "photos/"
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Пожалуйста, отправь мне фотографию.")

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
    bot.reply_to(message, "Фотография принята!")

    img = genimage(paint_style["Realism"], file_path)

    with open(img + ".png", 'rb') as f:
        bot.send_photo(message.chat.id, f)
def genimage(prompt, imgpath):
    imgname = ReplicateInterface("r8_5DHHGh72D2WeQjtERBDmyc8mwt8iiv339O4qL").imageInpaiting(prompt,imgpath)
    return imgname


bot.polling()

