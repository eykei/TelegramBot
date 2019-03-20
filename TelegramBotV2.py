'''
author: eykei
description:
usage:
notes:
issues: handle timed out error
'''

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters)  # python-telegram-bot
import logging, time, threading, datetime, configparser, pytz, atexit
import sensor
import RPi.GPIO as GPIO
config= configparser.ConfigParser()
config.read('config.ini')

apiToken = config['settings']['apiToken']
logLength = int(config['settings']['logLength'])

sensors = []
event_log = []

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

sensor1 = sensor.Sensor('Door', 'contact', 7)
sensors.append(sensor1)

'''
def status(bot, update):
    doorOpen = GPIO.input(sensorPin)
    if doorOpen:
        update.message.reply_text('Door is currently open.')
    else:
        update.message.reply_text('Door is currently closed.')


def log_event(event):
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    pst_now = utc_now.astimezone(pytz.timezone("America/Los_Angeles"))
    l=event+ pst_now . strftime(' %B %d, %Y %H:%M:%S')
    if len(event_log) >= logLength:
        del(event_log[0])
        event_log.append(l)
    else:
        event_log.append(l)

def log(bot, update):
    update.message.reply_text('OK, printing log...')
    time.sleep(1)
    for event in event_log:
        update.message.reply_text(event)
'''


def home(bot, update):  # function for handling the /start command
    update.message.reply_text('Arming for Home...')
    for s in sensors:
        if s.type == 'contact':
            t = threading.Thread(target=s.monitor, args=[update])
            t.start()

def away(bot, update):
    update.message.reply_text('Arming for Away...')
    for s in sensors:
        t = threading.Thread(target=s.monitor, args=[update])
        t.start()


def disarm(bot, update) :
    update.message.reply_text('Disarming...')
    for s in sensors:
        s.exit_condition = True



def error_callback(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)
    # update.message.reply_text("Error, please restart.")

def main():
    print('Starting Telegram Bot...')
    updater = Updater(apiToken)  # fetches updates from telegram, gives to dispatcher
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('home', home))  # register with dispatcher
    dispatcher.add_handler(CommandHandler("disarm", disarm))
    #dispatcher.add_handler(CommandHandler("log",log) )
    #dispatcher.add_handler(CommandHandler('status', status))
    dispatcher.add_error_handler(error_callback)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
