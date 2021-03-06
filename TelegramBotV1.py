'''
author: eykei
description:
usage:
notes:
issues: handle timed out error
'''

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters)  # python-telegram-bot
import logging, time, threading, datetime, configparser, pytz, atexit
import RPi.GPIO as GPIO
config= configparser.ConfigParser()
config.read('config.ini')

apiToken = config['settings']['apiToken']
sensorPin = int(config['settings']['sensorPin'])
logLength = int(config['settings']['logLength'])

event_log = []
exit_condition = False

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def GPIOMonitor(update):
    GPIO.setmode(GPIO.BOARD)  # use the name of the pins by position
    GPIO.setup(sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # sensor reads high when door is open (door switch is on normally closed)

    doorOpen_prev = GPIO.input(sensorPin)

    while True:
        # print(GPIO.input(sensorPin))
        doorOpen_curr = GPIO.input(sensorPin)

        if doorOpen_curr!= doorOpen_prev:
            if doorOpen_curr:  # if the door is currently open
                event = 'Door is Open!'
                update.message.reply_text(event)
                log_event(event)
                doorOpen_prev = True
            if not doorOpen_curr:
                event = 'Door is Closed.'
                update.message.reply_text(event)
                log_event(event)
                doorOpen_prev = False

        if exit_condition == True:
            GPIO.cleanup()
            break

        time.sleep(0.5)


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


def start(bot, update):  # function for handling the /start command
    set_exit(False)
    update.message.reply_text('OK, begin monitoring...')
    t= threading.Thread(target=GPIOMonitor, args=[update])
    t.start()


def end(bot, update) :
    update.message.reply_text('OK, end monitoring...')
    set_exit(True)


def set_exit(bool):
    global exit_condition
    exit_condition = bool


def error_callback(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)
    # update.message.reply_text("Error, please restart.")

def main():
    print('Starting Telegram Bot...')
    updater = Updater(apiToken)  # fetches updates from telegram, gives to dispatcher
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))  # register with dispatcher
    dispatcher.add_handler(CommandHandler("end", end))
    dispatcher.add_handler(CommandHandler("log",log) )
    dispatcher.add_handler(CommandHandler('status', status))
    dispatcher.add_error_handler(error_callback)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
