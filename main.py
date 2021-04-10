#! /usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
import markups
import regexps
import transaction_checker
import pymysql.cursors
import config
import withdraw
import logging
from config import TOKEN, ADMIN_ID, nextAdmin, hello_text, TON_ADRESS, admins_list
import os

bot = telebot.TeleBot(TOKEN, num_threads=4, parse_mode="HTML")
logging.basicConfig(level=logging.DEBUG)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    buying = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="9R3BhW049TF6",
        database="buyforton",
        cursorclass=pymysql.cursors.DictCursor
    )
    if message.text == "/start":
        bot.send_message(message.chat.id, hello_text,
                         reply_markup=markups.main)
    else:
        buy_id = message.text.replace("/start ", "")
        try:
            with connection:

                with connection.cursor() as cursor:
                    # Read a single record
                    sql = "SELECT `nickname`, `chat_id`, `quantity` FROM `buyforton_appeals` WHERE `message_id`=%s"
                    cursor.execute(sql, (buy_id))
                    result = cursor.fetchone()
            quantity = result['quantity']
            if quantity != 0:
                buy_message = "Вы выбрали товар №{res}\n Перед тем, как оплатить его, обязательно свяжитесь с продавцом <a href=\"tg://user?id={id}\">{nickname}</a> и договоритесь об условиях доставки.\n Настоятельно не рекомендуем оплачивать товар до связи продавцом, ровно как и оплачивать товар напрямую у продавца. В этих случая мы не сможем гарантироать успешность сделки.".format(
                    res=buy_id, id=result['chat_id'], nickname=result['nickname']
                )
                buying.row("Оплатить " + str(buy_id))
                bot.send_message(message.chat.id, buy_message,
                                 reply_markup=buying)
            else:
                bot.send_message(
                    message.chat.id, "К сожалению, этот товар уже распродан, и мы не успели его удалить.", reply_markup=markups.main)
        except Exception as e:
            bot.send_message(message.chat.id, str(buy_id), reply_markup=buying)
            print(e)


@bot.message_handler(commands=["ban"])
def ban_user(message):
    bot.send_message(
        message.chat.id, '<a href="tg://user?id=564941525">Текст ссылки</a>')


@bot.message_handler(commands=["accept"])
def acception(message):
    try:
        if message.chat.id in config.admins_list:
            inline = message.reply_to_message.reply_markup
            new_channel = None
            if message.text.find("!") != -1:
                index = message.text.index("!")+1
                new_category = message.text[index:]
                new_category = new_category.replace(" ", "")

            try:
                channel_to_send = "dmth"
                if message.reply_to_message.text != None:
                    for i in message.reply_to_message.text.split("\n"):
                        if "Категория:" in i:
                            channel_to_send = i
                            print(channel_to_send)
                elif message.reply_to_message.caption != None:
                    for i in message.reply_to_message.caption.split("\n"):
                        if "Категория:" in i:
                            channel_to_send = i
                if message.text.find('!') != -1:
                    index = message.text.index("!")+1
                    new_channel = message.text[index:]
                    new_channel = new_channel.replace(" ", "")

                    try:
                        a = "Категория: " + \
                            message.reply_to_message.text.replace(
                                channel_to_send, config.commands[new_channel])
                        print(a)
                        bot.edit_message_text(
                            a,
                            message.chat.id,
                            message.reply_to_message.id,
                            reply_markup=inline
                        )
                    except:
                        a = message.reply_to_message.caption.replace(
                            channel_to_send, config.commands[new_channel])

                        print(a)
                        bot.edit_message_caption(
                            a,
                            message.chat.id,
                            message.reply_to_message.id,
                            reply_markup=inline
                        )
                channel_to_send = channel_to_send.replace('Категория: ', '')
                if new_channel != None:
                    channel_to_send = config.commands[new_channel]
                    channel_to_send = channel_to_send.replace('Категория: ', '')
                print(channel_to_send)
                print(config.categories[channel_to_send])
                print()
                try:
                    bot.send_message(
                        config.categories[channel_to_send], message.reply_to_message.text, reply_markup=inline)
                except:
                    photo = message.reply_to_message.photo[1].file_id
                    print(message.reply_to_message.text)
                    bot.send_photo(config.categories[channel_to_send], photo,
                                message.reply_to_message.caption, reply_markup=inline)

            except Exception as e:
                print(e)
        else:
            bot.send_message(message.chat.id, "Вы не админ")
    except Exception as e:
        bot.send_message(message.chat.id, e, reply_markup = markups.main)


