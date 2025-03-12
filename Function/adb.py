import subprocess
import time
import cv2


class ADB_Controller:

    def __init__(self,port):
        self.device = f"emulator-{port}"

    def list_device(self):
        # 查看當前有哪些device
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
        return result.stdout

    def screenshot(self):
        # 對模擬器截圖
        remote_path = "/sdcard/screenshot.png"
        local_path = "screenshot.png"
        subprocess.run(["adb", "-s", self.device, "shell", "screencap", "-p", remote_path])
        subprocess.run(["adb", "-s", self.device, "pull", remote_path, local_path],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        return True

    def test_screenshot_time(self):
        start_time = time.time()
        subprocess.run(["adb", "-s", self.device, "shell", "screencap", "-p", "/sdcard/screenshot.png"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["adb", "-s", self.device, "pull", "/sdcard/screenshot.png"], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
        end_time = time.time()
        print(f"截圖並儲存總耗時: {end_time - start_time:.3f} 秒")

    def click(self, x, y):
        # 點擊動作
        x = int(x)
        y = int(y)
        try:
            subprocess.run(["adb", "-s", self.device, "shell", "input", "tap", str(x), str(y)])
            # print(f"Tapped at ({x}, {y})")
        except Exception as e:
            return f"點擊時發生發生錯誤"

    def long_press(self, x, y, duration=2000):
        #長按
        subprocess.run(["adb", "-s", self.device, "shell", "input", "swipe", str(x), str(y), str(x), str(y), str(duration)])

    def swipe(self, x1, y1, x2, y2, duration=500):
        # 滑動
        subprocess.run(["adb", "shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration)])
