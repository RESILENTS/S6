from telebot import types


def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    btn = types.KeyboardButton(text='📥 Получить хайд')
    btn2 = types.KeyboardButton(text='📊 Статистика')
    btn3 = types.KeyboardButton(text='ℹ️ FAQ')
    btn4 = types.KeyboardButton(text='👥 Поддержка')
    markup.add(btn, btn2)
    markup.add(btn3, btn4)
    return markup

def admin_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn = types.KeyboardButton(text='Рассылка')
    btn1 = types.KeyboardButton(text='Добавить в БД')
    btn2 = types.KeyboardButton(text='Кол-во пользователей')
    btn3 = types.KeyboardButton(text='Все пользователей')
    markup.add(btn, btn1)
    return markup
