#import RPi.GPIO as GPIO
import time

MAX_DEG = 120
MIN_DEG = 20
GET_OPEN = 3.5
GET_CLOSE = 9

class Servo:
    
    def __init__(self, pin=12):

        self.pin = pin
        """
        #GPIO.setmode(GPIO.BCM) # use pin number
        GPIO.setup(pin, GPIO.OUT) # set pin as output port
        self.pwm = GPIO.PWM(pin, 50)
        self.pwm.start(0)
        """

    def motor_check(self):
        
        print("motor_check")
        """
        try:
            for deg in range(MIN_DEG, MAX_DEG):
                self.pwm.ChangeDutyCycle(deg/10)
                time.sleep(0.01)
            
            return True
        
        except KeyboardInterrupt:
            self.pwm.stop()
            print("motor error occured")
            return False
        """

    def motor_set(self,status):

        if status == "OPEN":
            print("motor open")
            """
            self.pwm.ChangeDutyCycle(GET_OPEN)
            """
        if status == "CLOSE":
            print("motor close")
            """
            self.pwm.ChaneDutyCycle(GET_CLOSE)
            """

    
"""
try:
	while True:
		p.ChangeDutyCycle(3.5)
		print("angle : 1")
		time.sleep(2)
		p.ChangeDutyCycle(9)
		print("angle : 5")
		time.sleep(2)
except KeyboardInterrupt:
	p.stop()
GPIO.cleanup()
"""