from Function.screenshot_thread import *
from Completed_Functionality.shop import *
from Completed_Functionality.back_home import *
from Completed_Functionality.supplies import *

port = 5560


screenshot = screenshot_threading(port)
screenshot_start = threading.Thread(target=screenshot.start_screenshot, daemon=True)
screenshot_start.start()


# shop--------------------------------------------------------------------------------------
shop_automation = ShopAutomation(port)
shop_automation.Start_Shopping(port,frequency=90,layers_wait_time=0.5,click_wait_time=1) # layers_wait_time掃描層數等待時間，click_wait_time點擊等時間
# shop--------------------------------------------------------------------------------------

#基地----------------------------------------------------------------------------------------
supplies_automation = SuppliesAutomation(port)
supplies_automation.Start_Supplies(port)
#基地----------------------------------------------------------------------------------------


screenshot.stop_start_screenshot_threading = True
screenshot_start.join()