@bot.message_handler(regexp=regexps.newproduct)
@bot.message_handler(regexp=regexps.newservice)
def def_category(message):
    global log
    global name
    global isItItem
    name = str(message.chat.id) + ".txt"

    try:
        log = open(name, "x+", encoding="utf-8")
    except:
        log = open(name, "r+", encoding="utf-8")
        log.truncate(0)

    if message.text == regexps.newproduct:
        msg = bot.send_message(
            message.chat.id, "Пожалуйста, выберите категорию товара",
            reply_markup=markups.categories
        )
        isItItem = True
        log.write("#товар \n")
    else:
        msg = bot.send_message(
            message.chat.id, "Пожалуйста, выберите категорию услуги:", reply_markup=markups.categories_service
        )
        isItItem = False
        log.write("#услуга \n")
    bot.register_next_step_handler(msg, def_name)


def def_name(message):
    global log
    global name
    global isItItem
    try:
        if message.text in config.categories and message.text != '💵💎Оплата за TON' and message.text != '🤝Прочие услуги':
            msg = bot.send_message(
                message.chat.id, "1. Название товара", reply_markup=markups.appeal
            )
            isItItem = True
            log.write("Категория: " + message.text + "\n")
        else:
            msg = bot.send_message(
                message.chat.id, "1. Название услуги", reply_markup=markups.appeal
            )
            isItItem = False
            log.write("Категория: " + message.text + "\n")
    except Exception as e:
        print(e)
    bot.register_next_step_handler(msg, description)


def description(message):
    global log
    global isItItem
    global itemName
    itemName = message.text

    if message.text == regexps.cancel:
        bot.send_message(message.chat.id, "Отменено",
                         reply_markup=markups.main)
    else:
        if isItItem:
            msg = bot.send_message(
                message.chat.id, "2. Описание  товара  (до 1000 символов)", reply_markup=markups.appeal
            )
        else:
            msg = bot.send_message(
                message.chat.id, "2. Описание  услуги  (до 1000 символов)", reply_markup=markups.appeal
            )
        log.write("Название: " + message.text + "\n")
        bot.register_next_step_handler(msg, def_price)


def def_price(message):
    global log
    global isItItem
    if message.text == regexps.cancel:
        bot.send_message(message.chat.id, "Отменено",
                         reply_markup=markups.main)
    else:
        if len(message.text) > 1000:
            msg = bot.send_message(message.chat.id, "Пожалуйста, поменьше букв")
            bot.register_next_step_handler(msg, def_price)
        else:
            if isItItem:
                msg = bot.send_message(
                    message.chat.id,
                    "3. Цена товара в TON (только число, минимум 2)",
                    reply_markup=markups.appeal,
                )
            else:
                msg = bot.send_message(
                    message.chat.id,
                    "3. Цена услуги в TON (только число, минимум 2)",
                    reply_markup=markups.appeal,
                )
            log.write("Описание: " + message.text + "\n")
            bot.register_next_step_handler(msg, quantity_def)


def quantity_def(message):
    global log
    global isItItem
    global price
    price = message.text
    if message.text == regexps.cancel:
        bot.send_message(message.chat.id, "Отменено",
                         reply_markup=markups.main)
    else:
        try:
            float(price)
            if float(price) < 2:
                msg = bot.send_message(
                    message.chat.id, "Минимум 2!", reply_markup=markups.appeal)
                bot.register_next_step_handler(msg, quantity)
            else:
                log.write("Цена: " + message.text + "💎\n")
                if isItItem:
                    msg = bot.send_message(
                        message.chat.id, '4. Сколько товаров вы хотите продать (только число)', reply_markup=markups.appeal)
                    bot.register_next_step_handler(msg, delivery)
                else:
                    msg = bot.send_message(message.chat.id, '4. Ваша услуга:',
                                           reply_markup=markups.isServiceReusable)
                    bot.register_next_step_handler(msg, city)
        except Exception as e:
            msg = bot.send_message(
                message.chat.id, "Неверный формат, необходимо ввести число. Введите ещё раз.", reply_markup=markups.appeal)
            bot.register_next_step_handler(msg, quantity_def)
            print(e)


