from telebot import TeleBot
from telebot import types
import asyncio
from settings import TOKEN

bot = TeleBot(token=TOKEN)

# Handle '/start' and '/help'
@bot.message_handler(commands=['start', 'echo'])
def send_welcome(message):
    commands=['/start', '/echo']
    if message.text.find(commands[0]) > -1:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        moscow_btn = types.KeyboardButton("Moscow")
        sochi_btn = types.KeyboardButton("Sochi")
        vladivostok_btn = types.KeyboardButton("Vladivostok")
        markup.add(moscow_btn)
        markup.add(sochi_btn)
        markup.add(vladivostok_btn)
        bot.send_message(message.chat.id, "Привет! Нажми на кнопку и перейди на сайт)", reply_markup=markup)
    if  message.text.find(commands[1]) > -1:
        bot.send_message(message.chat.id, text=message.text.replace('/echo', ''))

@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "Moscow"):
        bot.send_message(message.chat.id, text="Погода в Москве")
    elif(message.text == "Sochi"):
        bot.send_message(message.chat.id, text="Погода в Сочи")
    elif(message.text == "Vladivostok"):
        bot.send_message(message.chat.id, text="Погода в Владивосток")


asyncio.run(bot.polling())