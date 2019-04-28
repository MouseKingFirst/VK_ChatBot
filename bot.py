import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
import requests
import random

def weather():
    header = {
        'X-Yandex-API-Key': '',#Ваш ключи для яндекс.Погоды
    }
    res = requests.get('https://api.weather.yandex.ru/v1/forecast?lat=55.75396&lon=37.620393&extra=true', headers = header).json()
    now = res['fact']
    temp = str(now['temp']) + '°C'
    feel = str(now['feels_like']) + '°C'
    wind_speed = str(now['wind_speed']) + ' м/с'
    humidity = str(now['humidity']) + '%'
    pressure_mm = str(now['pressure_mm']) + ' мм рт.ст.'
    output = 'Сейчас в Москве: '+temp+'\nЧувствуется на: '+feel+'\nСкорость ветра: '+wind_speed+'\nВлажность воздуха (в процентах): '+humidity+'\nДавление: '+pressure_mm
    return output


def ExchangeRates():
    """Актуальный курс валюты на сегодня"""
    res = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    valute = res['Valute']
    usd = valute['USD']
    eur = valute['EUR']
    # Доллар
    NameUsd = str(usd['Name'])
    ValueUsd = str(usd['Value'])
    # Евро
    NameEur = str(eur['Name'])
    ValueEur = str(eur['Value'])
    #Вывод
    info = 'Вся информация предоставляется сайтом https://www.cbr-xml-daily.ru'
    output = 'Обменный курс по ЦБ РФ на сегодня \n'+NameUsd+': '+ValueUsd+'\n'+NameEur+': '+ ValueEur+'\n'+info
    return output

def bitcoin():
    res = requests.get('https://api.coindesk.com/v1/bpi/currentprice/RUB.json').json()
    time = res['time']['updated']
    dollars = str(res['bpi']['USD']['rate'])
    rub = str(res['bpi']['RUB']['rate'])
    info = str('По курсу coindesk.com на '+time)
    output = 'Текущий курс биткоина \n 1 Биткоин = '+rub+' рублей \n 1 Биткоин = '+dollars+' долларов \n'+info
    return output

def help():
    """Текст для команды помощь"""
    file = open('help.txt', 'r',encoding='utf8')
    output = file.read()
    file.close()
    return output

def main():
    #Далее идёт настройка самого бота
    token = ""#Ключ для VKApi
    vk = vk_api.VkApi(token=token)
    longpoll = VkLongPoll(vk)
    #Настройка клавиатуры
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Погода', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Курс валюты', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()  # Переход на вторую строку
    keyboard.add_button('Курс биткоина', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()  # Переход на вторую строку
    keyboard.add_button('Помощь', color=VkKeyboardColor.PRIMARY)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            text_user = event.text.lower().replace(' ', '')
            if text_user == 'погода':
                vk.method('messages.send', {
                    'user_id': event.user_id,
                    'message':  weather(),
                    'random_id': get_random_id(),
                    'keyboard': keyboard.get_keyboard()
                })
            if text_user == 'cлучайноечисло':
                num = str(random.randint(1, 100))
                vk.method('messages.send', {
                    'user_id': event.user_id,
                    'message': 'Случайное число: '+num,
                    'random_id': get_random_id(),
                    'keyboard': keyboard.get_keyboard()
                })
            if text_user == 'курсвалюты':
                vk.method('messages.send', {
                    'user_id': event.user_id,
                    'message': ExchangeRates(),
                    'random_id': get_random_id(),
                    'keyboard': keyboard.get_keyboard()
                })
            if text_user == 'курсбиткоина':
                vk.method('messages.send', {
                    'user_id': event.user_id,
                    'message': bitcoin(),
                    'random_id': get_random_id(),
                    'keyboard': keyboard.get_keyboard()
                })
            if text_user == 'помощь':
                vk.method('messages.send', {
                    'user_id': event.user_id,
                    'message': help(),
                    'random_id': get_random_id(),
                    'keyboard': keyboard.get_keyboard()
                })
if __name__ == '__main__':
    main()
