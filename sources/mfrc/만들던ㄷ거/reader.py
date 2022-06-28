from mfrc522 import MFRC522
from constant import Args
import RPi.GPIO as GPIO


class Reader(Args):

    KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    BLOCK_ADDRS = [8, 9, 10]

    def __init__(self):
        self.mfrc = MFRC522()

    def read_id_no_block(self):

        (status, tag_type) = self.mfrc.request_MFRC(Args.PICC_REQIDL)
        print(status, tag_type)
        if status != Args.MI_OK:
            return None

        (status, uid) = self.mfrc.anticoll_mfrc()
        if status != Args.MI_OK:
            return None

        return self.uid2num(uid)
    
    def read_id(self):
        id = self.read_id_no_block()
        while not id:
            id = self.read_id_no_block()
        return id

    def uid2num(self, uid):

        n = 0
        for i in range(0, 5):
            n = n * 256 + uid[i]

        return n