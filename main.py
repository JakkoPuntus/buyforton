#! /usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
from config import TOKEN, ADMIN_ID, nextAdmin, hello_text, form

bot = telebot.TeleBot(TOKEN, num_threads = 4)

markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
markup_appeal = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
markup_photo = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)

mkp_newproduct = telebot.types.KeyboardButton('Создать новый товар')
mkp_newservice = telebot.types.KeyboardButton('Создать новую услугу')
mkp_support = telebot.types.KeyboardButton('Написать в техподдержку')
mkp_donate = telebot.types.KeyboardButton('Поддержать проект')
mkp_cancel = telebot.types.KeyboardButton('Отменить')
mkp_skip = telebot.types.KeyboardButton('Пропустить')
mkp_vip = telebot.types.KeyboardButton('Купить VIP 💎')

markup.row(mkp_newproduct, mkp_newservice)
markup.row(mkp_donate, mkp_support)
markup_appeal.row(mkp_cancel)
markup_photo.row(mkp_cancel, mkp_skip)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, hello_text, reply_markup = markup)

@bot.message_handler(commands=["ban"])
def ban_user(message):
    bot.kick_chat_member(message.chat.id, message.chat.id)

@bot.message_handler(regexp = "Создать новый товар")
@bot.message_handler(regexp = "Создать новую услугу")
def def_name(message):
    global log
    global name
    global isItItem
    name = str(message.chat.id) + ".txt"
    try:
        log = open(name, "x", encoding = "utf-8")
    except:
        log = open(name, "r+", encoding = "utf-8")
    bot.send_message(message.chat.id, "Пожалуйста введите:", reply_markup = markup_appeal)
    if message.text == "Создать новый товар":
        msg = bot.send_message(message.chat.id, "1. Название товара", reply_markup = markup_appeal)
        isItItem = True
        log.write("#товар \n")
    else:
        msg = bot.send_message(message.chat.id, "1. Название услуги", reply_markup = markup_appeal)
        isItItem = False
        log.write("#услуга \n")

    bot.register_next_step_handler(msg, description)

def description(message):
    global log
    global isItItem
    if message.text == "Отменить":
        bot.send_message(message.chat.id, "Отменено", reply_markup = markup)
    else:
        if isItItem:
            msg = bot.send_message(message.chat.id, "2. Описание  товара", reply_markup = markup_appeal)
        else:
            msg = bot.send_message(message.chat.id, "2. Описание  услуги", reply_markup = markup_appeal)
        log.write("Название: " + message.text + "\n")
        bot.register_next_step_handler(msg, price)

def price(message):
    global log
    global isItItem
    if message.text == "Отменить":
        bot.send_message(message.chat.id, "Отменено", reply_markup = markup)
    else:
        if isItItem:
            msg = bot.send_message(message.chat.id, "3. Цена товара", reply_markup = markup_appeal)
        else:
            msg = bot.send_message(message.chat.id, "3. Цена услуги", reply_markup = markup_appeal)
        log.write("Описание: " + message.text + "\n")
        if isItItem:
            bot.register_next_step_handler(msg, delivery)
        else:
            bot.register_next_step_handler(msg, city)

def delivery(message):
    global log
    global isItItem
    if message.text == "Отменить":
        bot.send_message(message.chat.id, "Отменено", reply_markup = markup)
    else:
        log.write("Цена: " + message.text + "\n")
        msg = bot.send_message(message.chat.id, "4.Доставка по РБ (цена и условия)", reply_markup = markup_appeal)
        bot.register_next_step_handler(msg, seller)

def city(message):
    global log
    
    if message.text == "Отменить":
        bot.send_message(message.chat.id, "Отменено", reply_markup = markup)
    else:
        log.write("Цена: " + message.text + "\n")
        msg = bot.send_message(message.chat.id, "4. Ваш город", reply_markup = markup_appeal)
        bot.register_next_step_handler(msg, seller)
        
def seller(message):
    global log
    if message.text == "Отменить":
        bot.send_message(message.chat.id, "Отменено", reply_markup = markup)
    else:
        if isItItem:
            log.write("Доставка: " + message.text + "\n")
        else:
            log.write("Город: " + message.text + "\n")
        msg = bot.send_message(message.chat.id, "5. Ваш никнейм в телеграме (в формате @username)", reply_markup = markup_appeal)
        bot.register_next_step_handler(msg, image)

def image(message):
    global log
    global isItItem
    if message.text == "Отменить":
        bot.send_message(message.chat.id, "Отменено", reply_markup = markup)
    else:
        log.write("Продавец: " + message.text + "\n")
        msg = bot.send_message(message.chat.id, "6. Фото", reply_markup = markup_photo)
        log.close()
        bot.register_next_step_handler(msg, finishing)

def finishing(message):
    global log
    global name
   
    
    if message.text == "Отменить":
        bot.send_message(message.chat.id, "Отменено", reply_markup = markup)
    else:
        loger = open(name, "r", encoding = "utf-8")
        appeal = loger.read()
        try:
            if message.text == "Пропустить":
                bot.send_message(ADMIN_ID, appeal)
            else:
                bot.send_photo(ADMIN_ID, message.photo[1].file_id,appeal)
            bot.send_message(message.chat.id, "Заявка отправлена на модерацию", reply_markup=markup)
        except:
            msg = bot.send_message(message.chat.id, "Упс, попробуйте ещё раз", reply_markup=markup_appeal)
            bot.register_next_step_handler(msg, finishing)
        try:
            if message.text == "Пропустить":
                bot.send_message(nextAdmin, appeal)
            else:
                bot.send_photo(nextAdmin , message.photo[1].file_id,appeal)
            
        except Exception as e:
            print("blya")
            print(e)

            



bot.enable_save_next_step_handlers(delay = 2)
bot.load_next_step_handlers()

@bot.message_handler(regexp = "Написать в техподдержку")
def support_first(message):
    msg = bot.send_message(message.chat.id, "Задайте свой вопрос модераторам", reply_markup = markup_appeal)
    bot.register_next_step_handler(msg, support)

def support(message):
    if message.text == "Отменить":
        bot.send_message(message.chat.id, "отменено", reply_markup = markup)
    else:
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        bot.forward_message(nextAdmin, message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "Ваше обращение принято, мы вам ответим", reply_markup = markup)

@bot.message_handler(regexp = "Поддержать проект")
def donate(message):
    photo = open("img/qr_vip.png", "rb")
    bot.send_photo(message.chat.id, photo, "Отправьте TON по адресу: 0:662c32971dbe7d21d71eee8e3f2a0bf8adb73521ee3779090a4910b7742b0b2f или отсканируйте QR код")
    
@bot.message_handler(regexp = "Купить VIP 💎")
def buy_vip(message):
    photo = open("img/qr_vip.png", "rb")
    bot.send_photo(message.chat.id, photo, "Чтобы приобрести VIP, отправьте n TON по адресу: 0:662c32971dbe7d21d71eee8e3f2a0bf8adb73521ee3779090a4910b7742b0b2f или отсканируйте QR код (QR пока не тот)")

@bot.message_handler(content_types = ["text"])
def repeat_all_messages(message):
    if message.chat.id == ADMIN_ID:
        try:
            print(message.reply_to_message.message_id)
            bot.send_message(message.reply_to_message.chat.id, message.text,  reply_markup = markup)
        except Exception as e:
            print(e)





if __name__ == "__main__":
    try: 
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        pass