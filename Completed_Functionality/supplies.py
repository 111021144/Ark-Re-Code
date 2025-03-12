from Function.vid_orc import *
from Function.screenshot_thread import *
from Completed_Functionality.back_home import *
import time

class SuppliesAutomation:
    def __init__(self, port=5560):
        self.ADB_Controller = ADB_Controller(port=port)
        self.IMG_Recognition = IMG_Recognition()

    def go_base(self, port):
        self.home = Home(port)
        self.home.go_home()
        sleep(1)
        Enter_base = self.IMG_Recognition.wait_for_image(1, 1276, 1, 715, "picture/base/Enter_base.png")
        if Enter_base:
            self.ADB_Controller.click(Enter_base[0], Enter_base[1])
            print("進入基地")
        else:
            self.ADB_Controller.click(18, 44)


    def Power_conversion(self,port):
        self.go_base(port)
        Enter_Power_conversion = self.IMG_Recognition.wait_for_image(448, 785, 328, 437, "picture/base/Enter_Power_conversion.png")
        if Enter_Power_conversion:
            self.ADB_Controller.click(Enter_Power_conversion[0], Enter_Power_conversion[1])
            print("進入動力轉換")

            Receive_conversion_rewards = self.IMG_Recognition.wait_for_image(980, 1234, 590, 690, "picture/base/Receive_conversion_rewards.png")
            if Receive_conversion_rewards:
                self.ADB_Controller.click(Receive_conversion_rewards[0], Receive_conversion_rewards[1])

                Rewards_Received = self.IMG_Recognition.wait_for_image(490, 785, 138, 210, "picture/base/Rewards_Received.png")
                if Rewards_Received:
                    self.ADB_Controller.click(Rewards_Received[0], Rewards_Received[1])
                    print("獎勵領取成功")

    def Production_Center(self, port):
        self.go_base(port)
        Production_Center = self.IMG_Recognition.wait_for_image(178, 544, 146, 257, "picture/base/Production_Center.png")
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
        Production_Center = self.IMG_Recognition.wait_for_image(178, 544, 146, 257, "picture/base/Production_Center.png")
        if Production_Center:
            self.ADB_Controller.click(Production_Center[0], Production_Center[1])
            print("進入生產中心")

        Fast_production = self.IMG_Recognition.wait_for_image(284, 503, 484, 564, "picture/base/Fast_production.png")
        if Fast_production:
            self.ADB_Controller.click(Fast_production[0], Fast_production[1])
            print("進入快速量產")

        gem = self.IMG_Recognition.wait_for_image(218, 1041, 432, 585, "picture/base/gem.png")
        self.ADB_Controller.swipe(571,490,571,237)
        sleep(2)
        if gem:
            self.ADB_Controller.click(gem[0], gem[1])
            print("購買水晶頁面")
            Get_gem = self.IMG_Recognition.wait_for_image(218, 1041, 432, 585, "picture/base/Get_gem.png")
            if Get_gem:
                self.ADB_Controller.click(Get_gem[0], Get_gem[1])
                print("已購買水晶")
                return

    from time import sleep, time

    def Task_Click(self, img):
        flag = True
        while flag:
            War_Mission = self.IMG_Recognition.wait_for_image(1052, 1276, 169, 570, "picture/base/War_Mission.png")
            if War_Mission:
                self.ADB_Controller.click(War_Mission[0], War_Mission[1])
                print("戰爭任務頁面")
                while flag:
                    Execution = self.IMG_Recognition.wait_for_image(330, 1047, 146, 711, f"picture/base/{img}")
                    if Execution:
                        self.ADB_Controller.click(Execution[0] + 377, Execution[1])
                        print(f"執行 {img[:-4]}")
                        while flag:
                            Not_implemented = self.IMG_Recognition.wait_for_image(807, 956, 134, 500,
                                                                                  "picture/base/Not_implemented.png")
                            if Not_implemented:
                                print("成員未滿")
                                self.ADB_Controller.click(608, 497)
                            else:
                                print("成員已滿")
                                In_progress = self.IMG_Recognition.wait_for_image(964, 1244, 616, 687,
                                                                                "picture/base/In_progress.png")
                                implement = self.IMG_Recognition.wait_for_image(964, 1244, 616, 687,
                                                                                "picture/base/implement.png")
                                if In_progress:
                                    print("已在執行中\n")
                                    retur = self.IMG_Recognition.wait_for_image(7, 164, 13, 71, "picture/base/retur.png")
                                    if retur:
                                        self.ADB_Controller.click(retur[0], retur[1])
                                        flag = False

                                if implement:
                                    print("開始執行\n")
                                    self.ADB_Controller.click(implement[0], implement[1])
                                    flag = False

                    self.ADB_Controller.swipe(603, 505, 603, 260)
                    sleep(0.5)


    def despatch(self, port):
        self.go_base(port)
        Command_Headquarters = self.IMG_Recognition.wait_for_image(132, 470, 457, 551,
                                                                   "picture/base/Command_Headquarters.png")
        if Command_Headquarters:
            self.ADB_Controller.click(Command_Headquarters[0], Command_Headquarters[1])
            print("指揮總部")

        self.Task_Click(f"Execution1.png")
        self.Task_Click(f"Execution2.png")

    def Start_Supplies(self, port):
        self.Power_conversion(port)
        self.Production_Center(port)
        self.Buy_Crystal(port)
        self.despatch(port)
