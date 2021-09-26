import telebot
from telebot import types
import parse_data
from datetime import date, datetime, timedelta
from data_base_spbpu.read_csv import *


bot = telebot.TeleBot("1786082801:AAEOePWM3kTbgLDALmK-6m46RsyLgQK1jBw")
group_id = 34578
group = '5030102/80401'
name_institute = 'fm'
code_institute = 124


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Привет', 'Пока')
    keyboard.row('Узнать рассписание')
    chat_id = message.chat.id
    bot.send_message(message.chat.id, 'Привет!', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет!')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Пока!')
    elif message.text == 'Узнать рассписание':
        choose_institute(message)
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю, выбери, пожалуйста, пункт из меню')


def choose_institute(message):
    key = types.InlineKeyboardMarkup()

    but_1 = types.InlineKeyboardButton(text="ИКЗИ", callback_data="ikzi")
    but_2 = types.InlineKeyboardButton(text="Физ-Мех", callback_data="fm")
    but_3 = types.InlineKeyboardButton(text="ИФНиТ", callback_data="ifnit")
    but_4 = types.InlineKeyboardButton(text="ИБСБ", callback_data="ibsb")
    but_5 = types.InlineKeyboardButton(text="ИЭ", callback_data="ie")
    but_6 = types.InlineKeyboardButton(text="ИПМЭиТ", callback_data="ipmeit")
    but_7 = types.InlineKeyboardButton(text="ИКНТ", callback_data="iknt")
    but_8 = types.InlineKeyboardButton(text="ИММиТ", callback_data="immit")
    but_9 = types.InlineKeyboardButton(text="ИСИ", callback_data="isi")
    but_10 = types.InlineKeyboardButton(text="ГИ", callback_data="gi")

    key.add(but_1, but_2, but_3, but_4, but_5, but_6, but_7, but_8, but_9, but_10)

    bot.send_message(message.chat.id, 'Выбери институт:', reply_markup=key)


@bot.callback_query_handler(func=lambda call: True)
def callback_institute(call):
    code_institute = 0
    if call.data == "ikzi":
        name_institute = "ikzi"
        code_institute = 122
        bot.send_message(call.message.chat.id, 'Твой институт: ИКЗИ')
    if call.data == "fm":
        name_institute = 'fm'
        code_institute = 124
        bot.send_message(call.message.chat.id, 'Твой институт: Физ-Мех')
    if call.data == "ifnit":
        name_institute = 'ifnit'
        code_institute = 98
        bot.send_message(call.message.chat.id, 'Твой институт: ИФНиТ')
    if call.data == "ibsb":
        name_institute = 'ibsb'
        code_institute = 119
        bot.send_message(call.message.chat.id, 'Твой институт: ИБСБ')
    if call.data == "ie":
        name_institute = 'ie'
        code_institute = 93
        bot.send_message(call.message.chat.id, 'Твой институт: ИЭ')
    if call.data == "ipmeit":
        name_institute = 'ipmeit'
        code_institute = 100
        bot.send_message(call.message.chat.id, 'Твой институт: ИПМЭиТ')
    if call.data == "iknt":
        name_institute = 'iknt'
        code_institute = 95
        bot.send_message(call.message.chat.id, 'Твой институт: ИКНТ')
    if call.data == "immit":
        name_institute = 'immit'
        code_institute = 94
        bot.send_message(call.message.chat.id, 'Твой институт: ИММиТ')
    if call.data == "isi":
        name_institute = 'isi'
        code_institute = 92
        bot.send_message(call.message.chat.id, 'Твой институт: ИСИ')
    if call.data == 'gi':
        name_institute = 'gi'
        code_institute = 101
        bot.send_message(call.message.chat.id, 'Твой институт: ГИ')
    bot.send_message(call.message.chat.id, 'Введи, пожалуйста, номер группы.\n' +
                     'Например «5030102/80401».')
    bot.register_next_step_handler(call.message, choose_group)


def data_day_modifier(marker):
    today = date.today()
    if marker == 0:
        return str(today)

    if marker == 1:  # завтра
        one_day = timedelta(days=2)
        return str(today + one_day)


def data_week_modifier(i):
    today = date.today()
    one_day = timedelta(days=i)
    return str(today + one_day)


def print_link(text, group_id, code_institute):
    t = parse_data.get_data(text, str(code_institute), group_id)
    return t


@bot.message_handler(content_types=['text'])
def choose_group(message):
    group = message.text
    bot.send_message(message.chat.id, 'Твоя группа: ' + group)
    group_id = get_group_id(group, name_institute)
    if group_id != 0:
        marker = 0
        text = data_day_modifier(marker)
        temp = datetime.strptime(text, '%Y-%m-%d')
        bot.send_message(message.chat.id,
                         'Расписание на текущую неделю\n' + print_link(text, group_id, code_institute))


bot.polling()
