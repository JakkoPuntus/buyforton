import telebot
import regexps

main = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
appeal = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
photo = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
buying = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
transaction = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
order = telebot.types.InlineKeyboardMarkup()

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
order.row(back)

