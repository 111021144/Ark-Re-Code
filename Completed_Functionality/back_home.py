from time import sleep
from Function.ocr import *
from Function.adb_controller import *


class Home:
    def __init__(self, port):
        self.ADB_Controller = ADB_Controller(port)
        self.OCR_Recognition = OCR_Recognition(port)
    def go_home(self):
        sleep(1)
        while True:
            home = self.OCR_Recognition.Cutting_Ocr_Pictures(910, 1071, 263, 307, "战斗通行证",timeout=0.1)
            back = self.OCR_Recognition.Cutting_Ocr_Pictures(69, 131, 17, 57, "返回",timeout=0.1)
            if home is not None:
                print("\n已回到首頁\n")
                sleep(1)
                break
            elif back is not None:
                self.ADB_Controller.click(back[0], back[1])
            else:
                self.ADB_Controller.click(18, 44)