import telebot

main = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
appeal = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
photo = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)

newproduct = telebot.types.KeyboardButton('Создать новый товар')
newservice = telebot.types.KeyboardButton('Создать новую услугу')
support = telebot.types.KeyboardButton('Написать в техподдержку')
donate = telebot.types.KeyboardButton('Поддержать проект')
cancel = telebot.types.KeyboardButton('Отменить')
skip = telebot.types.KeyboardButton('Пропустить')
vip = telebot.types.KeyboardButton('Купить VIP 💎')

main.row(newproduct, newservice)
main.row(donate, support)
appeal.row(cancel)
photo.row(cancel, skip)