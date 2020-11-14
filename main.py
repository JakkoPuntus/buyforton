import telebot
from config import TOKEN, ADMIN_ID, nextAdmin, hello_text, form

bot = telebot.TeleBot(TOKEN, num_threads = 4)

markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
mkp_newproduct = telebot.types.KeyboardButton('Создать новый товар')
mkp_support = telebot.types.KeyboardButton('Написать в техподдержку')
mkp_donate = telebot.types.KeyboardButton('Поддержать проект')
markup.row(mkp_newproduct, mkp_support)
markup.row(mkp_donate)

log = open("log.txt", "w", encoding = "utf-8")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, hello_text, reply_markup = markup)

@bot.message_handler(commands=["ban"])
def ban_user(message):
    bot.kick_chat_member(message.chat.id, message.chat.id)

@bot.message_handler(regexp = "Создать новый товар")
def first_step(message):
    bot.send_message(message.chat.id, "Пожалуйста введите:", reply_markup = None)
    msg = bot.send_message(message.chat.id, "1. Название товара", reply_markup = None)
    bot.register_next_step_handler(msg, second_step)

def second_step(message):
    log.write("Название: " + message.text + "\n")
    msg = bot.send_message(message.chat.id, "2. Описание  товара")
    bot.register_next_step_handler(msg, third_step)

def third_step(message):
    log.write("Описание: " + message.text + "\n")
    msg = bot.send_message(message.chat.id, "3. Цена товара")
    bot.register_next_step_handler(msg, fourth_step)

def fourth_step(message):
    log.write("Цена: " + message.text + "\n")
    msg = bot.send_message(message.chat.id, "4. Ваш город")
    bot.register_next_step_handler(msg, fifth_step)
        
def fifth_step(message):
    log.write("Город: " + message.text + "\n")
    msg = bot.send_message(message.chat.id, "5. Ваш никнейм в телеграме (например @username)")
    bot.register_next_step_handler(msg, sixth_step)

def sixth_step(message):
    log.write("Никнейм: " + message.text + "\n")
    bot.send_message(message.chat.id, "Заявка отправлена на модерацию")
    log.close()
    loger = open("log.txt", "r", encoding = "utf-8")
    text = loger.read()
    print(text)
    bot.send_message(ADMIN_ID, text)
    loger.close()

bot.enable_save_next_step_handlers(delay = 2)
bot.load_next_step_handlers()

@bot.message_handler(regexp = "Написать в техподдержку")
def support_first(message):
    msg = bot.send_message(message.chat.id, "Задайте свой вопрос модераторам")
    bot.register_next_step_handler(msg, support)

def support(message):
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "Ваше обращение принято, мы вам ответим")

@bot.message_handler(regexp = "Поддержать проект")
def donate(message):
    photo = open("img/qr.jpg", "rb")
    bot.send_photo(message.chat.id, photo, "Отправьте TON по адресу: EQDMEdLrfKYcQsS2a34hgQxWZfpaD91sbtL9eQpis0TmybgN или отсканируйте QR код в приложении TON Surf")
    

@bot.message_handler(content_types = ["text"])
def repeat_all_messages(message):
    if message.chat.id == ADMIN_ID:
        try:
            print(message.reply_to_message.message_id)
            bot.send_message(message.reply_to_message.chat.id, message.text,  reply_markup = markup)
        except:
            print("None")





if __name__ == "__main__":
    bot.infinity_polling(none_stop = True)