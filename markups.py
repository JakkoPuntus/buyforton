import telebot
import regexps

main = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
appeal = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
photo = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
buying = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
transaction = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)


newproduct = telebot.types.KeyboardButton(regexps.newproduct)
newservice = telebot.types.KeyboardButton(regexps.newservice)
support = telebot.types.KeyboardButton(regexps.support)
donate = telebot.types.KeyboardButton(regexps.donate)
cancel = telebot.types.KeyboardButton(regexps.cancel)
skip = telebot.types.KeyboardButton(regexps.skip)
vip = telebot.types.KeyboardButton(regexps.vip)
confirm = telebot.types.KeyboardButton(regexps.confirm)
shopcart = telebot.types.KeyboardButton(regexps.shopcart)
back = telebot.types.InlineKeyboardButton(regexps.back, callback_data = "back")

main.row(newproduct, newservice)
main.row(donate, support)
main.row(shopcart)
appeal.row(cancel)
photo.row(cancel, skip)
transaction.row(cancel, confirm)

#categories
general = telebot.types.KeyboardButton("🛍🛒Общая")
hand_made =  telebot.types.KeyboardButton('🧶🧵🎨 Хэнд-мейд')
souvenirs = telebot.types.KeyboardButton('🏆🏺🎁 Сувениры ')
food = telebot.types.KeyboardButton('🍰🍒🍗 Продукты питания ')
pets = telebot.types.KeyboardButton('🐶🐱Домашние питомцы')
digital = telebot.types.KeyboardButton('📲Цифровые товары')
tech = telebot.types.KeyboardButton('💻 Техника')
sport = telebot.types.KeyboardButton('⚽️🏀🏓 Товары для спорта ')
adult = telebot.types.KeyboardButton('👙🔞👄 18+')
holiday = telebot.types.KeyboardButton('🎁 К празднику')
repair = telebot.types.KeyboardButton('🛠 Запчасти')

categories = telebot.types.ReplyKeyboardMarkup(selective = False)

categories.row(hand_made, souvenirs, food)
categories.row(pets, holiday, digital)
categories.row(tech, sport, repair, adult)
categories.row(general)
