from reader import Reader
import RPi.GPIO as GPIO

reader = Reader()

try:
	print(reader.read_id())
finally:
	GPIO.cleanup()
