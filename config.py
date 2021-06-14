import struct
#
TOKEN = "1453628529:AAGXPfrDPvsfHdywv65OqyDmoZiad-mSZng"
DEBUG_TOKEN = "1415540544:AAFdPPVCD5tLmOxgaOr034T9vso33z48LAU"
ADMIN_ID = 564941525
nextAdmin = 954657975

admins_list = [564941525, 954657975]

hello_file = open("hello.txt", encoding="utf-8")
hello_text = hello_file.read()


TON_ADRESS = "0:af22c44fc447f8497219969d6faed49894584f0de66a208956aec20c1ed47530"


def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])


categories = {
    '🛍🛒Общая': '@b4t_product_all',
    '👕👚🕶 Одежда и аксессуары': '@b4t_product_dress',
    '🧶🧵🎨 Хэнд-мейд': '@b4t_product_handmade',
    '🏆🏺🎁 Сувениры': '@b4t_product_souvenirs',
    '🍰🍒🍗 Продукты питания': '@b4t_product_foods',
    '🐶🐱Домашние питомцы': '@b4t_product_pets',
    '🎁 К празднику': '@b4t_product_holiday',
    '📲Цифровые товары': '@b4t_product_digital',
    '💻 Техника': '@b4t_product_tech',
    '⚽️🏀🏓 Товары для спорта': '@b4t_product_sport',
    '🛠 Запчасти': '@b4t_product_repair',
    '👙🔞👄 18+': '@b4t_product_adult',
    '💵💎Оплата за TON': '@b4t_services_pay',
    '🤝Прочие услуги': '@b4t_services_all'
}

categories_service = {
    '💵💎Оплата за TON': '@b4t_services_pay',
    '🤝Прочие услуги': '@b4t_services_all'
}


commands = {
    'general': 'Категория: 🛍🛒Общая',
    'cloth': 'Категория: 👕👚🕶 Одежда и аксессуары',
    'handmade': 'Категория: 🧶🧵🎨 Хэн-мейд',
    'souvenirs': 'Категория: 🏆🏺🎁 Сувениры',
    'food': 'Категория: 🍰🍒🍗 Продукты питания',
    'pets': 'Категория: 🐶🐱Домашние питомцы',
    'holiday': 'Категория: 🎁 К празднику',
    'digital': 'Категория: 📲Цифровые товары',
    'tech': 'Категория: 💻 Техника',
    'sport': 'Категория: ⚽️🏀🏓 Товары для спорта',
    'repair': 'Категория: 🛠 Запчасти',
    'adult': 'Категория: 👙🔞👄 18+',
    'pay': 'Категория: 💵💎Оплата за TON',
    's_all': 'Категория: 🤝Прочие услуги'

}

countries = {
    '🇧🇾Беларусь': 'Беларусь',
    '🇷🇺Россия' : 'Россия',
    '🇺🇦Украина' : 'Украина',
    '🇰🇿Казахстан' : 'Россия',
    '🏴Другое' : 'Другое'
}