def delivery(message):
    global log
    global quantity
    if message.text == regexps.cancel:
        bot.send_message(message.chat.id, "Отменено",
                         reply_markup=markups.main)
    else:
        quantity = message.text
        try:
            int(quantity)
            if quantity == 0:
                msg = bot.send_message(
                    message.chat.id, "Неверный формат, необходимо ввести натуральное число. Введите ещё раз.", reply_markup=markups.appeal)
                bot.register_next_step_handler(msg, delivery)
            else:
                msg = bot.send_message(
                    message.chat.id, '5. Доставка по РБ (цена и условия)', reply_markup=markups.appeal)
                bot.register_next_step_handler(msg, TON_wallet)

        except:
            msg = bot.send_message(
                message.chat.id, "Неверный формат, необходимо ввести натуральное число. Введите ещё раз.", reply_markup=markups.appeal)
            bot.register_next_step_handler(msg, delivery)


def city(message):
    global log
    global isItItem
    global quantity
    if message.text == regexps.cancel:
        bot.send_message(message.chat.id, "Отменено",
                         reply_markup=markups.main)
    else:
        quantity = message.text
        
        if quantity != "Многоразовая" and quantity != 'Одноразовая':
            msg = bot.send_message(
                message.chat.id, "Не балуйся! Выбери еще раз.", reply_markup=markups.isServiceReusable)
            bot.register_next_step_handler(msg, city)
        elif quantity == "Многоразовая":
            quantity = 1024
            msg = bot.send_message(message.chat.id, '5. Город')
            bot.register_next_step_handler(msg, guarantee)
        elif quantity == "Одноразовая":
            quantity = 1
            msg = bot.send_message(message.chat.id, '5. Город')
            bot.register_next_step_handler(msg, guarantee)


def guarantee(message):
    global isItItem
    grnt = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    grnt_yes = telebot.types.KeyboardButton("Да")
    grnt_no = telebot.types.KeyboardButton("Нет")

    grnt.row(grnt_yes, grnt_no)
    grnt.row(markups.cancel)

    if message.text == regexps.cancel:
        bot.send_message(message.chat.id, "Отменено",
                         reply_markup=markups.main)
    else:
        if isItItem:
            log.write("Доставка: " + message.text + "\n")
        else:
            log.write("Город: " + message.text + "\n")
        msg = bot.send_message(
            message.chat.id,
            "6. Использовать гаранта?",
            reply_markup=grnt,
        )
        bot.register_next_step_handler(msg, TON_wallet)


def TON_wallet(message):
    global log
    global isItItem
    global isGuaranteed
    if message.text == regexps.cancel:
        bot.send_message(message.chat.id, "Отменено",
                         reply_markup=markups.main)
    else:
        if isItItem:
            log.write("Доставка: " + message.text + "\n")
        else:
            log.write("Город: " + message.text + "\n")
        try:
            log.write('Продавец: <a href="tg://user?id=' + str(message.chat.id) +
                        '">' + message.from_user.first_name + '</a> \n')
        except:
            log.write("Продавец: публичное имя скрыто \n")
        if isItItem == True:
            msg = bot.send_message(
                message.chat.id,
                "7. Адрес вашего TON кошелька",
                reply_markup=markups.appeal,
            )
            isGuaranteed = True
            bot.register_next_step_handler(msg, image)
        else:
            if message.text == "Нет" or message.text == "нет":
                isGuaranteed = False
                msg = bot.send_message(
                    message.chat.id, "7. Фото", reply_markup=markups.photo)
                log.close()
                bot.register_next_step_handler(
                    msg, finishing, wallet="none")
            else:
                isGuaranteed = True
                msg = bot.send_message(
                    message.chat.id,
                    "7. Адрес вашего TON кошелька",
                    reply_markup=markups.appeal,
                )
                bot.register_next_step_handler(msg, image)


