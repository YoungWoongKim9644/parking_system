import I2C_LCD_driver
from client import Client
from time import *

my_lcd = I2C_LCD_driver.Lcd()
my_lcd.lcd_display_string("Hello World",1)
my_lcd.lcd_display_string("raspberry pi",2)
print("")


HOST = 'localhost'

PORT = 9999


client = Client(HOST,PORT)

client.connection_init()

while True:
	msg = input("input: ")
	if msg == 'x':
		client.con_close()
		break
	client.write_msg(msg)
	
	
