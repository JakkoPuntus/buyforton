#! /usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
import markups
import regexps
import transaction_checker
import pymysql.cursors
import config

import logging
from config import TOKEN, ADMIN_ID, nextAdmin, hello_text, TON_ADRESS
import logging

bot = telebot.TeleBot(TOKEN, num_threads=4)
logging.basicConfig(level=logging.DEBUG)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):

    connection = pymysql.connect(
        host="localhost",
        user="root",
        database="buyforton",
        cursorclass=pymysql.cursors.DictCursor,
    )
    if message.text == "/start":
        bot.send_message(message.chat.id, hello_text, reply_markup=markups.main)
    else:
        buy_id = message.text.replace("/start ", "")
        try:
            with connection:

                with connection.cursor() as cursor:
                    # Read a single record
                    sql = "SELECT `nickname` FROM `buyforton_appeals` WHERE `message_id`=%s"
                    cursor.execute(sql, (buy_id))
                    result = cursor.fetchone()
            buy_message = "Вы выбрали товар №{res} \n Перед тем, как оплатить его, обязательно свяжитесь с продавцом @{nickname} и договоритесь об условиях доставки. \n Настоятельно не рекомендуем оплачивать товар до связи продавцом, ровно как и оплачивать товар напрямую у продавца. В этих случая мы не сможем гарантироать успешность сделки.".format(
                res=buy_id, nickname=result["nickname"]
            )
            markups.buying.row("Оплатить " + str(buy_id))
            bot.send_message(message.chat.id, buy_message, reply_markup=markups.buying)
        except Exception as e:
            bot.send_message(message.chat.id, str(buy_id), reply_markup=markups.buying)
            print(e)


@bot.message_handler(commands=["ban"])
def ban_user(message):
    bot.kick_chat_member(message.chat.id, message.chat.id)


@bot.message_handler(regexp=regexps.newproduct)
@bot.message_handler(regexp=regexps.newservice)
def def_name(message):
    global log
    global name
    global isItItem
    name = str(message.chat.id) + ".txt"
    try:
        log = open(name, "x", encoding="utf-8")
    except:
        log = open(name, "r+", encoding="utf-8")
    bot.send_message(
        message.chat.id, "Пожалуйста введите:", reply_markup=markups.appeal
    )
    if message.text == regexps.newproduct:
        msg = bot.send_message(
            message.chat.id, "1. Название товара", reply_markup=markups.appeal
        )
        isItItem = True
        log.write("#товар \n")
    else:
        msg = bot.send_message(
            message.chat.id, "1. Название услуги", reply_markup=markups.appeal
        )
        isItItem = False
        log.write("#услуга \n")
    bot.register_next_step_handler(msg, description)


def description(message):
    global log
    global isItItem
    global itemName
    itemName = message.text

    if message.text == regexps.cancel:
        bot.send_message(message.chat.id, "Отменено", reply_markup=markups.main)
    else:
        if isItItem:
            msg = bot.send_message(
                message.chat.id, "2. Описание  товара", reply_markup=markups.appeal
            )
        else:
            msg = bot.send_message(
                message.chat.id, "2. Описание  услуги", reply_markup=markups.appeal
            )
        log.write("Название: " + message.text + "\n")
        bot.register_next_step_handler(msg, price)


def price(message):
    global log
    global isItItem
    if message.text == regexps.cancel:
        bot.send_message(message.chat.id, "Отменено", reply_markup=markups.main)
    else:
        if isItItem:
            msg = bot.send_message(
                message.chat.id,
                "3. Цена товара в TON (только число)",
                reply_markup=markups.appeal,
            )
        else:
            msg = bot.send_message(
                message.chat.id,
                "3. Цена услуги в TON (только число)",
                reply_markup=markups.appeal,
            )
        log.write("Описание: " + message.text + "\n")
        if isItItem:
            bot.register_next_step_handler(msg, delivery)
        else:
            bot.register_next_step_handler(msg, city)


def delivery(message):
    global log
    global isItItem
    global price
    price = message.text
    if message.text == regexps.cancel:
        bot.send_message(message.chat.id, "Отменено", reply_markup=markups.main)
    else:
        log.write("Цена: " + message.text + "\n")
        msg = bot.send_message(
            message.chat.id,
            "4.Доставка по РБ (цена и условия)",
            reply_markup=markups.appeal,
        )
        bot.register_next_step_handler(msg, seller)


def city(message):
    global log

    if message.text == regexps.cancel:
        bot.send_message(message.chat.id, "Отменено", reply_markup=markups.main)
    else:
        log.write("Цена: " + message.text + "\n")
        msg = bot.send_message(
            message.chat.id, "4. Ваш город", reply_markup=markups.appeal
        )
        bot.register_next_step_handler(msg, seller)


