'''
description: see readme.txt
usage:
status: working
todo:
'''

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters)  # python-telegram-bot
import logging, time, threading, datetime, configparser, pytz, atexit
import sensor
import RPi.GPIO as GPIO

sensors = []
event_log = []

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def initialize(configFile):
    config = configparser.ConfigParser()
    config.read(configFile)
    apiToken = config['settings']['apiToken']
    # logLength = int(config['settings']['logLength'])

    for section in config:
        if "sensor" in section:
            name = config[section]['name']
            type = config[section]['type']
            pin = config[section]['pin']
            sensors.append(sensor.Sensor(name, type, int(pin)))

    return apiToken


'''
def log_event(event):
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    pst_now = utc_now.astimezone(pytz.timezone("America/Los_Angeles"))
    l = event + pst_now.strftime(' %B %d, %Y %H:%M:%S')
    if len(event_log) >= logLength:
        del(event_log[0])
        event_log.append(l)
    else:
        event_log.append(l)

def print_log(bot, update):
    update.message.reply_text('OK, printing log...')
    time.sleep(1)
    for event in event_log:
        update.message.reply_text(event)
'''


def status(bot, update):
    for s in sensors:
        s.status(update)


def home(bot, update):
    update.message.reply_text('Arming for Home...')
    # disarm all sensors
    for s in sensors:
        s.exit_condition = True
    time.sleep(2)
    # arm only the contact sensors
    for s in sensors:
        if s.type == 'contact':
            s.exit_condition = False
            t = threading.Thread(target=s.monitor, args=[update])
            t.start()


def away(bot, update):
    update.message.reply_text('Arming for Away...')
    # disarm all sensors
    for s in sensors:
        s.exit_condition = True
    time.sleep(2)
    # arm all sensors
    for s in sensors:
        s.exit_condition = False
        t = threading.Thread(target=s.monitor, args=[update])
        t.start()


def disarm(bot, update):
    update.message.reply_text('Disarming...')
    for s in sensors:
        s.exit_condition = True


def cleanup():
    print('Cleaning Up...')
    GPIO.cleanup()


def error_callback(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)
    time.sleep(20*60)
    for s in sensors:
        s.exit_condition = True
    time.sleep(10)
    for s in sensors:
        s.exit_condition = False
    print("Bot restarted!")
    # update.message.reply_text("Error, please restart.")

def help(bot, update):
    update.message.reply_text('Commands:\n/home: Arm only contact sensors.\n/away: Arm all sensors.\n/disarm: Disarm all sensors.')


def main():
    print('Starting Telegram Bot...')
    apiToken = initialize('config.ini')
    atexit.register(cleanup)
    updater = Updater(apiToken)  # fetches updates from telegram, gives to dispatcher
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('home', home))  # register with dispatcher
    dispatcher.add_handler(CommandHandler('away', away))
    dispatcher.add_handler(CommandHandler("disarm", disarm))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler('status', status))
    dispatcher.add_error_handler(error_callback)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
