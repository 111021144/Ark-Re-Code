import time

import cv2
import os
import easyocr
import matplotlib.pyplot as plt


def is_valid_png(file_path):
    # 檢查檔案是否為有效的PNG圖片
    try:
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

    def Cutting_Search_Pictures(self, x_start, x_end, y_start, y_end, img, method):
        # 找圖片 裁切圖片測圖片並返回位置
        # cv2.TM_CCOEFF           (忽略整體亮度影響，適合一般匹配，數值越大越匹配。)
        # cv2.TM_CCOEFF_NORMED    (TM_CCOEFF 的正規化版本，結果穩定，範圍 -1 到 1，取最大值。)
        # cv2.TM_CCORR            (受亮度影響，適合對比度高的圖片，數值越大越匹配。)
        # cv2.TM_CCORR_NORMED     (TM_CCORR 的正規化版本，範圍 0 到 1，取最大值。)
        # cv2.TM_SQDIFF           (計算像素差異，數值越小越匹配，受亮度影響大。)
        # cv2.TM_SQDIFF_NORMED    (TM_SQDIFF 的正規化版本，範圍 0 到 1，取最小值。)
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

    def wait_for_image(self, x1, x2, y1, y2, image_path, timeout=3):
        #等待找到圖片
        start_time = time.time()
        while time.time() - start_time < timeout:
            result = self.Cutting_Search_Pictures(x1, x2, y1, y2, image_path, cv2.TM_CCOEFF_NORMED)
            if result is not None:
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

    def Cutting_Search_ORC(self,x_start,x_end,y_start,y_end,text,gpu=False):
        # 找文字 裁切圖片測文字並返回位置
        image = cv2.imread("screenshot.png")
        roi = image[y_start:y_end, x_start:x_end]  # image[y_start:y_end, x_start:x_end]每一格Y+115
        cv2.imwrite("cutting_pictures.png", roi)
        reader = easyocr.Reader(['ch_tra'],gpu)  #如果是中文使用 ['ch_tra']
        result = reader.readtext('cutting_pictures.png')
        # print(result)
        if result:
            if result[0][1]==text:
                center_x = (x_start + x_end) / 2
                center_y = (y_start + y_end) / 2
                print(f"Successfully_found:{result[0][1],center_x,center_y}")
                return center_x,center_y
        else:
            return None
