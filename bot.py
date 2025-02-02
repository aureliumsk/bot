import telebot
from telebot.types import InputFile
from uuid import uuid4
from config import *
from logic import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может показывать города на карте. Напиши /help для списка команд.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, """Доступные команды:
    /help - справка
    /remember_city - \"запомнить\" город
    /show_city <город> - показать город
    /show_my_cities - показать сохранённые города
    """)

@bot.message_handler(commands=['show_city'])
def handle_show_city(message):
    city_name = message.text.split()[-1]

    filename = f"{uuid4()}.png"
    manager.create_grapf(filename, [city_name])

    bot.send_photo(message.chat.id, InputFile(filename))    


@bot.message_handler(commands=['remember_city'])
def handle_remember_city(message):
    user_id = message.chat.id
    city_name = message.text.split()[-1]
    if manager.add_city(user_id, city_name):
        bot.send_message(message.chat.id, f'Город {city_name} успешно сохранен!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    cities = manager.select_cities(message.chat.id)
    filename = f"{uuid4()}.png"
    manager.create_grapf(filename, cities)
    bot.send_photo(message.chat.id, InputFile(filename))


if __name__=="__main__":
    manager = DB_Map(DATABASE)
    bot.polling()
