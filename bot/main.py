import telebot
import time
from telebot import types
from decouple import config

from common import getMostPopularPairs, printPairResult, getAvailableCommands
from routes import getUserById, createUser, getPair, buyCrypto, sellCrypto, exchangeCrypto, generateVoucher, redeemVoucher, getWallets, getPendingWithdrawals, withdrawalCrypto, getHistory, getVouchers

bot = telebot.TeleBot(config("BOT_API_KEY"))
bot.set_my_commands([
            telebot.types.BotCommand("/menu", "Get list of all commands"),
            telebot.types.BotCommand("/getpair", "Get crypto pair rate"),
            telebot.types.BotCommand("/buycrypto", "Buy crypto for USDT"),
            telebot.types.BotCommand("/sellcrypto", "Sell crypto for USDT"),
            telebot.types.BotCommand("/exchangecrypto", "Crypto-To-Crypto exchange"),
            telebot.types.BotCommand("/myvouchers", "Show all your vouchers"),
            telebot.types.BotCommand("/generatevoucher", "Generate voucher and send it to someone"),
            telebot.types.BotCommand("/redeemvoucher", "Redeem voucher and get crypto on your wallet"),
            telebot.types.BotCommand("/mywallets", "Get amounts of your balances"),
            telebot.types.BotCommand("/deposit", "Deposit crypto"),
            telebot.types.BotCommand("/withdrawal", "Withdrawal crypto"),
            telebot.types.BotCommand("/history", "Get history of your withdrawals and deposits")
        ])

commands = getAvailableCommands()


@bot.message_handler(commands=["help", "menu", "start"])
def menucmd(message):
    user = getUserById(message.chat.id)
    if user.get("status") is not None and user["status"] == 0:
        return startcmd(message)

    menuMessage = getmenumarkup(message.chat.first_name)
    markup = getkeyboardmarkup(["/contact", "/getpair", "/mywallets"])
    return bot.send_message(message.chat.id, menuMessage, reply_markup=markup, parse_mode="html")


@bot.message_handler(commands=["getpair"])
def getpaircmd(message):
    getPairMessage = "Ok, what's pair you are looking for?\n\n" \
                     "Here is the list of most popular pairs.\n\n" \
                     "Haven't found? Just type crypto! (Only USDT pair are available)"

    markup = types.ReplyKeyboardMarkup()
    mostPopularPairs = getMostPopularPairs()
    i = 0
    while i != len(mostPopularPairs):
        markup.add(
            types.InlineKeyboardButton(mostPopularPairs[i]),
            types.InlineKeyboardButton(mostPopularPairs[i + 1])
        )
        i += 2
    markup.add(types.InlineKeyboardButton("/menu"))

    return bot.send_message(message.chat.id, getPairMessage, reply_markup=markup, parse_mode="html")


@bot.message_handler(commands=["buycrypto"])
def buycryptocmd(message):
    buyCryptoMessage = "Buy cryptocurrencies for <i>USDT</i>\n\n"

    markup = types.ReplyKeyboardMarkup()
    return bot.send_message(message.chat.id, buyCryptoMessage, reply_markup=markup, parse_mode="html")


@bot.message_handler(commands=["sellcrypto"])
def sellcryptocmd(message):
    sellCryptoMessage = "Sell cryptocurrencies for <i>USDT</i>\n\n"

    markup = types.ReplyKeyboardMarkup()
    return bot.send_message(message.chat.id, sellCryptoMessage, reply_markup=markup, parse_mode="html")


@bot.message_handler(commands=["exchangecrypto"])
def exchangecryptocmd(message):
    exchangeCryptoMessage = "Pick pair to exchange cryptocurrencies\n\n"

    markup = types.ReplyKeyboardMarkup()
    return bot.send_message(message.chat.id, exchangeCryptoMessage, reply_markup=markup, parse_mode="html")


@bot.message_handler(commands=["generatevoucher"])
def generatevouchercmd(message):
    generateVoucherMessage = "To generate voucher provide command in this format:\n\n" \
                             "\gv Crypto Amount\n" \
                             "<b>Example:</b> \gv BTC 0.0001"
    
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("/menu"))
    markup.add(types.InlineKeyboardButton("/redeemvoucher"))
    markup.add(types.InlineKeyboardButton("/myvouchers"))
    return bot.send_message(message.chat.id, generateVoucherMessage, reply_markup=markup, parse_mode="html")


