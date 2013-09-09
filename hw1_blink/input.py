try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

import time

INPUT_PIN = 24

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(INPUT_PIN, GPIO.IN)

input_values = []
while True:
	input_value = GPIO.input(INPUT_PIN)

	if not input_values:
		input_values.append(input_value)
		print(input_value)

	elif input_value != input_values[-1]:
		input_values.append(input_value)
		print(input_value)
	

	time.sleep(.0001)