from transmitter import Transmitter
# from receiver import Receiver
import atexit

ADDRESS = "e"
MINIMUM_BLINK_TIME = 100

if __name__ == '__main__':
	transmitter = Transmitter(minimum_blink_time=MINIMUM_BLINK_TIME)
	atexit.register(transmitter.cleanup)
	while True:
		message = input("message: ")
		transmitter.send_message(message, ADDRESS)
		# receiver = Receiver()
		# start_time = time.time()
		# previous_num_intervals = 0
		# input_value = GPIO.input(self.input_pin)
		# if input_value:
		# 	input_value = 0
		# else:
		# 	input_value = 1
		# time_passed = (time.time() - start_time) * 1000
		# num_intervals = int(time_passed / minimum_blink_time)
		# if num_intervals > previous_num_intervals:
		# 	input_values.append(input_value)
		# 	previous_num_intervals = num_intervals
		# 	decoder.add_bit(input_value)
		# time.sleep(0.001)