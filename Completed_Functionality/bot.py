from Function.ocr import *
from Completed_Functionality.back_home import *

class NpcAutomation:
    def __init__(self,port):

        self.OCR_Recognition = OCR_Recognition(port)
        self.ADB_Controller = ADB_Controller(port)

    def go_NPC(self,port):
        home = Home(port)
        home.go_home()
        Attack = self.OCR_Recognition.Cutting_Ocr_Pictures(1087, 1194, 618, 681, "出击")
        if Attack:
            self.ADB_Controller.click(Attack[0], Attack[1])
            Arena = self.OCR_Recognition.Cutting_Ocr_Pictures(503, 643, 637, 690, "竞技场")
            if Arena:
                self.ADB_Controller.click(Arena[0], Arena[1])
                NPC = self.OCR_Recognition.Cutting_Ocr_Pictures(1069, 1159, 300, 350, "NPC对战")
                if NPC:
                    self.ADB_Controller.click(NPC[0], NPC[1])
                    Hell = self.OCR_Recognition.Cutting_Ocr_Pictures(866, 997, 71, 120, "地狱级")
                    if Hell:
                        self.ADB_Controller.click(Hell[0], Hell[1])
    def Find_match(self,port):
        NPC_LIST = [
            "方舟α菁英小队", "方舟α维安小队", "全知全能的学者们", "不可忽视的天们",
            "散播大爱的少女们", "使徒的虔诚信众", "视钱如命的猎人团", "方舟β科技部队",
            "偶像群星会", "超越本尊的复制军"
        ]
        Flag = True
        for i in NPC_LIST:
            while Flag:
                PK = self.OCR_Recognition.Cutting_Ocr_Pictures(687, 848, 130, 719, text=f"{i}")

                if PK:
                    square = self.OCR_Recognition.Get_Square_Coordinates(PK[0]+151,PK[1]+13,100)
                    text = self.OCR_Recognition.Detect_Text_Area(square['x_start'], square['x_end'], square['y_start'], square['y_end'])
                    if text:
                        print(f"{i}: {PK}:{text}")
                        if text=="挑战":
                            self.ADB_Controller.click(PK[0]+151,PK[1]+13)
                            Battle_Begins = self.OCR_Recognition.Cutting_Ocr_Pictures(1155,1243,610,655,"战斗开始")
                            if Battle_Begins:
                               self.ADB_Controller.click(Battle_Begins[0], Battle_Begins[1])
                               sleep(1)


                            #未驗證---------------------------------------------------------------------------------
                               Purchase_flags = self.OCR_Recognition.Cutting_Ocr_Pictures(320,461,146,195,"购买旗帜")
                               if Purchase_flags:
                                   print("旗幟不足")
                                   Insufficient_purchases = self.OCR_Recognition.Cutting_Ocr_Pictures(412,570,322,366,"一天可购买1次")
                                   if Insufficient_purchases:
                                       Cancel = self.OCR_Recognition.Cutting_Ocr_Pictures(412, 521, 500,550,"取消")
                                       if Cancel:
                                           self.ADB_Controller.click(Cancel[0], Cancel[1])
                                           Flag = False
                                           break
                                   else:
                                       buy = self.OCR_Recognition.Cutting_Ocr_Pictures(764, 864, 494, 548, "购买")
                                       if buy:
                                           self.ADB_Controller.click(buy[0], buy[1])
                                           buy = self.OCR_Recognition.Cutting_Ocr_Pictures(772, 854, 474, 515, "购买")
                                           if buy:
                                               self.ADB_Controller.click(buy[0], buy[1])
                                               Successfully_obtained = self.OCR_Recognition.Cutting_Ocr_Pictures(325,950,120,550,f'获得道具')
                                               if Successfully_obtained:
                                                   self.ADB_Controller.click(Successfully_obtained[0], Successfully_obtained[1])
                               # 未驗證---------------------------------------------------------------------------------


                               else:
                                   print("戰鬥中....")
                                   while Flag:
                                        end = self.OCR_Recognition.Cutting_Ocr_Pictures(1155, 1243, 610, 680, "结束")
                                        if end:
                                            print("戰鬥結束")
                                            self.ADB_Controller.click(end[0], end[1])
                                            NPC_Battle = self.OCR_Recognition.Cutting_Ocr_Pictures(1155, 1225, 620, 675, "NPC对战")
                                            if NPC_Battle:
                                                break
                    break
                else:
                    self.ADB_Controller.swipe(915, 336, 919, 207)  # 继续滑动找 NPC
                    sleep(2)
        home = Home(port)
        home.go_home()

    def Start_NPC(self,port):
        print(f"\n{'=' * 15}\n|開始NPC對戰功能|\n{'=' * 15}")
        self.go_NPC(port)
        self.Find_match(port)