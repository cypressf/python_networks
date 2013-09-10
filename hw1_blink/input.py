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
words = []

start_time = time.time()
minimum_blink_time = 50 # milliseconds
previous_num_intervals = 0
while True:
	input_value = GPIO.input(INPUT_PIN)
	time_passed = (time.time() - start_time) * 1000
	num_intervals = int(time_passed / minimum_blink_time)
	if num_intervals > previous_num_intervals:
		input_values.append(input_value)
		previous_num_intervals = num_intervals
		print(input_value)
	time.sleep(0.001)