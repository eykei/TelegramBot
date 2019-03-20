import RPi.GPIO as GPIO
import time

class Sensor():
    def __init__(self, name, type, pin):
        self.name = name  # e.g. Door 1, Basement
        self.type = type  # contact or motion
        self.pin = pin

        self.exit_condition = False


    def monitor(self, update):
        GPIO.setmode(GPIO.BOARD)  # use the name of the pins by position
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # sensor reads high when door is open (door switch is on normally closed)
        if self.type == 'contact':
            doorOpen_prev = GPIO.input(self.pin)
            while True:
                doorOpen_curr = GPIO.input(self.pin)

                if doorOpen_curr != doorOpen_prev:
                    if doorOpen_curr:  # if the door is currently open
                        event = '{} is Open!'.format(self.name)
                        update.message.reply_text(event)
                        #log_event(event)
                        doorOpen_prev = True
                    if not doorOpen_curr:
                        event = '{} is Closed.'.format(self.name)
                        update.message.reply_text(event)
                        #log_event(event)
                        doorOpen_prev = False

                if self.exit_condition == True:
                    GPIO.cleanup()
                    return

                time.sleep(0.5)

        elif self.type == 'motion':
            while True:
                if GPIO.input(self.pin):
                    event = '{}: motion detected!'.format(self.name)
                    update.message.reply_text(event)
                    time.sleep(10)

                if self.exit_condition == True:
                    GPIO.cleanup()
                    return
        else:
            raise Exception('Invalid Sensor Type')

