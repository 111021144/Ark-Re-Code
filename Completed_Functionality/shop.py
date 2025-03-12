from Function.vid_orc import *
from Function.screenshot_thread import *
from Completed_Functionality.back_home import *

class ShopAutomation:
    def __init__(self, port=5560):
        self.ADB_Controller = ADB_Controller(port=port)
        self.IMG_Recognition = IMG_Recognition()

    def go_shop(self,port):
        home = Home(port)
        home.go_home()
        sleep(2)
        while True:
            Enter_store = self.IMG_Recognition.Cutting_Search_Pictures(1, 1276, 1, 715, "picture/shop/Enter_store.png", cv2.TM_CCOEFF_NORMED)
            if Enter_store is not None:
                self.ADB_Controller.click(Enter_store[0], Enter_store[1])
                sleep(1)
                Secret_Store = self.IMG_Recognition.Cutting_Search_Pictures(1, 1276, 1, 715, "picture/shop/Secret_Store.png",cv2.TM_CCOEFF_NORMED)
                if Secret_Store is not None:
                    self.ADB_Controller.click(Secret_Store[0], Secret_Store[1])
                    sleep(1)
                    print("已到達秘密商店\n")
                    break
            else:
                self.ADB_Controller.click(18, 44)

    def buy(self,click_wait_time):
        # 點擊購買
        sleep(click_wait_time)
        x_start, x_end, y_start, y_end = 325, 950, 120, 550
        while True:
            Purchased = self.IMG_Recognition.Cutting_Search_Pictures(x_start=x_start, x_end=x_end, y_start=y_start,
                                                                     y_end=y_end, img=f'picture/shop/Purchased.png',
                                                                     method=cv2.TM_CCOEFF_NORMED)
            if Purchased is not None:
                self.ADB_Controller.click(Purchased[0], Purchased[1] + 66)
                print("已購買過")
                break


            buy = self.IMG_Recognition.Cutting_Search_Pictures(x_start=x_start, x_end=x_end, y_start=y_start,y_end=y_end, img=f'picture/shop/buy.png',method=cv2.TM_CCOEFF_NORMED)
            if buy is not None:
                self.ADB_Controller.click(buy[0], buy[1])

                while True:
                    Successfully_obtained = self.IMG_Recognition.Cutting_Search_Pictures(x_start=x_start,x_end=x_end,y_start=y_start,y_end=y_end,img=f'picture/shop/Successfully_obtained.png',method=cv2.TM_CCOEFF_NORMED)
                    if Successfully_obtained is not None:
                        self.ADB_Controller.click(Successfully_obtained[0], Successfully_obtained[1])
                        print("購買成功")
                        return


    def Shop_function(self, frequency,layers_wait_time=0.5,click_wait_time=1): #time每層等待時間
        # 刷票卷
        Green_Ticket=0
        Yellow_Ticket=0
        print(f"\n{'=' * 17}\n|開始商店刷新的功能|\n{'=' * 17}")
        sleep(2)
        for i in range(frequency+1):
            print(f"------------------------------\n更新第{i + 1}頁")
            y_start, y_end = 61, 175
            pause_event.set()
            for j in range(6):
                sleep(layers_wait_time)
                green = self.IMG_Recognition.Cutting_Search_Pictures(435, 1055, y_start=y_start, y_end=y_end,
                                                                         img='picture/shop/Green_Ticket.png',
                                                                         method=cv2.TM_CCOEFF_NORMED)
                yellow = self.IMG_Recognition.Cutting_Search_Pictures(435, 1055, y_start=y_start, y_end=y_end,
                                                                          img='picture/shop/Yellow_Ticket.png',
                                                                          method=cv2.TM_CCOEFF_NORMED)
                if green is not None:
                    pause_event.clear()
                    if is_valid_png("screenshot.png"):
                        print(f"找到綠票點位: {green}")
                        self.ADB_Controller.click(green[0] + 434, green[1] + 20)
                        self.buy(click_wait_time)
                        Green_Ticket+=1
                        sleep(click_wait_time)
                        pause_event.set()
                elif yellow is not None:
                    pause_event.clear()
                    if is_valid_png("screenshot.png"):
                        print(f"找到黃票點位: {yellow}")
                        self.ADB_Controller.click(yellow[0] + 434, yellow[1] + 20)
                        self.buy(click_wait_time)
                        Yellow_Ticket+=1
                        sleep(click_wait_time)
                        pause_event.set()

                # test = self.IMG_Recognition.Cutting_Search_Pictures(435, 1055, y_start=y_start, y_end=y_end,
                #                                                           img='picture/shop/test.png',
                #                                                           method=cv2.TM_CCOEFF_NORMED)
                # if test is not None:
                #     pause_event.clear()
                #     if is_valid_png("screenshot.png"):
                #         print(f"找到粉塵點位: {test}")
                #         self.ADB_Controller.click(test[0] + 434, test[1] + 20)
                #         self.buy(click_wait_time)
                #         sleep(click_wait_time)
                #         pause_event.set()

                y_start += 115
                y_end += 115
            pause_event.clear()

            # 更新頁數
            Update_Store = self.IMG_Recognition.Cutting_Search_Pictures(
                    34, 234, 629, 685,
                    img='picture/shop/Update_Store.png',
                    method=cv2.TM_CCOEFF_NORMED)
            if Update_Store is not None:
                print(f"找到更新點位: {Update_Store}\n------------------------------\n")
                self.ADB_Controller.click(Update_Store[0], Update_Store[1])
                x_start, x_end, y_start, y_end = 325, 950, 120, 550
                sleep(click_wait_time)
                for _ in range(30):
                    confirm = self.IMG_Recognition.Cutting_Search_Pictures(x_start=x_start, x_end=x_end,y_start=y_start, y_end=y_end,img=f'picture/shop/confirm.png',method=cv2.TM_CCOEFF_NORMED)
                    if confirm is not None:
                        self.ADB_Controller.click(confirm[0], confirm[1])
                        sleep(1)
                        for _ in range(30):
                            Max_frequency = self.IMG_Recognition.Cutting_Search_Pictures(x_start=x_start, x_end=x_end,y_start=y_start, y_end=y_end,img=f'picture/shop/Max_frequency.png',method=cv2.TM_CCOEFF_NORMED)
                            Not_enough_money = self.IMG_Recognition.Cutting_Search_Pictures(x_start=x_start,x_end=x_end,y_start=y_start,y_end=y_end,img=f'picture/shop/Not_enough_money.png',method=cv2.TM_CCOEFF_NORMED)
                            if Max_frequency is not None:
                                self.ADB_Controller.click(Max_frequency[0], Max_frequency[1]+66)
                                print("次數已用盡")
                                print(f"<<商店購買完成,綠票共:{Green_Ticket},黃票共:{Yellow_Ticket}>>\n")
                                return
                            elif Not_enough_money is not None:
                                self.ADB_Controller.click(Not_enough_money[0], Not_enough_money[1] + 66)
                                print("財務不足")
                                print(f"<<商店購買完成,綠票共:{Green_Ticket},黃票共:{Yellow_Ticket}>>\n")
                                return
                    else:
                        self.ADB_Controller.click(263, 393)
        print(f"<<商店購買完成,綠票共:{Green_Ticket},黃票共:{Yellow_Ticket}>>\n")


    def Start_Shopping(self,port, frequency,layers_wait_time=0.5,click_wait_time=1):
        self.go_shop(port)
        self.Shop_function(frequency,layers_wait_time,click_wait_time)