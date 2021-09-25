import telebot
from telebot import types
import parse_data
from datetime import date, datetime, timedelta
import csv1
import error
bot = telebot.TeleBot("1786082801:AAEOePWM3kTbgLDALmK-6m46RsyLgQK1jBw")


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Привет', 'Пока')
    keyboard.row('Расписание ВУЗа')
    chat_id = message.chat.id
    bot.send_message(message.chat.id, 'Привет!', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет!')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Пока!')
    elif message.text == 'Расписание ВУЗа':
        bot.send_message(message.chat.id, 'Введи, пожалуйста, номер группы.\n' +
                         'Например «3630102/80401» для СПбПУ.\n' +
                         'И только потом выбери номер группы.')
        bot.register_next_step_handler(message, abc)

        # # elif message.text == group:
        key = types.InlineKeyboardMarkup()
        but_1 = types.InlineKeyboardButton(text="СПбПУ", callback_data="СПбПУ")
        # but_2 = types.InlineKeyboardButton(text="ГУАП", callback_data="ГУАП")
        key.add(but_1)
        bot.send_message(message.chat.id, text="Какой ВУЗ ты выбираешь, чтобы посмотреть распиание?", reply_markup=key)


@bot.callback_query_handler(func=lambda call: True)
def inline(call):
    bot.register_next_step_handler(call.message, send_text)
    # group = '3630102/80401'; #по идее мы это от пользователя доллжны получить
    group_id = csv1.get_group_id(group)
    print(group_id)

    # if call.data == 'СПбПУ':
    bot.send_message(call.message.chat.id, 'Твой ВУЗ - СПбПУ.')
    key = types.InlineKeyboardMarkup()

    but_1 = types.InlineKeyboardButton(text="Сегодня", callback_data="td_spbstu")
    but_2 = types.InlineKeyboardButton(text="Завтра", callback_data="tw_spbstu")
    but_3 = types.InlineKeyboardButton(text="Эта неделя", callback_data="this_week_spbstu")
    but_4 = types.InlineKeyboardButton(text="Следующая неделя", callback_data="next_week_spbstu")
    but_5 = types.InlineKeyboardButton(text="Ввести свою дату", callback_data="my_spbstu")
    key.add(but_1, but_2, but_3, but_4, but_5)
    bot.send_message(call.message.chat.id, 'Твой ВУЗ - СПбПУ.\nВыбери промежуток:', reply_markup=key)


    # if call.data == 'ГУАП':
    #     # bot.send_message(call.message.chat.id, 'Твой ВУЗ - ГУАП. \n Введи, пожалуйста, номер группы.')
    #     key = types.InlineKeyboardMarkup()
    #     but2_1 = types.InlineKeyboardButton(text="Сегодня", callback_data="td_guap")
    #     but2_2 = types.InlineKeyboardButton(text="Завтра", callback_data="tw_guap")
    #     but2_3 = types.InlineKeyboardButton(text="Эта неделя", callback_data="this_week_guap")
    #     but2_4 = types.InlineKeyboardButton(text="Следующая неделя", callback_data="next_week_guap")
    #     key.add(but2_1, but2_2, but2_3, but2_4)
    #     bot.send_message(call.message.chat.id, 'Твой ВУЗ - ГУАП.\nВыбери промежуток:', reply_markup=key)

    # формирование и вызов даты политех
    if call.data == 'td_spbstu':
        marker = 0
        text = data_day_modifier(marker)
        temp = datetime.strptime(text, '%Y-%m-%d')
        bot.send_message(call.message.chat.id, 'Расписание на сегодня ' +
                         "{}.{}.{}".format(temp.day, temp.month, temp.year) + ':\n\n' + print_shedule(text, group_id))

    if call.data == 'tw_spbstu':
        marker = 1
        text = data_day_modifier(marker)
        temp = datetime.strptime(text, '%Y-%m-%d')
        bot.send_message(call.message.chat.id, 'Расписание на завтра ' +
                         "{}.{}.{}".format(temp.day, temp.month, temp.year) + ':\n\n' + print_shedule(text, group_id))

    if call.data == 'this_week_spbstu':
        day_week = datetime.isoweekday(datetime.today())
        delta = -(day_week - 1)  # чтобы узнать дату пн
        while delta <= 7 - day_week:
            text = data_week_modifier(delta)
            delta += 1
            temp = datetime.strptime(text, '%Y-%m-%d')
            bot.send_message(call.message.chat.id, 'Расписание на текущую неделю ' +
                             "{}.{}.{}".format(temp.day, temp.month, temp.year) + ':\n\n' + print_shedule(text,
                                                                                                          group_id))

    if call.data == 'next_week_spbstu':
        day_week = datetime.isoweekday(datetime.today())
        delta = 7 - day_week + 1  # чтобы узнать дату пн
        while delta <= 6 + day_week:
            text = data_week_modifier(delta)
            delta += 1
            temp = datetime.strptime(text, '%Y-%m-%d')
            bot.send_message(call.message.chat.id, 'Расписание на следующую неделю ' +
                             "{}.{}.{}".format(temp.day, temp.month, temp.year) + ':\n\n' + print_shedule(text,
                                                                                                          group_id))

    if call.data == 'my_spbstu':
        msg = bot.send_message(call.message.chat.id, 'Введите дату в формате YYYY-MM-DD')




def data_day_modifier(marker):
    today = date.today()
    if marker == 0:
        return str(today)
        # return '2021-05-08'

    if marker == 1:  # завтра
        one_day = timedelta(days=2)  # потому что 17.05 нормальное расписание
        return str(today + one_day)
        # return '2021-05-17'


def data_week_modifier(i):
    today = date.today()
    one_day = timedelta(days=i)
    return str(today + one_day)


def print_shedule(text, group_id):
    t = parse_data.get_data(text, '99', group_id)
    return t


def abc(message):
    global group

    group = message.text
    bot.send_message(message.chat.id, 'Твоя группа: ' + group)

    return

bot.polling()
