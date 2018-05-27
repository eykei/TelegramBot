'''
#testing
import telegram
bot = telegram.Bot(token=apiToken) #API token provided by Botfather
print(bot.get_me())
'''

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters)
import logging, time, threading
import RPi.GPIO as GPIO

apiToken='601155106:AAGVS0HLVhSpQeFx42USd8js7KkITcJNJiI'
exit=False
sensorPin=7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensorPin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def GPIOMonitor(update):
    while True:
        print(GPIO.input(sensorPin))
        if GPIO.input(sensorPin):
            update.message.reply_text('Door is Open!')
        if exit == True:
            GPIO.cleanup()
            break
        time.sleep(1)

def start(bot, update): #function for handling the /start command
    update.message.reply_text('OK, begin monitoring...')
    t=threading.Thread(target=GPIOMonitor, args=[update])
    t.start()
    global exit
    set_exit(False)

def end(bot,update):
    update.message.reply_text('OK, end monitoring...')
    set_exit(True)

def set_exit(bool):
    global exit
    exit = bool

def main():
    updater = Updater(apiToken)  # fetches updates from telegram, gives to dispatcher
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start)) #register with dispatcher
    dispatcher.add_handler(CommandHandler("end", end))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()

'''
#Example functions
def echo(bot, update): #e.g. user: hello bot: hello
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

echo_handler = MessageHandler(Filters.text, echo) #Filters class contains contents of message (images, text, etc.)
dispatcher.add_handler(echo_handler)

def caps(bot, update, args): #e.g. user: /caps hello bot: HELLO
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)

caps_handler = CommandHandler('caps', caps, pass_args=True) #pass arguments after /caps as a list delimited by spaces
dispatcher.add_handler(caps_handler)
'''