@bot.message_handler(commands=["redeemvoucher"])
def redeemvouchercmd(message):
    redeemVoucherMessage = "To redeem voucher provide command in this format:\n\n" \
                           "\\rv Voucher\n" \
                           "<b>Example:</b> \\rv 5CAE73AB2667FA99B5077EDA4353E85A"

    markup = getkeyboardmarkup(["/menu", "/generatevoucher", "/myvouchers"])
    return bot.send_message(message.chat.id, redeemVoucherMessage, reply_markup=markup, parse_mode="html")


@bot.message_handler(commands=["myvouchers"])
def myvoucherscmd(message):
    myVouchersMessage = "*List of your unreedemed vouchers:* (click on to copy to clipboard)\n\n"
    vouchers = getVouchers(message.chat.id)

    for voucher in vouchers:
        myVouchersMessage += f"----------------\nCrypto: {voucher['symbol']}\nAmount: {voucher['amount']}\nVoucher: `{voucher['codeenc']}`\n"

    keyboard = [[types.InlineKeyboardButton("Hide vouchers", callback_data='hide_vouchers')]]
    markup = types.InlineKeyboardMarkup(keyboard)
    return bot.send_message(message.chat.id, myVouchersMessage, reply_markup=markup, parse_mode="markdown")


@bot.message_handler(commands=["mywallets"])
def mywalletscmd(message):
    myWalletsMessage = "*List of your wallets:*\n\n"
    wallets = getWallets(message.chat.id)

    for wallet in wallets:
        myWalletsMessage += f"----------------\nCrypto: {wallet['symbol'][:-3]}\nAmount: {wallet['amount']}\nWallet: `{wallet['wallet']}`\n"

    markup = getkeyboardmarkup(["/menu", "/deposit", "/withdrawal", "/history"])
    return bot.send_message(message.chat.id, myWalletsMessage, reply_markup=markup, parse_mode="markdown")


@bot.message_handler(commands=["deposit"])
def depositcmd(message):
    depositMessage = "Your wallets:\n\n"
    wallets = getWallets(message.chat.id)

    for wallet in wallets:
        depositMessage += f"----------------\nCrypto: <b>{wallet['symbol'][:-3]}</b>\nWallet: <u>{wallet['wallet']}</u>\n"

    markup = getkeyboardmarkup(["/menu", "/withdrawal", "/mywallets"])
    return bot.send_message(message.chat.id, depositMessage, reply_markup=markup, parse_mode="html")


@bot.message_handler(commands=["withdrawal"])
def withdrawalcmd(message):
    withdrawalMessage = ""
    pendingWithdrawals = getPendingWithdrawals(message.chat.id)

    if (len(pendingWithdrawals) == 0):
        withdrawalMessage += "<b>You have no pending withdrawals.</b>\n\n"
    else:
        withdrawalMessage += "<b>Your pending withdrawals:</b>\n\n"

    withdrawalMessage += "If you want withdrawal crypto on external wallet, first choose the crypto, " \
        "and then provide external wallet and amount to withdraw.\n\n" \
        "Or provide message in this format: <b>\w Crypto Amount Destination</b>\n" \
        "Example: \w BTC 0.00008 mwR1LkQVXJ6fWYcTKmtQRPfV6a8o6883XE"

    markup = getkeyboardmarkup(["/menu", "/deposit", "/mywallets"])
    return bot.send_message(message.chat.id, withdrawalMessage, reply_markup=markup, parse_mode="html")


@bot.message_handler(commands=["history"])
def historycmd(message):
    historyMessage = "<b>Here is history of your wallet transactoins:</b>\n\n"
    userHistory = getHistory(message.chat.id)

    if (len(userHistory) == 0):
        historyMessage += "You have no history on your wallets. Go on, and do crypto <a>/deposit</a>!"
    else:
        historyMessage += ""

    markup = getkeyboardmarkup(["/menu", "/deposit", "/withdrawal"])
    return bot.send_message(message.chat.id, historyMessage, reply_markup=markup, parse_mode="html")


@bot.message_handler(commands=["contact"])
def contactcmd(message):
    contactMessage = "In case if you have any questions, please text here:\n\nContact email: bl4drnnr@protonmail.com\nPGP: 8773E25F4E5B06F60AD9A04151E343BA669AD317"

    markup = getkeyboardmarkup(["/menu", "/getpair", "/mywallets"])
    return bot.send_message(message.chat.id, contactMessage, reply_markup=markup, parse_mode="html")


