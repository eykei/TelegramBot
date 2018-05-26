#install package: python-telgram-bot
from telegram.ext import (Updater, CommandHandler)
import logging, time, threading
import RPi.GPIO as GPIO

'''
add function to log events
'''

apiToken='601155106:AAGVS0HLVhSpQeFx42USd8js7KkITcJNJiI'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

exit=False
sensorPin=8
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensorPin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)


def GPIOMonitor(update):
    while True:
        if GPIO.input(sensorPin):
            update.message.reply_text('Door is Open!')
        if exit == True:
            GPIO.cleanup()
            break

        time.sleep(1)

def start(update,context):
    update.message.reply_text('OK, begin monitoring...')
    t=threading.Thread(target=GPIOMonitor, args=[update])
    t.start()
    global exit
    set_exit(False)

def end(update,context):
    update.message.reply_text('OK, end monitoring...')
    set_exit(True)

def set_exit(bool):
    global exit
    exit=bool


def main():
    updater = Updater(apiToken, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("end", end))
    #updater.bot.send_message(chat_id,'sup dude')
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()