import sys

sys.path.append('C:/Users/duddn/PycharmProjects/parking_system/parking_system/sources/mfrc')
# sys.path.append('/home/pi/Desktop/parking_system/sources/mfrc')

from multiprocessing import Process, Value
from time import *
# from sources.mfrc import MFRC
from sources.mfrc import simpleMFRC
from sources import motor
# from sources.lcd import I2C_LCD_driver
# from sources.lcd import simple_lcd
from sources import connection
from sources import timer

HOST = 'localhost'
PORT = 9999
TIMER_RESET = 0

MOTOR = 0
BUZZ = 1
LOGO = 2
LCD = 3
TIMEOUT = 4

if __name__ == '__main__':

    class ParkingSystem:

        def __init__(self, total_space=40):
            print("init")
            self.total_space = total_space
            self.current_space = self.total_space

            # self.lcd = I2C_LCD_driver.Lcd()
            self.mfrc = simpleMFRC.SimpleMFRC522()
            self.conn = connection.Client(HOST,PORT)
            self.motor = motor.Servo()
            print("init end")

        def system_init(self):
            print("sys_init")
            if self.mfrc.version_check() and self.conn.connection_init():
                self.motor.motor_check()
                # motor & buzzer init
                """
                self.lcd.display_string_tmp(1,"====================", 1, 2)
                self.lcd.display_string_tmp(1,"   Parking System   ", 2, 0)
                self.lcd.display_string_tmp(1,"       V.2          ", 3, 0)
                self.lcd.display_string_tmp(1,"====================", 4, 0)
                """

        def system_body(self):

            while True:

                uid = self.mfrc.read()
                print("id, text :", uid[0], uid[1])
                self.recv_data2str(uid)

                self.rc_522_data_state_check_and_actuate(uid)

                while True:

                    if timer.flags[MOTOR].value:

                        if timer.ticks[MOTOR].value > 100000:
                            self.motor.motor_set("CLOSE")
                            timer.timer_disable(MOTOR)
                            timer.ticks[MOTOR].value = TIMER_RESET

                    if timer.flags[LOGO].value:

                        if timer.ticks[LOGO].value > 100000:
                            self.logo_set("CLOSE")
                            timer.timer_disable(LOGO)
                            timer.ticks[LOGO].value = TIMER_RESET

                    if timer.flags[MOTOR].value is False and timer.flags[LOGO].value is False:
                        break

        def gate_open_close(self, status):
            self.motor.motor_set(status)
            self.buzzer_set(status)
            self.logojec_set(status)

        def buzzer_set(self, status):

            if status == "OPEN":
                pass

        def logo_set(self, status):

            if status == "OPEN":
                print("LOGO ON")
            if status == "CLOSE":
                print("LOGO OFF")

        def recv_data2str(self, uid):
            self.user_id_number = "user id:" + str(uid[0])
            print(self.user_id_number)

        def cal_empty_space(self, current):  # current is +- 1

            self.current_space += current
            self.empty_space = "       " + str(self.current_space) + "/" + str(self.total_space) + "       "
            print(self.current_space)
            print(self.empty_space)

        def rc_522_data_state_check_and_actuate(self, uid):

            if self.conn.is_registered(uid[0]):

                self.cal_empty_space(1)

                self.motor.motor_set("OPEN")
                timer.timer_enable(MOTOR)
                self.logo_set("OPEN")
                timer.timer_enable(LOGO)

                self.buzzer_set("OPEN")
                timer.timer_enable(BUZZ)

                # self.lcd.display_string(self.user_id_number, 2, 0)
                # self.lcd.display_string(self.empty_space, 3, 0)
                print(self.user_id_number)
                print(self.empty_space)

            else:
                print('{} : un registerd id'.format(uid[0]))

    p_motor = Process(target=timer._timer, args=(timer.ticks[MOTOR], timer.flags[MOTOR]))
    p_buzz = Process(target=timer._timer, args=(timer.ticks[BUZZ], timer.flags[BUZZ]))
    p_logo = Process(target=timer._timer, args=(timer.ticks[LOGO], timer.flags[LOGO]))
    p_lcd = Process(target=timer._timer, args=(timer.ticks[LCD], timer.flags[LCD]))
    p_timeout = Process(target=timer._timer, args=(timer.ticks[TIMEOUT], timer.flags[TIMEOUT]))

    p_motor.start()
    p_buzz.start()
    p_logo.start()
    p_lcd.start()
    p_timeout.start()


    print("system start")
    parking_sys = ParkingSystem()
    parking_sys.system_init()
    parking_sys.system_body()



