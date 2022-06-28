from multiprocessing import Process, Value
import time
from ctypes import c_bool  # to use boolean type in using multiprocess Value

#global variable cant be shared at different proceeses

MOTOR_TIC = 0
BUZZ_TIC = 1
LOGO_TIC = 2
LCD_TIC = 3
TIMEOUT = 4

MOTOR_INIT = 0
BUZZ_INIT = 1
LOGO_INIT = 2
LCD_INIT = 3
TIMEOUT_INIT = 4

tick = Value('i',0)
timer_flag = Value(c_bool, False)

actuators = ['motor','buzz','logo','lcd','timeout']

def _timer(tick,flag):
    
    while True:
        #print(flag)
        if flag.value == True:
            time.sleep(1)
            tick.value += 1
            print('TIMER',tick.value)

#def timer_enable(flag):
   

def timer_disable(flag):
    
    if flag == MOTOR_END:
        print("flag1 end")
        flags[MOTOR_TIC].value = False
    
    elif flag == BUZZ_END:
        flags[BUZZ_TIC].value = False
    
    elif flag == LOGO_END:
        print("flag2 end")
        flags[LOGO_TIC].value = False
        
    elif flag == LCD_END:
        flags[LCD_TIC].value = False
        
    elif flag == TIMEOUT_END:
        flags[TIMEOUT].value = False
        
        
        
        
        
            
def park_sys():
    timer_flag.value = True
    while True:
        if tick.value > 10:
            time.sleep(1)
            timer_flag.value = False
        
 


p_motor = Process(target = _timer, args=(tick,timer_flag))
p2 = Process(target = park_sys)

p_motor.start()
p2.start()