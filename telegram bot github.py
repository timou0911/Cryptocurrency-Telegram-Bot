from telegram.ext import * 
from telegram import *
import telegram
from binance import *
import pandas as pd

updater = Updater('telegram bot API') #telegram bot API
dispatcher = updater.dispatcher
bot = telegram.Bot('telegram bot API')

apikey = 'Binance API key' #binance API key
secret = 'Binance secret key' #binance secret key
client = Client(apikey, secret)

list = [] #儲存pairs的list

def start(update:Update, context:CallbackContext):
    context.message.reply_text('You can know the cryptocurrency pair price currently. Type /help to know how to operate.')

#直接輸入pair搜尋價格
def search(update:Update, context:CallbackContext):
    pair = context.message.text
    pair = pair.upper()
    tickers = client.get_all_tickers()
    ticker_df = pd.DataFrame(tickers)
    ticker_df.set_index('symbol', inplace=True)

    if pair not in ticker_df.index:
        context.message.reply_text('I don\'t know what you\'re talking about.')
    else:
        context.message.reply_text('Current price is:')
        context.message.reply_text(float(ticker_df.loc[pair]))

#收藏pairs
def save(update:Update, context:CallbackContext):
    pair = context.message.text[6:]
    pair = pair.upper()
    tickers = client.get_all_tickers()
    ticker_df = pd.DataFrame(tickers)
    ticker_df.set_index('symbol', inplace=True)

    if pair not in ticker_df.index:
        context.message.reply_text('I don\'t know what you\'re talking about.')
    else:
        if pair in list:
            context.message.reply_text('It\'s already saved.')
        else:
            list.append(pair)
            context.message.reply_text('Successfully save.')

#移除收藏
def remove(update:Update, context:CallbackContext):
    pair = context.message.text[8:]
    pair = pair.upper()
    tickers = client.get_all_tickers()
    ticker_df = pd.DataFrame(tickers)
    ticker_df.set_index('symbol', inplace=True)

    if pair not in ticker_df.index:
        context.message.reply_text('I don\'t know what you\'re talking about.')
    else:
        if pair not in list:
            context.message.reply_text('It\'s not saved in the list.')
        else:
            list.remove(pair)
            context.message.reply_text('Successfully remove.')

#輸出收藏pairs的價格
def show(update:Update, context:CallbackContext):
    list.sort()
    tickers = client.get_all_tickers()
    ticker_df = pd.DataFrame(tickers)
    ticker_df.set_index('symbol', inplace=True)
    reply = ""
    
    if list == []:
        context.message.reply_text('You haven\'t saved any pair.')
    else:
        for n in range(0, len(list), 1):
            pair = list[n-1]
            price = float(ticker_df.loc[pair])
            reply += 'Pair : {}\nPrice : $ {}\n\n'.format(pair, price)
        context.message.reply_text(reply)

#清除收藏
def clear(update:Update, context:CallbackContext):
    list.clear()
    context.message.reply_text('Successfully clear.')

#顯示操作清單
def help(update:Update, context:CallbackContext):
    context.message.reply_text(
"""
1. You can enter the pair to know the current price. E.g. BTCBUSD
2. /save ----> Save the pair in the list. E.g. /save BTCBUSD
3. /remove ----> Remove the pair from the list. E.g. /remove BTCBUSD
4. /show ----> Show each saved pair's current price.
5. /clear ----> Clear the whole list.
"""
)

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('save', save))
dispatcher.add_handler(CommandHandler('remove', remove))
dispatcher.add_handler(CommandHandler('show', show))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('clear', clear))
dispatcher.add_handler(MessageHandler(Filters.text, search))

updater.start_polling() 
updater.idle()