def image(message):
    global log
    global isItItem
    if message.text == regexps.cancel:
        bot.send_message(message.chat.id, "Отменено",
                         reply_markup=markups.main)
    else:
        msg = bot.send_message(message.chat.id, "Фото",
                               reply_markup=markups.photo)
        log.close()
        bot.register_next_step_handler(msg, finishing, wallet=message.text)


def finishing(message, wallet):
    global log
    global price
    global isGuaranteed
    global isItItem
    global quantity

    if isItItem:
        item_type = "item"
    else:
        item_type = "service"

    url = "t.me/buyforton_bot?start=" + str(message.message_id)
    if isGuaranteed:
        inline = telebot.types.InlineKeyboardMarkup()
        appeal_btn = telebot.types.InlineKeyboardButton(text="Купить", url=url)
        inline.add(appeal_btn)
    else:
        inline = None

    if message.text == regexps.cancel:
        bot.send_message(message.chat.id, "Отменено",
                         reply_markup=markups.main)
    else:
        loger = open(name, "r", encoding="utf-8")
        appeal = loger.read()
        try:
            if message.text == "Пропустить":
                bot.send_message(ADMIN_ID, appeal, reply_markup=inline)
            else:
                bot.send_photo(
                    ADMIN_ID, message.photo[1].file_id, appeal, reply_markup=inline
                )
            bot.send_message(
                message.chat.id,
                "Заявка отправлена на модерацию",
                reply_markup=markups.main,
            )
        except:
            msg = bot.send_message(
                message.chat.id, "Упс, попробуйте ещё раз", reply_markup=markups.appeal
            )
            bot.register_next_step_handler(msg, finishing)
        try:
            if message.text == "Пропустить":
                bot.send_message(nextAdmin, appeal, reply_markup=inline)
            else:
                bot.send_photo(
                    nextAdmin, message.photo[1].file_id, appeal, reply_markup=inline)
        except Exception as e:
            print(e)
        print

        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="9R3BhW049TF6",
            database="buyforton",
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `buyforton_appeals` (`message_id`, `nickname`, `chat_id`, `price`, `name`, `wallet`, `type`, `quantity`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(
                    sql,
                    (
                        message.message_id,
                        message.from_user.first_name,
                        message.chat.id,
                        price,
                        itemName,
                        wallet,
                        item_type,
                        quantity
                    )
                )
            connection.commit()


@bot.message_handler(regexp=regexps.support)
def support_first(message):
    msg = bot.send_message(
        message.chat.id, "Задайте свой вопрос модераторам", reply_markup=markups.appeal
    )
    bot.register_next_step_handler(msg, support)


def support(message):
    if message.text == regexps.cancel:
        bot.send_message(message.chat.id, "отменено",
                         reply_markup=markups.main)
    else:
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        bot.forward_message(nextAdmin, message.chat.id, message.message_id)
        bot.send_message(
            message.chat.id,
            "Ваше обращение принято, мы вам ответим",
            reply_markup=markups.main,
        )


@bot.message_handler(regexp=regexps.donate)
def donate(message):
    photo = open("img/qr_vip.png", "rb")
    bot.send_photo(
        message.chat.id,
        photo,
        "Отправьте TON по адресу: 0:d013df48b33ff5479357b651499846eda4db2a3bac3d1926def3693403192d59 или отсканируйте QR код",
    )


@bot.message_handler(regexp=regexps.vip)
def buy_vip(message):
    photo = open("img/qr_vip.png", "rb")
    bot.send_photo(
        message.chat.id,
        photo,
        "Чтобы приобрести VIP, отправьте n TON по адресу: "
        + TON_ADRESS
        + " или отсканируйте QR код (QR пока не тот)",
    )


@bot.callback_query_handler(func=lambda message: message.data == "back")
@bot.message_handler(regexp=regexps.shopcart)
def shopcart(message):
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="9R3BhW049TF6",
        database="buyforton",
        cursorclass=pymysql.cursors.DictCursor
    )
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT `message_id` FROM `shopwheels` WHERE `user_id`=%s"
            cursor.execute(sql, (message.from_user.id))
            result = cursor.fetchall()
    print(type(result))
    shpwl_markup = telebot.types.InlineKeyboardMarkup()
    if len(result) != 0:
        for i in tuple(result):
            btn = telebot.types.InlineKeyboardButton(
                text="Заказ номер " + str(i["message_id"]),
                callback_data="order" + str(i["message_id"]),
            )
            shpwl_markup.row(btn)
        try:
            bot.send_message(
                message.chat.id, "Список ваших активных заказов", reply_markup=shpwl_markup
            )
        except:
            bot.edit_message_text(
                "Список ваших активных заказов",
                message.message.chat.id,
                message.message.id,
                reply_markup=shpwl_markup
            )

    else:
        bot.send_message(message.chat.id, "Пусто", reply_markup=shpwl_markup)