@bot.callback_query_handler(func=lambda call: True)
def commandshandlebtn(call):
    userMessage = call.data

    # Commands by buttons click
    if len(userMessage.split()) == 2 and userMessage.split()[1] == "create":
        # Creating new user
        createdUser = createUser({"userid": userMessage.split()[0]})
        if createdUser["status"] == 1:
            return menucmd(call.message)
        else:
            return defaulterrormessage(call.message)
    elif userMessage == "hide_vouchers":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=getmenumarkup(call.message.chat.first_name), parse_mode="html")


@bot.message_handler(content_types=["text"])
def manualhandlermessage(message):
    userMessage = message.text.strip().upper()
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("/menu"))

    if userMessage[0] == "/":
        # Manual commands handler
        userMessage = userMessage.lower()
        if userMessage not in commands:
            userMessage = "/menu"
            return bot.send_message(message.chat.id, "Are you sure about this command?\n\nSee menu to get all possible commands", reply_markup=markup)
    elif userMessage[0:3] == "\W ":
        withdrawalCrypto({})
    elif userMessage[0:4] == "\GV ":
        generateVoucher({
            "userid": str(message.chat.id),
            "crypto": userMessage.split()[1],
            "amount": userMessage.split()[2]
        })
    elif userMessage[0:4] == "\RV ":
        redeemVoucher({
            "userid": str(message.chat.id),
            "voucher": userMessage.split()[1]
        })
    else:
        # Looking for pair
        pair = getPair(str(userMessage) + str("USDT"))

        markup = types.ReplyKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("/menu"), types.InlineKeyboardButton("/getpair"))
        if pair.get("status") is not None:
            return bot.send_message(message.chat.id, "We haven't found that crypto. :(", reply_markup=markup)

        pairMessage = printPairResult(pair)

        return bot.send_message(message.chat.id, pairMessage, parse_mode="html", reply_markup=markup)


def startcmd(message):
    # New user start message
    startMessage = f"Hello there, <b><i>{message.from_user.first_name}</i></b>!\n" \
                   f"Welcome to PCM - P2P cryptoexchange in your pocket.\n\n" \
                   f"+ No KYC/AML. Absolutely anonymous!\n" \
                   f"+ Availability of buying and selling crypto for USDT \n" \
                   f"+ State fee for all operations (0,00004 BTC)"

    initData = f"{str(message.from_user.id)} create"

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Let's start", callback_data=initData))
    return bot.send_message(message.chat.id, startMessage, parse_mode="html", reply_markup=markup)


def defaulterrormessage(chatid):
    errorMessage = "<b><i>Something went wrong! Maybe you should try again?</i></b>"
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("/menu"))
    return bot.send_message(chatid, errorMessage, parse_mode="html") 


def getkeyboardmarkup(items):
    markup = types.ReplyKeyboardMarkup()

    for item in items:
        markup.add(types.InlineKeyboardButton(item))

    return markup


def getmenumarkup(username):
    return f"Welcome, <u>{username}</u>, let's start!\n\n" \
                  f"What are we gonna do?\n\n" \
                  f"<b><i>Crypto</i></b>\n\n" \
                  f"<a>/getpair</a> - get crypto pair rate (<i>to USDT only, for now</i>)\n" \
                  f"<a>/buycrypto</a> - buy crypto for USDT\n" \
                  f"<a>/sellcrypto</a> - sell crypto for USDT\n" \
                  f"<a>/exchangecrypto</a> - Crypto-To-Crypto exchange\n\n" \
                  f"<b><i>Vouchers</i></b>\n\n" \
                  f"<a>/myvouchers</a> - show all your vouchers\n" \
                  f"<a>/generatevoucher</a> - generate voucher and send it to someone\n" \
                  f"<a>/redeemvoucher</a> - redeem voucher and get crypto on your wallet\n\n" \
                  f"<b><i>Wallets</i></b>\n\n" \
                  f"<a>/mywallets</a> - get amounts of your balances\n" \
                  f"<a>/deposit</a> - deposit crypto\n" \
                  f"<a>/withdrawal</a> - withdrawal crypto\n" \
                  f"<a>/history</a> - get history of your wallet\n " \


if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)
