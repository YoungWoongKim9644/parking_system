import RPi.GPIO as GPIO
import spidev
import signal
import time
import logging
from constant import Args


class MFRC522(Args):

    def __init__(self,
                 bus=0,
                 device=0,
                 speed=1000000,
                 pin=10,
                 pin_rst=-1,
                 debug_level='WARNING',
                 ):

        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = speed

        self.logger = logging.getLogger('mfrc522Logger')
        self.logger.addHandler(logging.StreamHandler())  # handler : 로깅한 정보가 출력되는 위치설정
        level = logging.getLevelName(debug_level)
        self.logger.setLevel(level)

        gpio_mode = GPIO.getmode()

        """
        -1 if GPIO.setmode() is not set
        11 if GPIO.setmode(GPIO.BCM) is active
        10 if GPIO.setmode(GPIO.BOARD) is active
        
        """

        if gpio_mode is None:  # setmode 먼저 안하고도 가능한가?
            GPIO.setmode(pin)
        else:
            pin = gpio_mode

        if pin_rst == -1:
            pin_rst = 15 if pin == 11 else 22

        GPIO.setup(pin_rst, GPIO.OUT)
        GPIO.output(pin_rst, 1)
        self.init_mfrc()

    def reset_mfrc(self):
        self.write_mfrc(Args.CommandReg, Args.PCD_IDLE)

    def read_mfrc(self, addr):
        val = self.spi.xfer2([((addr << 1) & Args.ADDR_MASK) | Args.MSB_MASK, 0])  # 0x80 = 1000 0000 read = (MSB == 1)
        return val[1]

    def write_mfrc(self, addr, val):  # address에 value을 write
        val = self.spi.xfer2([((addr << 1) & Args.ADDR_MASK), val])

    def close_mfrc(self):
        self.spi.clse()
        GPIO.cleanup()

    def set_bit_mask(self, reg, mask):
        self.write_mfrc(reg, self.read_mfrc(reg) | mask)

    def clear_bit_mask(self,reg, mask):
        self.write_mfrc(reg, self.read_mfrc(reg) & (~mask))

    def antenna_on(self):
        temp = self.read_mfrc(Args.TxControlReg)
        if ~(temp & 0x03):
            self.set_bit_mask(Args.TxControlReg, 0x03)

    def antenna_off(self):
        self.ClearBitMask(self.TxControlReg, 0x03)

    # 0x03: TxControlReg 에서 0x03은 각 TX1과 TX2의 activation 을 제어

    def m2card(self, command, send_data):
        back_data = []
        back_len = 0
        status = Args.MI_ERR
        irqEn = 0x00
        waitIRq = 0x00
        lastBits = None
        n = 0
        
        if command == Args.PCD_AUTHENT:
            irqEn = 0x12
            waitIRq = 0x10
            
        if command == Args.PCD_TRANSCEIVE:
            irqEn = 0x77
            waitIRq = 0x30

        self.write_mfrc(Args.CommIEnReg, irqEn | Args.MSB_MASK)
        self.clear_bit_mask(Args.CommIEnReg, Args.MSB_MASK)
        self.set_bit_mask(Args.FIFODataReg, Args.MSB_MASK)

        self.write_mfrc(Args.CommIEnReg, Args.PCD_IDLE)

        for i in range(len(send_data)):
            self.write_mfrc(Args.FIFODataReg, send_data[i])

        self.write_mfrc(Args.CommandReg, command)

        if command == Args.PCD_TRANSCEIVE:
            self.set_bit_mask(Args.BitFramingReg, Args.MSB_MASK)

        i = 2000
        
        while True:
            n = self.read_mfrc(Args.CommIrqReg)
            print("inner n",n)
            i -= 1
            if ~((i != 0) and ~(n & 0x01) and ~(n & waitIRq)):
                break

        self.clear_bit_mask(Args.BitFramingReg, Args.MSB_MASK)
        print("i",i)
        if i != 0:
            if (self.read_mfrc(Args.ErrorReg) & 0x1B) == 0x00:
                status = Args.MI_OK

                if n & irqEn & 0x01:
                    status = Args.MI_NOTAGERR

                if command == Args.PCD_TRANSCEIVE:
                    n = self.read_mfrc(Args.FIFOLevelReg)
                    print("n1",n)
                    lastBits = self.read_mfrc(Args.ControlReg) & 0x07

                    if lastBits != 0:
                        back_len = (n - 1) * 8 + lastBits
                    else:
                        back_len = n * 8
                    
                    print("n:",n)
                    if n == 0:
                        n = 1
                    if n > Args.MAX_LEN:
                        n = Args.MAX_LEN

                    for i in range(n):
                        back_data.append(self.read_mfrc(Args.FIFODataReg))

            else:
                status = Args.MI_ERR

        return status, back_data, back_len

    def request_MFRC(self, reqmode):

        status = None
        back_bits = None
        tag_type = []

        self.write_mfrc(Args.BitFramingReg, 0x07)
        # TxLastbit define[2:0]

        tag_type.append(reqmode)
        (status, back_data, back_bits) = self.m2card(Args.PCD_TRANSCEIVE, tag_type)
        print(status, back_data, back_bits)
        if (status != Args.MI_OK) | (back_bits != 0x10):
            status = Args.MI_ERR

        return status, back_bits

    def anticoll_mfrc(self):

        back_data = []
        ser_num_check = 0
        ser_num = []

        self.write_mfrc(Args.BitFramingReg, 0x00)

        ser_num.append(Args.PICC_ANTICOLL)
        ser_num.append(0x20)

        status, back_data, back_bits = self.m2card(Args.PCD_TRANSCEIVE, ser_num)

        if status == Args.MI_OK:
            i = 0
            if len(back_data) == 5:
                for i in range(4):
                    ser_num_check = ser_num_check ^ back_data[i]
                if ser_num_check != back_data[4]:
                    status = Args.MI_ERR

            else:
                status = Args.MI_ERR

        return status, back_data

    def init_mfrc(self):

        self.reset_mfrc()

        self.write_mfrc(Args.TModeReg, 0x8D)  # timer setup
        self.write_mfrc(Args.TPrescalerReg, 0x3E)  # timer setup
        self.write_mfrc(Args.TReloadRegL, 30)
        self.write_mfrc(Args.TReloadRegH, 0)

        self.write_mfrc(Args.TxAutoReg, 0x40)
        self.write_mfrc(Args.ModeReg, 0x3D)
        self.antenna_on()
