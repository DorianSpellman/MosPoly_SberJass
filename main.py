from config import token
import telebot
from telebot import types
import pandas as pd


bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, f'Здравствуй, {msg.from_user.first_name}! \nДля формирования конференций на необходимый день загрузите в ответ на это сообщение файл формата excel ')



@bot.message_handler(content_types=['document'])
def doc(msg):
    try:
        file_info = bot.get_file(msg.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        file = file_info.file_path

        if file.endswith('.xlsx'):
            src = './saved_docs/' + msg.document.file_name

            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
                data = pd.read_excel(src)

                data.columns = ['date', 'id', 'teacher', 'email', 'call_number', 'discipline', 'start_time', 'end_time', 'link', 'room', 'groups', 'day', 'type']
                # print(data)

                # Write
                with open(src, 'a') as new_file:
                    for col in range(len(data)):
                        data['room'][col] = f'{generate_room()[0]} {str(col)}'
                        data['link'][col] = f'{generate_room()[1]} {str(col)}'

                    # Update data to excel
                    data.columns = ['Дата', 'ID', 'Преподаватель ФИО', 'Почта преподавателя', 'Телефон преподавателя', 'Название предмета', 
                                    'Время с', 'Время по', 'Ссылка', 'Вебинарная комната', 'Группы', 'День', 'Тип вебинара'
                                    ]
                    data.to_excel(src, header=True, index=False)  

            #print(data)
            bot.send_document(msg.chat.id, document=open(src, 'rb'),)
            bot.send_message(msg.chat.id, 'Файл отредактирован, спасибо!')
        else:
            bot.send_message(msg.chat.id, 'Файл должен быть в формате xlsx!')

    except Exception as e:
            bot.reply_to(msg, e)

@bot.message_handler(func = lambda m: True)
def another(message):
    bot.send_message(message.chat.id, 'Нажмите /start, чтобы начать')


def generate_room():
    'Генерация комнаты и ссылки'
    name = 'Room'
    link = 'Link'
    return (name, link)

            

bot.polling(none_stop=True, interval=0)

