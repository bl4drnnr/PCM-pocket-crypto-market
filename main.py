import telebot
from telebot import types
from decouple import config

from common import getMostPopularPairs
from bybitapi import getPairApi

bot = telebot.TeleBot(config('BOT_API_KEY'))


@bot.message_handler(commands=['start'])
def start(message):
    welcomeMessage = f'Your welcome, <u>{message.from_user.first_name}</u>, let\'s start!\n\n' \
                     f'What are we going to do?\n\n' \
                     f'/getpair - get crypto pair rate'
    bot.send_message(message.chat.id, welcomeMessage, parse_mode='html')


@bot.message_handler(commands=['getpair'])
def getpair(message):
    getPairMessage = 'Ok, what\'s pair you are looking for?\n\n' \
                     'Here is the list of most popular pairs.\n\n' \
                     'Haven\'t found? Just type pair! (example of format - BTCUSDC)'

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    for mpp in getMostPopularPairs():
        mpp = types.KeyboardButton(mpp)
        markup.add(mpp)
    bot.send_message(message.chat.id, getPairMessage, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def getpairfunc(message):
    userMessage = message.text.strip().upper()
    # pairResult = ""
    pair = getPairApi(userMessage)
    bot.send_message(message.chat.id, pair)


bot.polling(none_stop=True)
