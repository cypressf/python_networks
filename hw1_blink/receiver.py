try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
from multiprocessing import Process, Queue

import time

input_values = []
words = []

class Receiver:
	"""
	Decodes an incomming morse code message
	"""

	def __init__(self, transmitter, address="c", input_pin=24, minimum_blink_time=100):
		self.body = ""
		self.header = ""
		self.address = address
		self.running = True
		self.bits = []
		self.waiting_for_new_word = True
		self.waiting_for_header = True
		self.minimum_blink_time = minimum_blink_time
		self.transmitter = transmitter
		self.input_pin = input_pin
		GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)
		GPIO.setup(self.input_pin, GPIO.IN)
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

		self.process = Process(target=self.read_loop)
		self.process.start()

	def add_bit(self, bit):
		"""
		Given a new bit, process the bit queue.
		"""
		# A new word is arriving
		if bit == 1 and self.waiting_for_new_word:
			self.waiting_for_new_word = False

		# We're waiting for a new word, and there is a stream
		# of 0s, so lets just ignore all of them. It's silence.
		if bit == 0 and self.waiting_for_new_word:
			self.bits = []

		# A new bit arrived! Append it to our bits list.
		else:
			self.bits.append(bit)

		# We received seven 0s in a row, which means we insert a space.
		if self.bits[-7:] == [0,0,0,0]:
			self.add_space()

		elif self.bits[-3:] == [0,0,0] and 1 in self.bits:
			# starting new character
			self.add_character()
		


	def add_space(self):
		# If this is the end of the header, check the address.
		if self.waiting_for_header:
			self.waiting_for_header = False

			# the message is addressed to us!
			if self.header == self.address:
				print("Here comes our message!")

			# the message is not addressed to us. forward the header
			else:
				print("\nForwarding a message to", self.header)
				self.transmitter.add_to_queue(self.header + " ")

		# this is an ordinary space in the body
		elif self.header == self.address:
			self.body += " "
		
		else:
			self.body += " "
			self.transmitter.add_to_queue(" ")
		
		# clear the bit queue
		self.bits = []
		self.waiting_for_new_word = True

	def add_character(self):
		bitstring = "".join([str(bit) for bit in self.bits[:-3]])
		if bitstring in self.morse_code:
			character = self.morse_code[bitstring]

			# we're reading in the header right now
			if self.waiting_for_header:
				self.header += character

			# we're reading in the body right now, and it's our message
			elif self.header == self.address:
				# end of message. wait for the next header
				if character == "/":
					self.waiting_for_new_word = True
					self.waiting_for_header = True
					self.header = ""
					self.body = ""
					print(bitstring, "<end of message>")
				else:
					self.body += character
				print(self.body)

			# we need to pass the message along to someone else
			else:
				if character == "/":
					self.waiting_for_new_word = True
					self.waiting_for_header = True
					self.header = ""
					self.body = ""
					print(bitstring, "<end of message>")
				else:
					self.body += character
				print(self.body)
				self.transmitter.add_to_queue(character)

		else:
			print(bitstring, "<no match>")
		self.bits = []

	def cleanup(self):
		"""
		So the child process doesn't live forever
		"""
		self.running = False

	def read_loop(self):
		"""
		Continually read the input
		"""
		start_time = time.time()
		previous_num_intervals = 0

		while self.running:
			input_value = GPIO.input(self.input_pin)
			
			# flip input, so LIGHT is 1, DARK is 0
			if input_value:
				input_value = 0
			else:
				input_value = 1

			time_passed = (time.time() - start_time) * 1000
			num_intervals = int(time_passed / self.minimum_blink_time)

			if num_intervals > previous_num_intervals:
				input_values.append(input_value)
				previous_num_intervals = num_intervals
				self.add_bit(input_value)

			# so we don't max out the CPU
			time.sleep(0.001)