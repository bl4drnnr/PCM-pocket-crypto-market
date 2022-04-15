import telebot
from telebot import types
from decouple import config

from common import getMostPopularPairs
from bybitapi import getPairApi

bot = telebot.TeleBot(config('BOT_API_KEY'))


@bot.message_handler(commands=['start', 'help'])
def start(message):
    welcomeMessage = f'Your welcome, <u>{message.from_user.first_name}</u>, let\'s start!\n\n' \
                     f'What are we gonna do?\n\n' \
                     f'<b><i>Crypto</i></b>\n\n' \
                     f'<a>/getpair</a> - get crypto pair rate (<i>to USDT only, for now</i>)\n' \
                     f'<a>/setalarm</a> - set alarm and get notified when set price is hit\n\n' \
                     f'<b><i>Positions</i></b>\n\n' \
                     f'<a>/commitposition</a> - commit your position to collect data\n'
    bot.send_message(message.chat.id, welcomeMessage, parse_mode='html')


@bot.message_handler(commands=['setalarm'])
def setalarm(message):
    bot.send_message(message.chat.id, "/help")


@bot.message_handler(commands=['commitposition'])
def commitposition(message):
    bot.send_message(message.chat.id, "/help")


@bot.message_handler(commands=['getpair'])
def getpair(message):
    getPairMessage = 'Ok, what\'s pair you are looking for?\n\n' \
                     'Here is the list of most popular pairs.\n\n' \
                     'Haven\'t found? Just type pair! (example of format - BTCUSDT)'

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    for mpp in getMostPopularPairs():
        mpp = types.KeyboardButton(mpp)
        markup.add(mpp)
    bot.send_message(message.chat.id, getPairMessage, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def getpairfunc(message):
    userMessage = message.text.strip().upper()
    pair = getPairApi(userMessage)

    if not pair:
        return bot.send_message(message.chat.id, "Nah, not that, try something else.")

    pairResult = f'Here you go with <b>{pair["symbol"]}</b> pair:\n\n' \
                 f'Mark price: <b>{pair["mark_price"]}</b>\n' \
                 f'Index price: <b>{pair["index_price"]}</b>\n\n' \
                 f'Purchase price: <b>{pair["bid_price"]}</b>\n' \
                 f'Selling price: <b>{pair["ask_price"]}</b>\n\n' \
                 f'The highest price in the last 24 hours: <b>{pair["high_price_24h"]}</b>\n' \
                 f'Lowest price in the last 24 hours: <b>{pair["low_price_24h"]}</b>\n'

    bot.send_message(message.chat.id, pairResult, parse_mode='html')


bot.polling(none_stop=True)
