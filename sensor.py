import RPi.GPIO as GPIO
import time


class Sensor():
    def __init__(self, name, type, pin):
        self.name = name  # e.g. Door 1, Basement
        self.type = type  # contact or motion
        self.pin = pin
        self.exit_condition = False
        GPIO.setmode(GPIO.BOARD)  # use the name of the pins by position
        if self.type == 'contact':
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # sensor reads high when door is open (door switch is on normally open)
        elif self.type == 'motion':
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        else:
            raise Exception('Unrecognized Sensor Type')
        print(self.name + ' activated!')

    def status(self, context, subscribers):
        if self.type == 'contact':
            if GPIO.input(self.pin):
                for subscriber in subscribers:
                    context.bot.send_message(subscriber, f'{self.name} is currently open.')
            else:
                for subscriber in subscribers:
                    context.bot.send_message(subscriber, f'{self.name} is currently closed.')
        elif self.type == 'motion':
            if GPIO.input(self.pin):
                for subscriber in subscribers:
                    context.bot.send_message(subscriber, f'{self.name} detects motion.')
            else:
                for subscriber in subscribers:
                    context.bot.send_message(subscriber, f'{self.name} does not detect motion.')
        else:
            raise Exception('Unrecognized Sensor Type')

    def monitor(self, context, subscribers):
        if self.type == 'contact':
            doorOpen_prev = GPIO.input(self.pin)
            while True:
                time.sleep(0.1)
                doorOpen_curr = GPIO.input(self.pin)
                if doorOpen_curr != doorOpen_prev:
                    if doorOpen_curr:  # if the door is currently open
                        for subscriber in subscribers:
                            context.bot.send_message(subscriber, f'{self.name} is open.')
                        doorOpen_prev = True
                    if not doorOpen_curr:
                        for subscriber in subscribers:
                            context.bot.send_message(subscriber, f'{self.name} is closed.')
                        doorOpen_prev = False

                if self.exit_condition:
                    # GPIO.cleanup()
                    return

        elif self.type == 'motion':
            while True:
                time.sleep(0.1)
                if GPIO.input(self.pin):
                    for subscriber in subscribers:
                        context.bot.send_message(subscriber, f'{self.name} detects motion.')
                    time.sleep(15)

                if self.exit_condition:
                    # GPIO.cleanup()
                    return
        else:
            raise Exception('Invalid Sensor Type')
