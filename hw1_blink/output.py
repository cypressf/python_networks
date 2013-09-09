try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

import time

OUTPUT_PIN = 26

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(OUTPUT_PIN, GPIO.OUT)

led_is_on = 0
while True:
	GPIO.output(OUTPUT_PIN, led_is_on)
	
	if led_is_on:
		led_is_on = 0
	else:
		led_is_on = 1
	time.sleep(0.06)