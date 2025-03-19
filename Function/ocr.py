from pponnxcr import TextSystem
from Function.adb_controller import *
import cv2

class OCR_Recognition():
    def __init__(self,port=5560):
        self.adb = ADB_Controller(port)
    def Cutting_Ocr_Pictures(self,x_start, x_end, y_start, y_end,text,timeout=2):
        start_time = time.time()
        while time.time() - start_time < timeout:
            self.adb.screenshot()
            # ZHT = TextSystem('zht')  # 繁体中文
            # JA = TextSystem('ja')    # 日文
            # EN = TextSystem('en')    # 英文
            ZHS = TextSystem('zhs')  # 简体中文
            img = cv2.imread('screenshot.png')
            cropped_img = img[y_start:y_end, x_start:x_end]
            result_detect = ZHS.detect_and_ocr(cropped_img)
            for i in result_detect:
                if i.text == text:
                    cx = int((i.box[0][0] + i.box[2][0]) / 2 + x_start)
                    cy = int((i.box[0][1] + i.box[2][1]) / 2 + y_start)
                    return cx,cy
                else:
                    continue

    def Detect_Text_Area(self,x_start, x_end, y_start, y_end):
        #找特定區域出現的文字
        # ZHT = TextSystem('zht')  # 繁体中文
        # JA = TextSystem('ja')    # 日文
        # EN = TextSystem('en')    # 英文
        ZHS = TextSystem('zhs')  # 简体中文
        img = cv2.imread('screenshot.png')
        cropped_img = img[y_start:y_end, x_start:x_end]
        result_detect = ZHS.detect_and_ocr(cropped_img)
        if result_detect:
            return result_detect[0].text

    def Get_Square_Coordinates(self,x, y, size):
        half_size = size // 2
        return {
            "x_start": x - half_size,
            "x_end": x + half_size,
            "y_start":  y - half_size,
            "y_end":  y + half_size,
        }