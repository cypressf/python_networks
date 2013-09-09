try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

import time

INPUT_PIN = 24
OUTPUT_PIN = 26

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(OUTPUT_PIN, GPIO.OUT)
GPIO.setup(INPUT_PIN, GPIO.IN)

led_is_on = 0
input_values = []
while True:
	input_values.append(GPIO.input(INPUT_PIN))
	
	print("input pin" + str(input_values))
	GPIO.output(OUTPUT_PIN, led_is_on)
	
	if led_is_on:
		led_is_on = 0
	else:
		led_is_on = 1
	time.sleep(1)