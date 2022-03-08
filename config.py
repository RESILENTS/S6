import telebot, sqlite3, random, string, csv, os
from SimpleQIWI import *
from telebot import types

username = message.from_user.username
username = username.replace('_', '\\_')

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

curdir = os.curdir

bot = telebot.TeleBot('5298338850:AAHKVHFUJrFCTJ3qmNrWDK31KgFiYU91YIg') #токен бота

admins = [641892529, 1938749145] #айди админов

id1 = []

def add_message(message):
        if (message.text != 'Назад'):
            rows = get_usersId_banker()

            for row in rows:
                try:
                    bot.send_message(row, message.text, parse_mode='HTML')
                except Exception as e:
                    print(e)
                    continue

def get_usersId_banker():
    try:
        array = []

        with sqlite3.connect("users.db") as con:
            cur = con.cursor()
            rows = cur.execute("SELECT user_id FROM user").fetchall()

            for row in rows:
                array.append(row[0])

        return array
    except Exception as e:
        print(e)


def bill_create(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))
