Instructions-------------------------------------------
Hardware----

Software---


On the Raspberry Pi, navigate to TelegramBot Folder.
Open config.ini
In the setting section, set the apiToken that BotFather gives you.

To configure sensors, add sections following this format:
[sensorX]                   << doesn't matter what it's called
name = sensorName           << pick a name (e.g. door, basement)
type = sensorType           << select type of sensor, either contact (magnetic reed) or motion (passive infrared)
pin = X						<< select GPIO pin that sensor is connected to 

Run the program from the command line.
>sudo python3 TelegramBotV3.py

In Telegram, add your bot. Enter commands by simply sending your bot a message. Available commands described below.

/subscribe
Subscribe to alert messages.

/unsubscribe
Unsubscribe to alert messages.

/home
Arm the system for home. Only contact sensors will be active.

/away
Arm the system for away. Both contact and motion sensors will be active.

/disarm
Disarm all sensors.

/status
Reports the current sensors' readings. Useful to tell if a door is open or closed.

When a sensor is tripped, the bot will send a message in the format of:

For contact sensors:
SensorName is Open.
SensorName is Closed.

For motion sensors:
SensorName detects Motion.



Notes:
The door sensor has two wires hooked up to NO/COM (Normally Open/Common).
On the Pi side, the two wires are connected to Ground, and a GPIO pin with a pullup resistor. 

When the door is closed, (magnet next to sensor) the switch closes, and the GPIO pin reads low.
When the door is opened, (magnet away from sensor) the switch opens, and the GPIO pin reads high due to pullup resistor.