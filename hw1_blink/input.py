try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
from multiprocessing import Process

import time

INPUT_PIN = 24
minimum_blink_time = 1000 # milliseconds

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(INPUT_PIN, GPIO.IN)

input_values = []
words = []

class Decoder:
	"""
	Decodes an incomming morse code message
	"""

	def __init__(self):
		self.body = ""
		self.header = ""
		address = "c"
		is_first_word = True
		self.bits = []
		self.waiting_for_new_word = True
		self.waiting_for_header = True
		self.morse_code = {
			"10111": "a",
			"111010101": "b",
			"11101011101": "c",
			"1110101": "d",
			"1": "e",
			"101011101": "f",
			"111011101": "g",
			"1010101": "h",
			"101": "i",
			"1011101110111": "j",
			"111010111": "k",
			"101110101": "l",
			"1110111": "m",
			"11101": "n",
			"11101110111": "o",
			"10111011101": "p",
			"1110111010111": "q",
			"1011101": "r",
			"10101": "s",
			"111": "t",
			"1010111": "u",
			"101010111": "v",
			"101110111": "w",
			"11101010111": "x",
			"1110101110111": "y",
			"11101110101": "z",
			"10111011101110111": "1",
			"101011101110111": "2",
			"1010101110111": "3",
			"10101010111": "4",
			"101010101": "5",
			"11101010101": "6",
			"1110111010101": "7",
			"111011101110101": "8",
			"11101110111011101": "9",
			"1110111011101110111": "0",
			"101010111010111": "/"
		}

	def add_bit(self, bit):
		if bit == 1 and self.waiting_for_new_word:
			self.waiting_for_new_word = False

		if bit == 0 and self.waiting_for_new_word:
			self.bits = []
		else:
			self.bits.append(bit)

		if self.bits[-7:] == [0,0,0,0]:
			# starting a new word
			self.add_space()

		elif self.bits[-3:] == [0,0,0] and 1 in self.bits:
			# starting new character
			self.add_character()

		print(self.bits)

	def add_space(self):
		# if this is the end of the header,
		# check the address
		if self.waiting_for_header:
			self.waiting_for_header = False
			self.

		self.body += " "
		self.bits = []
		self.waiting_for_new_word = True


	def add_character(self):
		bitstring = "".join([str(bit) for bit in self.bits[:-3]])
		if bitstring in self.morse_code:
			if self.morse_code(bitstring) == "/":
				# end of message character
				self.waiting_for_header = True
				print(bitstring, "<end of message>")
			else:
				self.body += self.morse_code[bitstring]
				print(self.body)
		else:
			print(bitstring, "<no match>")
		self.bits = []


decoder = Decoder()
start_time = time.time()
previous_num_intervals = 0
while True:
	input_value = GPIO.input(INPUT_PIN)
	if input_value:
		input_value = 0
	else:
		input_value = 1
	time_passed = (time.time() - start_time) * 1000
	num_intervals = int(time_passed / minimum_blink_time)
	if num_intervals > previous_num_intervals:
		input_values.append(input_value)
		previous_num_intervals = num_intervals
		decoder.add_bit(input_value)
	time.sleep(0.001)