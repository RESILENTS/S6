from  config import *
from  keyboard import *

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id

    inline_keyboard = types.InlineKeyboardMarkup(row_width = 1)
    inline_1 = types.InlineKeyboardButton(text = "✅ Принять правила проекта", callback_data = 'RULES')
    inline_keyboard.add(inline_1)

    bot.send_message(chat_id, f'💁🏻‍♀️ Правила нашего магазина:\n\n• Осуществление возврата денежных средств за продукцию производится только на внутри лицевой счёт магазина\n• Администрация оставляет за собой право на изменение установленных правил без оповещения пользователей'
        + '\n• Администрация вправе ограничить доступ определённому лицу без объяснения причины\n• Администрация вправе обнулить внутри лицевой счёт пользователя при подозрении в мошенничестве\n• Отсутствие видеозаписи - основание для отказа в гарантийном обслуживаниии'
        + '\n• Гарантия на аккаунты GFN составляет 1 день\n\n💁🏻‍♀️ Вы подтверждаете, что *ознакомились и согласны с условиями и правилами* нашего магазина?',
    parse_mode="Markdown", reply_markup=inline_keyboard)

    except Exception as e:
        print(e)
    username = message.from_user.username
    with sqlite3.connect('users.db') as conn:
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS user(username TEXT, user_id INTEGER);""")
        cur.execute("SELECT * FROM user WHERE `user_id` = '{}'".format(chat_id))
        row = cur.fetchall()
        if len(row) == 0:
            cur.execute("INSERT INTO `user` (`username`, `user_id`) VALUES(?,?)",
                        (username, chat_id,))
    text = '👋 Приветствую, <b>'+message.from_user.first_name +'</b> — Я помогу тебе получить бесплатно схемы заработка, курсы по бизнесу, мануалы, инфопродукты и другую полезную информацию с разных форумах. \n\nУ меня есть база данных слитых хайдов с разных интернет площадок.\n\n🏠 <b>Наш канал:</b> @sorgeny\n💭 <b>Наш чат:</b> @sorgeny_chat\n👥 <b>Поддержка:</b> @sorgeny_support'
    img = open ('welc.webp', 'rb')
    bot.send_photo(chat_id, img, caption=text, reply_markup=main_keyboard(), parse_mode='html')

@bot.message_handler(commands=['admin'])
def admin(message):
    chat_id = message.from_user.id
    if chat_id in admins:
        bot.send_message(chat_id, '🛠️ Добро пожаловать в Админ панель.', reply_markup=admin_keyboard())


@bot.message_handler(content_types=['text'])
def text(message):
    chat_id = message.from_user.id
    if message.text == '📊 Статистика':
        with sqlite3.connect('users.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM user")
            row = cur.fetchall()
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute("select count(*) from links") 
            result2 = cursor.fetchone()[0]
            bot.send_message(message.chat.id, f'''📊  <b>Статистика бота SORGENY:</b>

 —  <b>Сливов в базе данных:</b> {result2}
 —  <b>Количество пользователей:</b> ''' + str(len(row)), parse_mode='HTML')

    if message.text == "📥 Получить хайд":
        global link_idm
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute("select count(*) from links") 
        result2 = cursor.fetchone()[0]
        link_idm = message.text
        msg = bot.send_message(message.chat.id, f'''🔍  <b>Введите ссылку для поиска в базе данных.</b>

⚠️  <b>ВНИМАНИЕ!</b> Если вы отправите ссылку с не актуальным доменом то <b>БОТ</b> не сможет найти запись в базе данных.
        
🟢  <b>Актуальные домены:</b>
 — slivup.cc
 
📊  <b>Сливов в базе данных:</b> {result2}''', parse_mode='HTML')
        bot.register_next_step_handler(msg, getlinkm)
    elif message.text == 'Рассылка' and chat_id in admins:
        message = bot.send_message(chat_id, '💁🏻‍♀️ Введите *сообщение* для рассылки', parse_mode="Markdown")
        bot.register_next_step_handler(message, add_message)

    elif message.text == 'Добавить в БД' and chat_id in admins:
        msg = bot.send_message(chat_id, '➕ Введите главную ссылку.\n\n Внимание! По этой ссылке будет производится поиск в базе данных.',parse_mode='HTML')
        bot.register_next_step_handler(msg, add1)

    elif message.text == '👥 Поддержка':
        bot.send_message(message.chat.id, '📩 На данный момент все запросы на слив принимаем в ручную.\n\nОтправте свои ссылки в ЛС по контактам ниже:\n👥 @sorgeny_support',parse_mode='HTML')

    elif message.text == 'Список всех пользователей' and chat_id in admins:
        with sqlite3.connect('users.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT * from `user`")
            row = cur.fetchall()
            w_file = open("users.csv", mode="w", encoding='utf-8')
            file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
            for rows in row:
                file_writer.writerow(rows)
            w_file.close()
            with open(curdir + "/users.csv", "r") as file:
                bot.send_document(chat_id, file)
                
def getlinkm(message):
        global link_coment, link_text, sql, link_id, get_link_new, link_global
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        link_coment = ""
        link_text = ""
        link_id = message.text
        link_global = link_id
        sql = "SELECT * FROM links WHERE link_id =?"
        result = cursor.fetchall()
        for row in cursor.execute(sql, ([link_id])):
            link_id = list(row)[0]
            link_coment = list(row)[1]
            link_text = list(row)[2]
        if  not link_text: 
            keyboard = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(text="➕ Отправить запрос на слив", callback_data="new_link")
            keyboard.add(btn1)
            bot.send_message(message.chat.id, f'''❌ <b>ОШИБКА:</b> По вашему запросу <b>"{link_id}"</b> ничего не найдено.
	    
Нажмите на кнопку ниже для отправки запроса на слив вашего запроса.''', reply_markup=keyboard, parse_mode='HTML')
        else:
            keyboard = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(text="❌ Удалить запрос", callback_data="get_close")
            keyboard.add(btn1)
            bot.send_message(message.chat.id, f'''🔍  <b>Результат по вашему запросу:</b>

🔗  <b>Ссылка вашего запроса: </b>
 — {link_id}
 
💭  <b>Продажник:</b>
{link_text}

🔐  <b>Скрытое содержимое: </b>
{link_coment}

''',reply_markup=keyboard, parse_mode='HTML')

def search1(message):
        global link_id
        link_id = message.text
        msg = bot.send_message(message.chat.id, f'''🔍  <b>Введите ссылку для поиска в базе данных.</b>

⚠️  <b>ВНИМАНИЕ!</b> Если вы отправите ссылку с не актуальным доменом то <b>БОТ</b> не сможет найти запись в базе данных.
        
🟢  <b>Актуальные домены:</b>
 — slivup.cc''', parse_mode='HTML')
        bot.register_next_step_handler(msg, add2)

def add1(message):
        global m1
        m1 = message.text
        msg = bot.send_message(message.chat.id, '➕ Введите коментарии к посту.',parse_mode='HTML')
        bot.register_next_step_handler(msg, add2)

def add2(message):
        global m2
        m2 = message.text
        msg = bot.send_message(message.chat.id, '➕ Введите скрытое содержимое.',parse_mode='HTML')
        bot.register_next_step_handler(msg, add3)

def add3(message):
        global m3
        m3 = message.text
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='✅ Опубликовать пост',callback_data=f'принятьзаявку_{message.chat.id}'))
        bot.send_message(message.chat.id, f'''Предпросмотр публикации:

◾ Ссылка: {m1}
◾ Содержимое скрытого текста: {m3}

◾ Коментарии к публикации:
{m2}''',parse_mode='HTML',reply_markup=keyboard)

def db_table_val(link_id: str, link_coment: str, link_text: str):
    params = (link_id, link_coment, link_text)
    cursor.execute(f'''INSERT INTO links (link_id, link_coment, link_text) VALUES ('{m1}', '{m3}', '{m2}')''')
    conn.commit()

@bot.callback_query_handler(func=lambda call:True)
def podcategors(call):
    if call.data == 'get_close':
        bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
	
    if call.data[:14] == 'принятьзаявку_':
        idasd = call.data[14:]
        bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
        main = telebot.types.ReplyKeyboardMarkup(True)
        bot.send_message(idasd,reply_markup=main, text='✅ Успешно!')

        link_id = {m1}
        link_coment = {m3}
        link_text = {m2}
        db_table_val(link_id=link_id, link_coment=link_coment, link_text=link_text)

    if call.data == 'new_link':
        bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, '📩 На данный момент все запросы на слив принимаем в ручную.\n\nОтправте свои ссылки в ЛС по контактам ниже:\n👥 @sorgeny_support',parse_mode='HTML')

bot.polling()
