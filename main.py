from telebot import TeleBot
from telebot import types
import asyncio
from settings import TOKEN

bot = TeleBot(token=TOKEN)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn0 = types.KeyboardButton("Moscow")
    itembtn1 = types.KeyboardButton("Sochi")
    itembtn2 = types.KeyboardButton("Vladivostok")
    markup.add(itembtn0)
    markup.add(itembtn1)
    markup.add(itembtn2)
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку и перейди на сайт)", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "Moscow"):
        bot.send_message(message.chat.id, text="Погода в москве")
    elif(message.text == "Sochi"):
        bot.send_message(message.chat.id, text="Погода в москве")
    elif(message.text == "Vladivostok"):
        bot.send_message(message.chat.id, text="Погода в москве")


asyncio.run(bot.polling())