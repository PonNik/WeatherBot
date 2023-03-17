from telebot import TeleBot
from telebot import types
import requests
from bs4 import BeautifulSoup as BS
import asyncio
from settings import TOKEN, URL_WEATHER

cities = ['gorod134242-Russia-g_Moskva-Moskva','gorod148-Russia-Krasnodarskiy_kray-Sochi', 'gorod167-Russia-Primorskiy_kray-Vladivostok']

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
        r = requests.get(URL_WEATHER + cities[0])
        print(r.status_code)
        soup = BS(r.text, 'html.parser')

        temp = soup.find('div', class_='current_data')
        info = temp.find('img').get('title')
        bot.send_message(message.chat.id, text=info)
    elif(message.text == "Sochi"):
        r = requests.get(URL_WEATHER + cities[1])
        print(r.status_code)
        soup = BS(r.text, 'html.parser')

        temp = soup.find('div', class_='current_data')
        info = temp.find('img').get('title')
        bot.send_message(message.chat.id, text=info)
    elif(message.text == "Vladivostok"):
        r = requests.get(URL_WEATHER + cities[2])
        print(r.status_code)
        soup = BS(r.text, 'html.parser')

        temp = soup.find('div', class_='current_data')
        info = temp.find('img').get('title')
        bot.send_message(message.chat.id, text=info)


asyncio.run(bot.polling())