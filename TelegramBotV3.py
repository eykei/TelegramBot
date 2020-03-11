'''
description: see readme.txt
usage:
status: working
todo:
'''

from telegram.ext import (Updater, CommandHandler)
import logging, time, threading, configparser, atexit
import sensor
import RPi.GPIO as GPIO

sensors = []
subscribers = []

# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# logger = logging.getLogger(__name__)

def initialize(configFile):
    config = configparser.ConfigParser()
    config.read(configFile)
    apiToken = config['settings']['apiToken']

    for section in config:
        if "sensor" in section:
            name = config[section]['name']
            type = config[section]['type']
            pin = config[section]['pin']
            sensors.append(sensor.Sensor(name, type, int(pin)))

    return apiToken

def subscribe(update, context):
    subscribers.append(update.message.from_user['id'])
    update.message.reply_text('Successfully subscribed!')

def unsubscribe(update, context):
    subscribers.remove(update.message.from_user['id'])
    try:
        subscribers.remove(update.message.from_user['id'])
        update.message.reply_text('Successfully unsubscribed!')
    except:
        update.message.reply_text('Could not find subscriber!')

def status(update, context):
    print(update.message.from_user)
    for s in sensors:
        s.status(context, subscribers)

def home(update, context):
    update.message.reply_text('Arming for Home...')
    # disarm all sensors
    for s in sensors:
        s.exit_condition = True
    time.sleep(2)
    # arm only the contact sensors
    for s in sensors:
        if s.type == 'contact':
            s.exit_condition = False
            t = threading.Thread(target=s.monitor, args=[context, subscribers])
            t.start()


def away(update, context):
    update.message.reply_text('Arming for Away...')
    # disarm all sensors
    for s in sensors:
        s.exit_condition = True
    time.sleep(2)
    # arm all sensors
    for s in sensors:
        s.exit_condition = False
        t = threading.Thread(target=s.monitor, args=[context, subscribers])
        t.start()


def disarm(update, context):
    update.message.reply_text('Disarming...')
    for s in sensors:
        s.exit_condition = True


def cleanup():
    print('Cleaning Up...')
    GPIO.cleanup()


def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    time.sleep(10)
    for s in sensors:
        s.exit_condition = True
    time.sleep(10)
    for s in sensors:
        s.exit_condition = False
        t = threading.Thread(target=s.monitor, args=[context, subscribers])
        t.start()
    print("Bot restarted!")
    for subscriber in subscribers:
        context.bot.send_message(subscriber, 'Error encountered, bot restarted!')

def help(update, context):
    update.message.reply_text('Commands:'
                              '\n/subscribe: Subscribe to receive alerts. '
                              '\n/unsubscribe: Unsubscribe from alerts'
                              '\n/home: Arm only contact sensors.'
                              '\n/away: Arm all sensors.'
                              '\n/disarm: Disarm all sensors.')


def main():
    print('Starting Telegram Bot...')
    apiToken = initialize('config.ini')
    atexit.register(cleanup)
    updater = Updater(apiToken, use_context=True)  # fetches updates from telegram, gives to dispatcher
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('subscribe', subscribe))#register functions with dispatcher
    dispatcher.add_handler(CommandHandler('unsubscribe', unsubscribe))
    dispatcher.add_handler(CommandHandler('home', home))
    dispatcher.add_handler(CommandHandler('away', away))
    dispatcher.add_handler(CommandHandler("disarm", disarm))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler('status', status))

    dispatcher.add_error_handler(error_callback)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
