import telebot
from config import TOKEN, ADMIN_ID, nextAdmin, hello_text, form

bot = telebot.TeleBot(TOKEN, num_threads = 4)

markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
markup_appeal = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)

mkp_newproduct = telebot.types.KeyboardButton('Создать новый товар')
mkp_support = telebot.types.KeyboardButton('Написать в техподдержку')
mkp_donate = telebot.types.KeyboardButton('Поддержать проект')
mkp_cancel = telebot.types.KeyboardButton('Отменить')
mkp_skip = telebot.types.KeyboardButton('Пропустить')

markup.row(mkp_newproduct, mkp_support)
markup.row(mkp_donate)
markup_appeal.row(mkp_cancel)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, hello_text, reply_markup = markup)

@bot.message_handler(commands=["ban"])
def ban_user(message):
    bot.kick_chat_member(message.chat.id, message.chat.id)

@bot.message_handler(regexp = "Создать новый товар")
def first_step(message):
    global log
    global name
    name = str(message.chat.id) + ".txt"
    try:
        log = open(name, "x", encoding = "utf-8")
    except:
        log = open(name, "r+", encoding = "utf-8")
    bot.send_message(message.chat.id, "Пожалуйста введите:", reply_markup = markup_appeal)
    msg = bot.send_message(message.chat.id, "1. Название товара", reply_markup = markup_appeal)
    bot.register_next_step_handler(msg, second_step)

def second_step(message):
    global log
    if message.text == "Отменить":
        bot.send_message(message.chat.id, "Создание товара отменено", reply_markup = markup)
    else:
        log.write("Название: " + message.text + "\n")
        msg = bot.send_message(message.chat.id, "2. Описание  товара", reply_markup = markup_appeal)
        bot.register_next_step_handler(msg, third_step)

def third_step(message):
    global log
    if message.text == "Отменить":
        bot.send_message(message.chat.id, "Создание товара отменено", reply_markup = markup)
    else:
        log.write("Описание: " + message.text + "\n")
        msg = bot.send_message(message.chat.id, "3. Цена товара", reply_markup = markup_appeal)
        bot.register_next_step_handler(msg, fourth_step)

def fourth_step(message):
    global log
    if message.text == "Отменить":
        bot.send_message(message.chat.id, "Создание товара отменено", reply_markup = markup)
    else:
        log.write("Цена: " + message.text + "\n")
        msg = bot.send_message(message.chat.id, "4. Ваш город", reply_markup = markup_appeal)
        bot.register_next_step_handler(msg, fifth_step)
        
def fifth_step(message):
    global log
    if message.text == "Отменить":
        bot.send_message(message.chat.id, "Создание товара отменено", reply_markup = markup)
    else:
        log.write("Город: " + message.text + "\n")
        msg = bot.send_message(message.chat.id, "5. Ваш никнейм в телеграме (например @username)", reply_markup = markup_appeal)
        bot.register_next_step_handler(msg, sixth_step)

def sixth_step(message):
    global log
    if message.text == "Отменить":
        bot.send_message(message.chat.id, "Создание товара отменено", reply_markup = markup)
    else:
        log.write("Никнейм: " + message.text + "\n")
        msg = bot.send_message(message.chat.id, "6. Фото", reply_markup = markup_appeal)
        log.close()
        bot.register_next_step_handler(msg, seventh_step)

def seventh_step(message):
    global log
    global name
    loger = open(name, "r", encoding = "utf-8")
    appeal = loger.read()
    if message.text == "Отменить":
        bot.send_message(message.chat.id, "Создание товара отменено", reply_markup = markup)
    else:
        try:
            bot.send_photo(ADMIN_ID, message.photo[1].file_id,appeal)
            bot.send_message(message.chat.id, "Заявка отправлена на модерацию", reply_markup=markup)
        except:
            msg = bot.send_message(message.chat.id, "Упс, попробуйте ещё раз", reply_markup=markup_appeal)
            bot.register_next_step_handler(msg, seventh_step)
        try:
            bot.send_photo(nextAdmin, message.photo[1].file_id, appeal)
        except Exception as e:
            print("blya")
            print(e)

            


bot.enable_save_next_step_handlers(delay = 2)
bot.load_next_step_handlers()

@bot.message_handler(regexp = "Написать в техподдержку")
def support_first(message):
    msg = bot.send_message(message.chat.id, "Задайте свой вопрос модераторам")
    bot.register_next_step_handler(msg, support)

def support(message):
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.forward_message(nextAdmin, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "Ваше обращение принято, мы вам ответим")

@bot.message_handler(regexp = "Поддержать проект")
def donate(message):
    photo = open("img/qr.png", "rb")
    bot.send_photo(message.chat.id, photo, "Отправьте TON по адресу: 0:96bb71fde16dc04cf3721f66a1b959cc32c5842a5877965d37f6bd894b1bf608 или отсканируйте QR код")
    

@bot.message_handler(content_types = ["text"])
def repeat_all_messages(message):
    if message.chat.id == ADMIN_ID:
        try:
            print(message.reply_to_message.message_id)
            bot.send_message(message.reply_to_message.chat.id, message.text,  reply_markup = markup)
        except Exception as e:
            print(e)





if __name__ == "__main__":
    bot.infinity_polling(none_stop = True)