@bot.callback_query_handler(func=lambda c: c.data.find("order") != -1)
def show_order(c):
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="9R3BhW049TF6",
        database="buyforton",
        cursorclass=pymysql.cursors.DictCursor
    )
    buy_id = c.data
    buy_id = buy_id.replace("order", "")
    with connection:
        with connection.cursor() as cursor:
            # Read a single record
            sql = (
                "SELECT `price`, `name` FROM `buyforton_appeals` WHERE `message_id`=%s"
            )
            cursor.execute(sql, (buy_id))
            result = cursor.fetchone()

    order = telebot.types.InlineKeyboardMarkup()
    confirm = telebot.types.InlineKeyboardButton(
        "Подтвердить получение заказа", callback_data="confirm" + str(buy_id))
    order.row(confirm)
    order.row(markups.back)
    try:
        bot.edit_message_text(
            "ЗАКАЗ " + str(result["name"]) + " ценой " +
            str(result["price"]) + " TON",
            c.message.chat.id,
            c.message.id,
            reply_markup=order
        )
    except:
        bot.send_message(c.message.chat.id, "Хватит баловаться",
                         reply_markup=markups.main)
    print(result)


@bot.callback_query_handler(func=lambda c: c.data.find("confirm") != -1)
def send_money(c):
    bot.send_message(
        c.message.chat.id, "Деньги скоро будут отправлены продавцу. Спасибо, что пользуетесь BUYFORTON")
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="9R3BhW049TF6",
        database="buyforton",
        cursorclass=pymysql.cursors.DictCursor
    )
    buy_id = c.data.replace('confirm', '')
    with connection:
        with connection.cursor() as cursor:
            # Read a single record
            sql = (
                "SELECT `wallet`, `price` FROM `buyforton_appeals` WHERE `message_id`=%s"
            )
            cursor.execute(sql, (buy_id))
            result = cursor.fetchone()
        with connection.cursor() as cursor:
            # Read a single record
            sql = (
                "DELETE FROM `buyforton_appeals` WHERE `message_id` = %s"
            )
            cursor.execute(sql, (buy_id))
        with connection.cursor() as cursor:
            # Read a single record
            sql = (
                "DELETE FROM `shopwheels` WHERE `message_id` = %s"
            )
            cursor.execute(sql, (buy_id))
        connection.commit()

    bot.send_message(c.message.chat.id,
                     result['wallet'] + " " + str(result['price']))
    if result["price"] * 0.03 < 0.5:
        withdraw.send_ton(result['wallet'], result['price'] - 0.4)
    else:
        withdraw.send_ton(result['wallet'],
                          result['price'] - result['price'] * 0.03)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):

    if message.text == "Отменить":
        bot.send_message(message.chat.id, "Отменено",
                         reply_markup=markups.main)
    else:

        if message.text.find("Оплатить") != -1:
            global buy_id
            global price
            buy_id = int(message.text.replace("Оплатить ", ""))
            connection = pymysql.connect(
                host="localhost",
                user="root",
                password="9R3BhW049TF6",
                database="buyforton",
                cursorclass=pymysql.cursors.DictCursor
            )
            with connection:
                with connection.cursor() as cursor:
                    # Read a single record
                    sql = "SELECT `price` FROM `buyforton_appeals` WHERE `message_id`=%s"
                    cursor.execute(sql, (buy_id))
                    result = cursor.fetchone()
                price = result["price"]

                msg = bot.send_message(
                    message.chat.id,
                    "Переведите {price} тон на следующий кошелек: ".format(
                        price=price)
                    + TON_ADRESS
                    + " с комментарием «kuna-2gs4kaytt5» и нажмите «Подтвердить». Перед отправкой советуем ознакомиться с руководством по ссылке \n https://telegra.ph/BUYFORTON-Oplata-03-04",
                    reply_markup=markups.transaction,
                )
                bot.register_next_step_handler(msg, confirmation)
        elif message.chat.id == ADMIN_ID:
            try:
                bot.send_message(
                    message.reply_to_message.chat.id,
                    message.text,
                    reply_markup=markups.main,
                )
            except Exception as e:
                print(e)


