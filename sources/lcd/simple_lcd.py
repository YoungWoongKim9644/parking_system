import sys
sys.path.append('/home/pi/Desktop/parking_system/sources/lcd')
import I2C_LCD_driver
from time import *


class SimpleLCD(I2C_LCD_driver.Lcd):
	
	def print_string(self,string, line=1, pos=0):
		print(string)
		self.lcd_display_string(string, line, pos)
	
	def display_string_tmp(self,timer,string, line=1, pos=0):
		self.lcd_display_string(string, line, pos)
		sleep(timer)
		self.lcd_clear()
