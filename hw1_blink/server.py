from transmitter import Transmitter
from receiver import Receiver
import atexit

SEND_ADDRESS = "1"
RECEIVE_ADDRESS = "c"
MINIMUM_BLINK_TIME = 1000

if __name__ == '__main__':
	transmitter = Transmitter(minimum_blink_time = MINIMUM_BLINK_TIME, send_address = SEND_ADDRESS)
	receiver = Receiver(transmitter, minimum_blink_time = MINIMUM_BLINK_TIME, address = RECEIVE_ADDRESS)
	
	def cleanup():
		transmitter.cleanup()
		receiver.cleanup()

	atexit.register(cleanup)

	while True:
		message = input("message: ")
		transmitter.send(message)
