from Completed_Functionality.back_home import *
from Function.vid import *
from Function.ocr import *
class ShopAutomation:
    def __init__(self, port=5560):
        self.ADB_Controller = ADB_Controller(port)
        self.IMG_Recognition = IMG_Recognition(port)
        self.OCR_Recognition = OCR_Recognition(port)

    def go_shop(self,port):
        home = Home(port)
        home.go_home()
        Enter_store = self.OCR_Recognition.Cutting_Ocr_Pictures(59, 136, 633, 698, "商店")
        if Enter_store:
            self.ADB_Controller.click(Enter_store[0], Enter_store[1])
            Secret_Store = self.OCR_Recognition.Cutting_Ocr_Pictures(1058, 1213, 170, 715, "秘密商店")
            if Secret_Store:
                self.ADB_Controller.click(Secret_Store[0], Secret_Store[1])
                print("已到達秘密商店\n")

    def buy(self):
        # 點擊購買
        buy = self.OCR_Recognition.Cutting_Ocr_Pictures(325, 950, 120, 550, f'购买')
        if buy:
            self.ADB_Controller.click(buy[0], buy[1])
            sleep(1)
            Successfully_obtained = self.OCR_Recognition.Cutting_Ocr_Pictures(325, 950, 120, 550, f'获得道具')
            if Successfully_obtained:
                self.ADB_Controller.click(Successfully_obtained[0], Successfully_obtained[1])
                print("購買成功")
                return
        confirm = self.OCR_Recognition.Cutting_Ocr_Pictures(351, 924, 281, 426, f'目前还无法购买')
        if confirm:
            self.ADB_Controller.click(confirm[0], confirm[1] + 66)
            print("已購買過")
            return



    def Shop_function(self, frequency):
        # 刷票卷
        Green_Ticket=0
        Yellow_Ticket=0
        for i in range(frequency+1):
            print(f"------------------------------\n更新第{i + 1}次")
            y_start, y_end = 61, 175
            self.ADB_Controller.swipe(716, 508, 728, 325)
            sleep(1.5)
            for j in range(6):
                sleep(0.5)
                green = self.OCR_Recognition.Cutting_Ocr_Pictures(435, 1055, y_start=y_start, y_end=y_end,
                                                                         text = '招募契约',timeout=0.5)
                yellow = self.OCR_Recognition.Cutting_Ocr_Pictures(435, 1055, y_start=y_start, y_end=y_end,
                                                                          text='神秘契约',timeout=0.5)
                if green is not None:
                    if is_valid_png("screenshot.png"):
                        print(f"找到綠票點位: {green}")
                        buy = self.OCR_Recognition.Cutting_Ocr_Pictures(435, 1055, y_start=y_start, y_end=y_end,text= f'购买')
                        if buy:
                            self.ADB_Controller.click(buy[0], buy[1])
                            self.buy()
                            Green_Ticket+=1
                elif yellow is not None:
                    if is_valid_png("screenshot.png"):
                        print(f"找到黃票點位: {yellow}")
                        buy = self.OCR_Recognition.Cutting_Ocr_Pictures(435, 1055, y_start=y_start, y_end=y_end, text=f'购买')
                        if buy:
                            self.ADB_Controller.click(buy[0], buy[1])
                            self.buy()
                            Yellow_Ticket+=1


                # test = self.OCR_Recognition.Cutting_Ocr_Pictures(435, 1055, y_start=y_start, y_end=y_end,
                #                                                           text='星源粉末',timeout=0.5)
                # if test is not None:
                #     if is_valid_png("screenshot.png"):
                #         print(f"找到粉塵點位: {test}")
                #         buy = self.OCR_Recognition.Cutting_Ocr_Pictures(435, 1055, y_start=y_start, y_end=y_end,text=f'购买')
                #         if buy:
                #             self.ADB_Controller.click(buy[0], buy[1])
                #             self.buy()

                y_start += 115
                y_end += 115

            # 更新頁數
            Update_Store = self.OCR_Recognition.Cutting_Ocr_Pictures(34, 234, 629, 685,f'立即更新', cv2.TM_CCOEFF_NORMED)
            if Update_Store :
                print(f"找到更新點位: {Update_Store}\n------------------------------\n")
                self.ADB_Controller.click(Update_Store[0], Update_Store[1])
                x_start, x_end, y_start, y_end = 325, 950, 120, 550
                confirm = self.OCR_Recognition.Cutting_Ocr_Pictures(x_start, x_end, y_start, y_end, f'确认')
                if confirm:
                    self.ADB_Controller.click(confirm[0], confirm[1])
                    Max_frequency = self.OCR_Recognition.Cutting_Ocr_Pictures(x_start, x_end, y_start, y_end, f'已达刷新上限',timeout=1)
                    Not_enough_money = self.OCR_Recognition.Cutting_Ocr_Pictures(x_start, x_end, y_start, y_end, f'财务不足',timeout=1)
                    if Max_frequency:
                        self.ADB_Controller.click(Max_frequency[0], Max_frequency[1]+66)
                        print("次數已用盡")
                        print(f"<<商店購買完成,綠票共:{Green_Ticket},黃票共:{Yellow_Ticket}>>\n")
                        return
                    if Not_enough_money:
                        self.ADB_Controller.click(Not_enough_money[0], Not_enough_money[1] + 66)
                        print("財務不足")
                        print(f"<<商店購買完成,綠票共:{Green_Ticket},黃票共:{Yellow_Ticket}>>\n")
                        return
                else:
                    self.ADB_Controller.click(263, 393)
        print(f"<<商店購買完成,綠票共:{Green_Ticket},黃票共:{Yellow_Ticket}>>\n")


    def Start_Shopping(self,port, frequency):
        print(f"\n{'=' * 15}\n|開始商店刷新功能|\n{'=' * 15}")
        self.go_shop(port)
        self.Shop_function(frequency)
        home = Home(port)
        home.go_home()