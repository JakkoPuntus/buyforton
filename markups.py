import telebot
import regexps

main = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
appeal = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
photo = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)

newproduct = telebot.types.KeyboardButton(regexps.newproduct)
newservice = telebot.types.KeyboardButton(regexps.newservice)
support = telebot.types.KeyboardButton(regexps.support)
donate = telebot.types.KeyboardButton(regexps.donate)
cancel = telebot.types.KeyboardButton(regexps.cancel)
skip = telebot.types.KeyboardButton(regexps.skip)
vip = telebot.types.KeyboardButton(regexps.vip)

main.row(newproduct, newservice)
main.row(donate, support)
appeal.row(cancel)
photo.row(cancel, skip)