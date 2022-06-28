from multiprocessing import Process, Value
import time
from ctypes import c_bool  # to use boolean type in using multiprocess Value

#global variable cant be shared at different proceeses
# 1 sec ~= 1000 ticks

MOTOR = 0
BUZZ = 1
LOGO = 2
LCD = 3
TIMEOUT = 4

ticks = [Value('i',0)]*5
flags = [Value(c_bool, False)]*5


def _timer(tick,flag):
    
    while True:
        #print(flag)
        if flag.value == True:
            tick.value += 1
            print(tick.value)

def timer_enable(flag):
	
    print("flag : ",flag)
    if flag == MOTOR:
        print("flag1 move")
        flags[MOTOR].value = True
    
    elif flag == BUZZ:
        flags[BUZZ].value = True
    
    elif flag == LOGO:
        print("flag2 move")
        flags[LOGO].value = True
        
    elif flag == LCD:
        flags[LCD].value = True
        
    elif flag == TIMEOUT:
        flags[TIMEOUT].value = True


def timer_disable(flag):
    
    if flag == MOTOR:
        print("flag1 end")
        flags[MOTOR].value = False
    
    elif flag == BUZZ:
        flags[BUZZ].value = False
    
    elif flag == LOGO:
        print("flag2 end")
        flags[LOGO].value = False
        
    elif flag == LCD:
        flags[LCD].value = False
        
    elif flag == TIMEOUT:
        flags[TIMEOUT].value = False
        
        
        
        
        
"""            
def park_sys():
		
    timer_enable(MOTOR_INIT)
    while True:
	
        time.sleep(1)
        print(ticks[MOTOR_TIC].value)
        if ticks[MOTOR_TIC].value > 3:
            
            timer_disable(MOTOR_END)            
            ticks[MOTOR_TIC].value = 0
            
            timer_enable(LOGO_INIT)
        
        if ticks[LOGO_TIC].value > 3:
            
            timer_disable(LOGO_END)
            ticks[MOTOR_TIC].value = 0
            
            timer_enable(MOTOR_INIT)
"""

"""
start = time.time()
timer_enable(MOTOR)
while True:
    if ticks[MOTOR].value > 1095:
        print("end")
        timer_disable(MOTOR)
        break
print("time: ", time.time() - start)
"""