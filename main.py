from config import token
import telebot
from telebot import types
import pandas as pd


bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, f'Здравствуй, {msg.from_user.first_name}! \nДля формирования конференций на текущий день загрузите в ответ на это сообщение файл формата excel. ')



@bot.message_handler(func = lambda m: True)
def getter(msg):
    bot.send_message(msg.chat.id, 'Файл получен, спасибо!')

bot.polling(none_stop=True, interval=0)