def confirmation(message):
    if message.text == "Отменить":
        bot.send_message(message.chat.id, "Отменено",
                         reply_markup=markups.main)
    else:
        try:
            msg = bot.send_message(
                message.chat.id, "Отправьте id транзакции", reply_markup=markups.transaction
            )
            bot.register_next_step_handler(msg, confirmation_second)
        except Exception as e:
            print(e)
            bot.send_message(message.chat.id, "Something went wrong: ")


def confirmation_second(message):
    global buy_id
    global price
    global name

    bot.send_message(message.chat.id, "Транзакция проверяется...")

    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="9R3BhW049TF6",
        database="buyforton",
        cursorclass=pymysql.cursors.DictCursor
    )

    tr_chk = transaction_checker.check_transaction(message.text)
    try:
        msg_chk = transaction_checker.check_message(
            tr_chk["transactions"][0]["out_msgs"][0]
        )

        if (
            tr_chk["transactions"][0]["status"] == 3
            and msg_chk["messages"][0]["dst"] == TON_ADRESS
            and tr_chk["transactions"][0]["balance_delta"] <= config.float_to_hex(price)
        ):

            with connection:
                with connection.cursor() as cursor:
                    # Read a single record
                    sql = "SELECT `chat_id`, `price`, `nickname` FROM `buyforton_appeals` WHERE `message_id`=%s"
                    cursor.execute(sql, (buy_id))
                    result = cursor.fetchone()
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `shopwheels` (`message_id`, `user_id`, `seller_id`) VALUES (%s, %s, %s)"
                    cursor.execute(
                        sql, (buy_id, message.chat.id, result["chat_id"]))
                with connection.cursor() as cursor:
                    sql = "UPDATE `quantity` = `quantity` - 1 WHERE `message_id` = %s"
                    cursor.execute(sql, (buy_id))
                    result_another = cursor.fetchone()
                connection.commit()
            bot.send_message(
                result["chat_id"],
                'Ваш товар ценой {price} TON оплачен юзером <a href="tg://user?id={chat_id}">{nickname}</a> '.format(
                    price=result["price"], chat_id=result["chat_id"], nickname=result["nickname"]),
                reply_markup=markups.main
            )
            bot.send_message(ADMIN_ID, "Удали из канала заказ " + str(buy_id))
            for i in admins_list:
                bot.send_message(i, "Удали из канала заказ " + str(buy_id))
            bot.send_message(
                message.chat.id, "Операция прошла успешно", reply_markup=markups.main
            )
            if result_another['quantity'] == 0:
                bot.send_message(ADMIN_ID, "удалить " + str(buy_id))
        else:
            msg = bot.send_message(
                message.chat.id, "Что-то пошло не так", reply_markup=markups.transaction
            )
            bot.register_next_step_handler(msg, confirmation)
    except:
        msg = bot.send_message(
            message.chat.id, "Что-то пошло не так. Отправьте id транзакции еще раз.", reply_markup=markups.transaction
        )
        bot.register_next_step_handler(msg, confirmation_second)


if __name__ == "__main__":
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(e)
        pass
