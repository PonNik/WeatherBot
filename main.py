from telebot import TeleBot
from telebot import types
import os
import aiohttp
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
import asyncio
from settings import TOKEN

bot = TeleBot(token=TOKEN)

weather_list = [['Ливень', 'rain'], ['дождь', 'rain'], ['Дождь', 'rain'], ['Ясно', 'sunny'], ['Пасмурно', 'cloudy'], ['Малооблачно', 'partly_cloudy'], ['Облачно с прояснениями', 'partly_cloudy'], ['снег', 'snow'], ['Снег', 'snow'], ['Гроза', 'thunderstorm']]

async def parse(url):
    HEADERS = {'User-Agent': UserAgent().random}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as response:
            r = await aiohttp.StreamReader.read(response.content)
            soup = BS(r, 'html.parser')

            info_yesterday_weather = soup.find('div', 'fact__time-yesterday-wrap')
            info_time = info_yesterday_weather.find('time', 'time fact__time')
            info_temp = info_yesterday_weather.find('span', 'a11y-hidden')
            itog = f'{info_time.text}{info_temp.text}\n'
            
            info_now_weather = soup.find('div', 'fact__temp-wrap')
            info = info_now_weather.find('a', 'link fact__basic fact__basic_size_wide day-anchor i-bem').get('aria-label')
            itog += f'{info}\n'
            dop_info = soup.find('div', 'fact__props')
            veter = dop_info.find_all('span', 'a11y-hidden')
            for i in veter:
                itog += f'{i.text}\n'

            print('parse successfully')
            return itog

def get_image(weather):
    for weather_item in weather_list:
        if weather_item[0] in weather:
            return f'res/{weather_item[1]}.jpg'
    return ''

# Handle '/start' and '/help'
@bot.message_handler(commands=['start', 'echo'])
def send_welcome(message):
    commands=['/start', '/echo']
    if message.text.find(commands[0]) > -1:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        moscow_btn = types.KeyboardButton("Москва")
        sochi_btn = types.KeyboardButton("Сочи")
        vladivostok_btn = types.KeyboardButton("Владивосток")
        markup.add(moscow_btn)
        markup.add(sochi_btn)
        markup.add(vladivostok_btn)
        bot.send_message(message.chat.id, "Привет! Нажми на кнопку и перейди на сайт)", reply_markup=markup)
    if  message.text.find(commands[1]) > -1:
        bot.send_message(message.chat.id, text=message.text.replace('/echo', ''))

@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "Москва"):
        weather = asyncio.run(parse('https://yandex.ru/weather/moscow'))
        path_image = get_image(weather)
        if path_image == '':
            bot.send_message(message.chat.id,'В Москве\n\n' +  weather)
        else:
            photo = open(path_image, 'rb')
            bot.send_photo(message.chat.id, photo, 'В Москве\n\n' +  weather)
            photo.close()
    elif(message.text == "Сочи"):
        weather = asyncio.run(parse('https://yandex.ru/pogoda/sochi'))
        path_image = get_image(weather)
        if path_image == '':
            bot.send_message(message.chat.id,'В Сочи\n\n' +  weather)
        else:
            photo = open(path_image, 'rb')
            bot.send_photo(message.chat.id, photo, 'В Сочи\n\n' +  weather)
            photo.close()
    elif(message.text == "Владивосток"):
        weather = asyncio.run(parse('https://yandex.ru/pogoda/vladivostok'))
        path_image = get_image(weather)
        if path_image == '':
            bot.send_message(message.chat.id,'Во Владивостоке\n\n' +  weather)
        else:
            photo = open(path_image, 'rb')
            bot.send_photo(message.chat.id, photo, 'Во Владивостоке\n\n' +  weather)
            photo.close()
    else:
        bot.send_message(message.chat.id, '')


asyncio.run(bot.polling())