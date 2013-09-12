try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

from multiprocessing import Process, Queue
import time

class Transmitter:
	def __init__(self, output_pin=26, minimum_blink_time=100):
		self.output_pin = output_pin
		GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)
		GPIO.setup(output_pin, GPIO.OUT)
		self.minimum_blink_time = minimum_blink_time # milliseconds
		self.bit_queue = Queue()
		self.running = True
		self.morse_code = {
			"a": [1,0,1,1,1,0,0,0],
			"b": [1,1,1,0,1,0,1,0,1,0,0,0],
			"c": [1,1,1,0,1,0,1,1,1,0,1,0,0,0],
			"d": [1,1,1,0,1,0,1,0,0,0],
			"e": [1,0,0,0],
			"f": [1,0,1,0,1,1,1,0,1,0,0,0],
			"g": [1,1,1,0,1,1,1,0,1,0,0,0],
			"h": [1,0,1,0,1,0,1,0,0,0],
			"i": [1,0,1,0,0,0],
			"j": [1,0,1,1,1,0,1,1,1,0,1,1,1,0,0,0],
			"k": [1,1,1,0,1,0,1,1,1,0,0,0],
			"l": [1,0,1,1,1,0,1,0,1,0,0,0],
			"m": [1,1,1,0,1,1,1,0,0,0],
			"n": [1,1,1,0,1,0,0,0],
			"o": [1,1,1,0,1,1,1,0,1,1,1,0,0,0],
			"p": [1,0,1,1,1,0,1,1,1,0,1,0,0,0],
			"q": [1,1,1,0,1,1,1,0,1,0,1,1,1,0,0,0],
			"r": [1,0,1,1,1,0,1,0,0,0],
			"s": [1,0,1,0,1,0,0,0],
			"t": [1,1,1,0,0,0],
			"u": [1,0,1,0,1,1,1,0,0,0],
			"v": [1,0,1,0,1,0,1,1,1,0,0,0],
			"w": [1,0,1,1,1,0,1,1,1,0,0,0],
			"x": [1,1,1,0,1,0,1,0,1,1,1,0,0,0],
			"y": [1,1,1,0,1,0,1,1,1,0,1,1,1,0,0,0],
			"z": [1,1,1,0,1,1,1,0,1,0,1,0,0,0],
			"1": [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,0,0],
			"2": [1,0,1,0,1,1,1,0,1,1,1,0,1,1,1,0,0,0],
			"3": [1,0,1,0,1,0,1,1,1,0,1,1,1,0,0,0],
			"4": [1,0,1,0,1,0,1,0,1,1,1,0,0,0],
			"5": [1,0,1,0,1,0,1,0,1,0,0,0],
			"6": [1,1,1,0,1,0,1,0,1,0,1,0,0,0],
			"7": [1,1,1,0,1,1,1,0,1,0,1,0,1,0,0,0],
			"8": [1,1,1,0,1,1,1,0,1,1,1,0,1,0,1,0,0,0],
			"9": [1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,0,0,0],
			"0": [1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,0,0],
			" ": [0, 0, 0, 0],
			"/": [1,0,1,0,1,0,1,1,1,0,1,0,1,1,1,0,0,0]
		}

		self.process = Process(target=self.message_loop)
		self.process.start()


	def send_message(self, message, address):
		"""
		Given a message body and address to send, add it to the queue, and send it when ready.
		"""
		message_string = address + " " + message + " /"
		for character in message_string:
			if character in self.morse_code:
				morse_code_list = self.morse_code[character]
				for bit in morse_code_list:
					self.bit_queue.put(bit)

	def message_loop(self):
		while self.running:
			led_state = int(self.bit_queue.get())
			GPIO.output(self.output_pin, led_state)
			time.sleep(self.minimum_blink_time / 1000)

	def cleanup(self):
		self.running = False