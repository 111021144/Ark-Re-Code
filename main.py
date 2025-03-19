from Completed_Functionality.shop import *
from Completed_Functionality.supplies import *
from Completed_Functionality.bot import *

port = 5560

#基地--------------------------------------------------------------------------------------
# supplies_automation = SuppliesAutomation(port)
# supplies_automation.Start_Supplies(port)
#基地--------------------------------------------------------------------------------------

#商店--------------------------------------------------------------------------------------
# shop_automation = ShopAutomation(port)
# shop_automation.Start_Shopping(port,frequency=90)
#商店--------------------------------------------------------------------------------------

#NPC--------------------------------------------------------------------------------------
npc_automation = NpcAutomation(port)
npc_automation.Start_NPC(port)
#NPC--------------------------------------------------------------------------------------

