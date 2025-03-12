import threading
from time import sleep
from Function.adb import ADB_Controller

pause_event = threading.Event()  # 控制截圖是否暫停
print(f"{'='*65}")
print(f"|控制器已初始化，截圖控制器:{pause_event}|")
print(f"{'=' * 65}\n")

class screenshot_threading:
    def __init__(self,port):
        self.ADB_Controller = ADB_Controller(port)
        self.stop_start_screenshot_threading = False
    def start_screenshot(self):
        # 多執行緒截圖
        print(f"開始執行緒: 截圖\n")
        while not self.stop_start_screenshot_threading:
            if not pause_event.is_set():
                self.ADB_Controller.screenshot()
                sleep(0.5)
        else:
            print("停止執行緒: 截圖\n")
