from Function.vid import *
from Completed_Functionality.back_home import *
from Function.ocr import *
import time

class SuppliesAutomation:
    def __init__(self, port=5560):
        self.ADB_Controller = ADB_Controller(port=port)
        self.IMG_Recognition = IMG_Recognition()
        self.OCR_Recognition = OCR_Recognition(port)

    def go_base(self, port):
        self.home = Home(port)
        self.home.go_home()
        Enter_base = self.OCR_Recognition.Cutting_Ocr_Pictures(860, 937, 650, 693, "基地")
        if Enter_base:
            self.ADB_Controller.click(Enter_base[0], Enter_base[1])
            print("進入基地")


    def Power_conversion(self,port):
        self.go_base(port)
        Enter_Power_conversion = self.OCR_Recognition.Cutting_Ocr_Pictures(448, 785, 328, 437, "动力转换")
        if Enter_Power_conversion:
            self.ADB_Controller.click(Enter_Power_conversion[0], Enter_Power_conversion[1])
            print("進入動力轉換")

            Receive_conversion_rewards = self.OCR_Recognition.Cutting_Ocr_Pictures(980, 1234, 590, 690, "领取生产的奖励")
            if Receive_conversion_rewards:
                self.ADB_Controller.click(Receive_conversion_rewards[0], Receive_conversion_rewards[1])

                Rewards_Received = self.OCR_Recognition.Cutting_Ocr_Pictures(490, 785, 138, 210, "领取奖励完成")
                if Rewards_Received:
                    self.ADB_Controller.click(Rewards_Received[0], Rewards_Received[1])
                    print("獎勵領取成功")

    def Production_Center(self, port):
        self.go_base(port)
        Production_Center = self.OCR_Recognition.Cutting_Ocr_Pictures(178, 544, 146, 257, "生产中心")
        if Production_Center:
            self.ADB_Controller.click(Production_Center[0], Production_Center[1])
            print("進入生產中心")
#還要再加----------------------------------------------------------------------------------------------------------------------------------------------------------
            Growth_Potion = self.IMG_Recognition.wait_for_image(1, 1276, 1, 715, "picture/base/Growth_Potion.png")
            Lower_level_crystal = self.IMG_Recognition.wait_for_image(1, 1276, 1, 715, "picture/base/Lower_level_crystal.png")
            if Growth_Potion:
                self.ADB_Controller.click(Growth_Potion[0], Growth_Potion[1])
                print("已領取成長藥劑")
            if Lower_level_crystal:
                self.ADB_Controller.click(Lower_level_crystal[0], Lower_level_crystal[1])
                print("已領取下級升星水晶")
            else:
                self.ADB_Controller.click(170, 328)
                print("未找到獎勵")

    def Buy_Crystal(self, port):
        self.go_base(port)
        Production_Center = self.OCR_Recognition.Cutting_Ocr_Pictures(178, 544, 146, 257, "生产中心")
        if Production_Center:
            self.ADB_Controller.click(Production_Center[0], Production_Center[1])
            print("進入生產中心")

        Fast_production = self.OCR_Recognition.Cutting_Ocr_Pictures(284, 503, 484, 564, "快速量产")
        if Fast_production:
            self.ADB_Controller.click(Fast_production[0], Fast_production[1])
            print("進入快速量產")

        gem = self.OCR_Recognition.Cutting_Ocr_Pictures(218, 1041, 432, 585, "4250")
        self.ADB_Controller.swipe(571,490,571,237)
        sleep(3)
        if gem:
            self.ADB_Controller.click(gem[0], gem[1])
            print("已購買水晶")
            return



    def Task_Click(self, text):
        print(f"執行 {text[:-4]}")
        flag = True
        while flag:
            War_Mission = self.OCR_Recognition.Cutting_Ocr_Pictures(1052, 1276, 169, 570, "战争任务")
            if War_Mission:
                self.ADB_Controller.click(War_Mission[0], War_Mission[1])
                print("戰爭任務頁面")
                while flag:
                    Execution = self.OCR_Recognition.Cutting_Ocr_Pictures(550, 663, 463, 708, f"{text}")
                    if Execution:
                        self.ADB_Controller.click(Execution[0] + 377, Execution[1])
                        while flag:
                            Not_implemented = self.IMG_Recognition.wait_for_image(807, 956, 134, 500,
                                                                                  "picture/base/Not_implemented.png")
                            if Not_implemented:
                                print("成員未滿")
                                add = self.IMG_Recognition.wait_for_image(571, 632, 469, 518,
                                                                                  "picture/base/add.png")
                                if add:
                                    self.ADB_Controller.click(add[0], add[1])
                            else:
                                print("成員已滿")
                                In_progress = self.OCR_Recognition.Cutting_Ocr_Pictures(964, 1244, 616, 687,
                                                                                "取消执行")
                                implement = self.OCR_Recognition.Cutting_Ocr_Pictures(964, 1244, 616, 687,
                                                                                "执行")
                                if In_progress:
                                    print("已在執行中\n")
                                    retur = self.OCR_Recognition.Cutting_Ocr_Pictures(67, 128, 18, 56, "返回")
                                    if retur:
                                        self.ADB_Controller.click(retur[0], retur[1])
                                        flag = False

                                if implement:
                                    print("開始執行\n")
                                    self.ADB_Controller.click(implement[0], implement[1])
                                    flag = False
                    else:
                        self.ADB_Controller.swipe(603, 505, 603, 260)
                        sleep(0.5)


    def despatch(self, port):
        self.go_base(port)
        Command_Headquarters = self.OCR_Recognition.Cutting_Ocr_Pictures(132, 470, 457, 551,"指挥总部")
        if Command_Headquarters:
            self.ADB_Controller.click(Command_Headquarters[0], Command_Headquarters[1])
            print("指揮總部")

        self.Task_Click(f"搜索埋伏")
        self.Task_Click(f"调查叛徒")
        self.home.go_home()

    def Start_Supplies(self, port):
        print(f"\n{'=' * 18}\n|開始基地收取獎勵功能|\n{'=' * 18}")
        self.Power_conversion(port)
        self.Production_Center(port)
        self.Buy_Crystal(port)
        self.despatch(port)
