from time import sleep

from Function.vid_orc import *
from Function.adb import *


class Home:
    def __init__(self, port):
        self.ADB_Controller = ADB_Controller(port)
        self.IMG_Recognition = IMG_Recognition()

    def go_home(self):
        sleep(1)
        while True:
            home = self.IMG_Recognition.Cutting_Search_Pictures(1, 1276, 1, 715, "picture/home.png", cv2.TM_CCOEFF_NORMED)
            back = self.IMG_Recognition.Cutting_Search_Pictures(1, 1276, 1, 715, "picture/back.png", cv2.TM_CCOEFF_NORMED)

            if home is not None:
                print("\n已回到首頁\n")
                break
            elif back is not None:
                self.ADB_Controller.click(back[0], back[1])
            else:
                self.ADB_Controller.click(18, 44)