def seller(message):
    global log
    if message.text == regexps.cancel:
        bot.send_message(message.chat.id, "Отменено", reply_markup=markups.main)
    else:
        if isItItem:
            log.write("Доставка: " + message.text + "\n")
        else:
            log.write("Город: " + message.text + "\n")
        msg = bot.send_message(
            message.chat.id,
            "5. Ваш никнейм в телеграме (в формате @username)",
            reply_markup=markups.appeal,
        )
        bot.register_next_step_handler(msg, image)


def image(message):
    global log
    global isItItem
    if message.text == regexps.cancel:
        bot.send_message(message.chat.id, "Отменено", reply_markup=markups.main)
    else:
        log.write("Продавец: " + message.text + "\n")
        msg = bot.send_message(message.chat.id, "6. Фото", reply_markup=markups.photo)
        log.close()
        bot.register_next_step_handler(msg, finishing)


def finishing(message):
    global log
    global price

    url = "t.me/buyforton_debug_bot?start=" + str(message.message_id)

    inline = telebot.types.InlineKeyboardMarkup()
    appeal_btn = telebot.types.InlineKeyboardButton(text="Купить", url=url)
    inline.add(appeal_btn)

    if message.text == regexps.cancel:
        bot.send_message(message.chat.id, "Отменено", reply_markup=markups.main)
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
                bot.send_message(nextAdmin, appeal)
            else:
                bot.send_photo(nextAdmin, message.photo[1].file_id, appeal)
        except Exception as e:
            print(e)
        print

        connection = pymysql.connect(
            host="localhost",
            user="root",
            database="buyforton",
            cursorclass=pymysql.cursors.DictCursor,
        )

        with connection:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `buyforton_appeals` (`message_id`, `nickname`, `chat_id`, `price`, `name`) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(
                    sql,
                    (
                        message.message_id,
                        message.from_user.username,
                        message.chat.id,
                        price,
                        itemName,
                    ),
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
        bot.send_message(message.chat.id, "отменено", reply_markup=markups.main)
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
        "Отправьте TON по адресу: " + TON_ADRESS + " или отсканируйте QR код",
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
        database="buyforton",
        cursorclass=pymysql.cursors.DictCursor,
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
                reply_markup = shpwl_markup
            )

    else:
        bot.send_message(message.chat.id, "Пусто", reply_markup=shpwl_markup)


@bot.callback_query_handler(func=lambda c: c.data.find("order") != -1)
def show_order(c):
    connection = pymysql.connect(
        host="localhost",
        user="root",
        database="buyforton",
        cursorclass=pymysql.cursors.DictCursor,
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
    print(buy_id)
    print(result)
    bot.edit_message_text(
        "ЗАКАЗ " + str(result["name"]) + " ценой " + str(result["price"]) + " TON",
        c.message.chat.id,
        c.message.id,
        reply_markup = markups.order
    )
    print(result)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):

    if message.text == "Отменить":
        bot.send_message(message.chat.id, "Отменено", reply_markup=markups.main)
    if message.text.find("Оплатить") != -1:
        global buy_id
        global price
        buy_id = int(message.text.replace("Оплатить ", ""))
        connection = pymysql.connect(
            host="localhost",
            user="root",
            database="buyforton",
            cursorclass=pymysql.cursors.DictCursor,
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
                "Переведите {price} тон на следующий кошелек: ".format(price=price)
                + TON_ADRESS
                + " с комментарием «kuna-a7q1pmp0ju» и нажмите «Подтвердить». Перед отправкой советуем ознакомиться с руководством по ссылке \n https://telegra.ph/BUYFORTON-Oplata-03-04",
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
        database="buyforton",
        cursorclass=pymysql.cursors.DictCursor,
    )

    tr_chk = transaction_checker.check_transaction(message.text)
    msg_chk = transaction_checker.check_message(
        tr_chk["transactions"][0]["out_msgs"][0]
    )
    print(tr_chk)

    if (
        tr_chk["transactions"][0]["status"] == 3
        and msg_chk["messages"][0]["dst"] == TON_ADRESS
        and tr_chk["transactions"][0]["balance_delta"] <= config.float_to_hex(price)
    ):

        with connection:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `chat_id` FROM `buyforton_appeals` WHERE `message_id`=%s"
                cursor.execute(sql, (buy_id))
                result = cursor.fetchone()
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `shopwheels` (`message_id`, `user_id`, `seller_id`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (buy_id, message.from_user.id, result["chat_id"]))

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                connection.commit()
        bot.send_message(
            result["chat_id"],
            "Ваш товар оплачен юзером @" + message.from_user.username,
            reply_markup=markups.main,
        )
        bot.send_message(
            message.chat.id, "Операция прошла успешно", reply_markup=markups.main
        )
    else:
        msg = bot.send_message(
            message.chat.id, "Что-то пошло не так", reply_markup=markups.transaction
        )
        bot.register_next_step_handler(msg, confirmation)


if __name__ == "__main__":
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(e)
        pass
