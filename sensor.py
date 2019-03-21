import RPi.GPIO as GPIO
import time


class Sensor():
    def __init__(self, name, type, pin):
        self.name = name  # e.g. Door 1, Basement
        self.type = type  # contact or motion
        self.pin = pin
        self.exit_condition = False
        print(self.name + ' activated!')

    def status(self, update):
        GPIO.setmode(GPIO.BOARD)  # use the name of the pins by position
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # sensor reads high when door is open (door switch is on normally closed)
        if self.type == 'contact':
            if GPIO.input(self.pin):
                update.message.reply_text('{} is currently Open.'.format(self.name))
            else:
                update.message.reply_text('{} is currently Closed.'.format(self.name))
        elif self.type == 'motion':
            if GPIO.input(self.pin):
                update.message.reply_text('{} currently detects motion.'.format(self.name))
            else:
                update.message.reply_text('{} currently detects no motion.'.format(self.name))
        else:
            raise Exception('Unrecognized Sensor Type')

    def monitor(self, update):
        GPIO.setmode(GPIO.BOARD)  # use the name of the pins by position
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # sensor reads high when door is open (door switch is on normally closed)
        if self.type == 'contact':
            doorOpen_prev = GPIO.input(self.pin)
            while True:
                doorOpen_curr = GPIO.input(self.pin)

                if doorOpen_curr != doorOpen_prev:
                    if doorOpen_curr:  # if the door is currently open
                        event = '{} is Open.'.format(self.name)
                        update.message.reply_text(event)
                        #log_event(event)
                        doorOpen_prev = True
                    if not doorOpen_curr:
                        event = '{} is Closed.'.format(self.name)
                        update.message.reply_text(event)
                        #log_event(event)
                        doorOpen_prev = False

                if self.exit_condition:
                    # GPIO.cleanup()
                    return

                time.sleep(0.5)

        elif self.type == 'motion':
            while True:
                if GPIO.input(self.pin):
                    event = '{} detects motion.'.format(self.name)
                    update.message.reply_text(event)
                    time.sleep(15)

                if self.exit_condition:
                    # GPIO.cleanup()
                    return
        else:
            raise Exception('Invalid Sensor Type')

