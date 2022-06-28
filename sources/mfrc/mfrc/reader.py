import RPi.GPIO as GPIO
from SimpleMFRC import SimpleMFRC522

reader = SimpleMFRC522()

try:
	id, text = reader.read()
	print(id)
	print(text)

finally:
	GPIO.cleanup()
