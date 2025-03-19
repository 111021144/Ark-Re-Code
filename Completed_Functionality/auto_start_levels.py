from Function.vid import *
from Function.ocr import *

class LevelsAutomation:
    def __init__(self, port=5560):
        self.ADB_Controller = ADB_Controller(port)
        self.IMG_Recognition = IMG_Recognition(port)
        self.OCR_Recognition = OCR_Recognition(port)
    def Automatic_Level(self):
        while True:
            self.ADB_Controller.screenshot()
            Complete_task = self.OCR_Recognition.Cutting_Ocr_Pictures(1, 1280, 1, 1280, '完成任务',timeout=0.1)
            if Complete_task:
                print("完成任务")
                self.ADB_Controller.click(Complete_task[0], Complete_task[1])
            Success = self.OCR_Recognition.Cutting_Ocr_Pictures(1, 1280, 1, 1280, '闯关成功',timeout=0.1)
            if Success:
                print("闯关成功")
                self.ADB_Controller.click(Success[0], Success[1])

            Teammate_Settingsw = self.OCR_Recognition.Cutting_Ocr_Pictures(1,1280,1,1280,'队伍设置',timeout=0.1)
            if Teammate_Settingsw:
                print("隊伍設置")
                self.ADB_Controller.click(Teammate_Settingsw[0], Teammate_Settingsw[1])
            Battle_Begins = self.OCR_Recognition.Cutting_Ocr_Pictures(1, 1280, 1, 1280, '战斗开始',timeout=0.1)
            if Battle_Begins:
                print("戰鬥開始")
                self.ADB_Controller.click(Battle_Begins[0], Battle_Begins[1])
            STAGE = self.OCR_Recognition.Cutting_Ocr_Pictures(1, 1280, 1, 1280, 'STAGE',timeout=0.1)
            if STAGE:
                print("關卡完成")
                self.ADB_Controller.click(STAGE[0], STAGE[1])
            confirm = self.OCR_Recognition.Cutting_Ocr_Pictures(1, 1280, 1, 1280, '确认',timeout=0.1)
            if confirm:
                print("確認")
                self.ADB_Controller.click(confirm[0], confirm[1])

            C = self.OCR_Recognition.Cutting_Ocr_Pictures(1, 1280, 1, 1280, "C",timeout=0.1)
            if C:
                print("跳過")
                self.ADB_Controller.click(C[0]+133, C[1])

LevelsAutomation = LevelsAutomation()
LevelsAutomation.Automatic_Level()