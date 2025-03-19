import time
import cv2
import os
from Function.adb_controller import ADB_Controller
import matplotlib.pyplot as plt

def is_valid_png(file_path):
    # 檢查檔案是否為有效的PNG圖片
    try:
        if not os.path.exists(file_path):
            return False

        if not os.path.isfile(file_path) or os.path.getsize(file_path) < 500:
            return False

        with open(file_path, "rb") as f:
            if f.read(8) != b'\x89PNG\r\n\x1a\n':  # 檢查 PNG 頭部
                return False
            f.seek(-8, os.SEEK_END)  # 檔案末尾 8 bytes
            if f.read(8) != b'IEND\xaeB`\x82':  # 檢查 PNG 結尾
                return False

        return True

    except:
        return False

class IMG_Recognition():
    def __init__(self,port=5560):
        self.adb = ADB_Controller(port)
    def Cutting_Search_Pictures(self, x_start, x_end, y_start, y_end, img, method=cv2.TM_CCOEFF_NORMED):
        # 找圖片 裁切圖片測圖片並返回位置
        # cv2.TM_CCOEFF           (忽略整體亮度影響，適合一般匹配，數值越大越匹配。)
        # cv2.TM_CCOEFF_NORMED    (TM_CCOEFF 的正規化版本，結果穩定，範圍 -1 到 1，取最大值。)
        # cv2.TM_CCORR            (受亮度影響，適合對比度高的圖片，數值越大越匹配。)
        # cv2.TM_CCORR_NORMED     (TM_CCORR 的正規化版本，範圍 0 到 1，取最大值。)
        # cv2.TM_SQDIFF           (計算像素差異，數值越小越匹配，受亮度影響大。)
        # cv2.TM_SQDIFF_NORMED    (TM_SQDIFF 的正規化版本，範圍 0 到 1，取最小值。)
        self.adb.screenshot()
        if is_valid_png("screenshot.png") and is_valid_png(img):
            image = cv2.imread("screenshot.png")
            if image is not None:
                roi = image[y_start:y_end, x_start:x_end]
                templ = cv2.imread(img)

                result = cv2.matchTemplate(roi, templ, method)
                minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
                h, w = templ.shape[:2]
                center_x, center_y = maxLoc[0] + w // 2 + x_start, maxLoc[1] + h // 2 + y_start
                if maxVal > 0.8:
                    # print(img, maxVal)
                    # print(center_x, center_y)
                    # cv2.rectangle(image, (x_start, y_start), (x_end, y_end), (0, 0, 255), 2)  # 畫裁切框
                    # cv2.circle(image, (center_x, center_y), 10, (0, 0, 255), -1)  # 在匹配中心畫紅點
                    # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                    # plt.axis('off')
                    # plt.show()
                    return center_x, center_y

    def Search_Pictures(self,x_start, x_end, y_start, y_end, img, method=cv2.TM_CCOEFF_NORMED):
        #等待圖片專用
        self.adb.screenshot()
        if is_valid_png("screenshot.png") and is_valid_png(img):
            image = cv2.imread("screenshot.png")
            if image is not None:
                roi = image[y_start:y_end, x_start:x_end]
                templ = cv2.imread(img)

                result = cv2.matchTemplate(roi, templ, method)
                minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
                h, w = templ.shape[:2]
                center_x, center_y = maxLoc[0] + w // 2 + x_start, maxLoc[1] + h // 2 + y_start

                # print(img, maxVal)
                if maxVal > 0.8:
                    # print(img, maxVal)
                    # print(center_x, center_y)
                    # cv2.rectangle(image, (x_start, y_start), (x_end, y_end), (0, 0, 255), 2)  # 畫裁切框
                    # cv2.circle(image, (center_x, center_y), 10, (0, 0, 255), -1)  # 在匹配中心畫紅點
                    # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                    # plt.axis('off')
                    # plt.show()
                    return center_x, center_y

    def wait_for_image(self, x_start, x_end, y_start, y_end, image_path,method=cv2.TM_CCOEFF_NORMED, timeout=2):
        #等待找到圖片
        start_time = time.time()
        while time.time() - start_time < timeout:
            result = self.Search_Pictures(x_start, x_end, y_start, y_end, image_path, method)
            if result:
                return result
        # return print(f"未找到{image_path}")

    def get_pixel_color(self,img, x, y):
        # 返回指定位置 (x, y) 的顏色
        img = cv2.imread(f'{img}')
        color = img[y, x]
        return color

    def crop_image(self,x_start, x_end, y_start, y_end, input_image_path, output_image_path):
        # 從大圖裁剪需要的區域
        img = cv2.imread(input_image_path)
        if x_start < 0 or y_start < 0 or x_end > img.shape[1] or y_end > img.shape[0]:
            print("裁剪區域超出圖片範圍！")
            return
        cropped_img = img[y_start:y_end, x_start:x_end]
        cv2.imwrite(output_image_path, cropped_img)
        print(f"裁剪後的圖片已保存為 {output_image_path}")