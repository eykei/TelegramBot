'''
add config file
'''

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters)
import logging, time, threading, datetime
import RPi.GPIO as GPIO

apiToken='601155106:AAGVS0HLVhSpQeFx42USd8js7KkITcJNJiI'
exit=False
sensorPin=7
event_log=[]



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def GPIOMonitor(update):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(sensorPin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    doorOpen=GPIO.input(sensorPin)
    while True:
        print(GPIO.input(sensorPin))

        if GPIO.input(sensorPin):
            if not doorOpen:
                event='Doors is Open!'
                update.message.reply_text(event)
                log_event(event)
                doorOpen=True
        else:
            if doorOpen:
                event='Door is Closed.'
                update.message.reply_text(event)
                log_event(event)
                doorOpen=False

        if exit == True:
            GPIO.cleanup()
            break

        time.sleep(1)

def log_event(event):
    dt=datetime.datetime.now()
    l='%d/%d/%d %d:%d:%d %s' % (dt.month, dt.day, dt.year, dt.hour, dt.minute, dt.second, event)
    if len(event_log)>=30:
        del(event_log[0])
        event_log.append(l)
    else:
        event_log.append(l)

def log(bot,update):
    update.message.reply_text('OK, printing log...')
    time.sleep(1)
    for event in event_log:
        update.message.reply_text(event)

def clear(bot,update):
    global event_log
    event_log=[]

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
    dispatcher.add_handler(CommandHandler("log", log))
    dispatcher.add_handler(CommandHandler("log", log))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()

'''
#testing
import telegram
bot = telegram.Bot(token=apiToken) #API token provided by Botfather
print(bot.get_me())
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