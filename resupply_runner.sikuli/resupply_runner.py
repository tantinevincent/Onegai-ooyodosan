from common import Common, logged
from fleet import Fleet
from sikuli import *
from config import Config
from status import Status

class ResupplyRunner(Common):
    def __init__(self, fleets, from_small_resuppy=False, enable_expedition_check=False, message=None):
        self.fleets = fleets
        self.from_small_resuppy = from_small_resuppy 
        self.enable_expedition_check = enable_expedition_check
        self.message = message
        
        if self.enable_expedition_check:
            self.expedition_img = Status(["on_expedition"]).get_images()[0]
        
    @logged
    def run(self):
        if not self.from_small_resuppy:
            supply_btn = "supply.png"
        else:
            supply_btn = "supply_small.png"
        
        if self.message is not None:
            self.message.set_need_check(False)
        
        self.clickWithRandomLocationAndResetMouse(supply_btn)
        for fleet in self.fleets:
            self.clickWithRandomOffset(fleet.getNotSelectedImage())
            if not self.__need_resupply():
                continue
            if self.message is not None:  # need record expedition check
                self.message.set_need_check(True)
            
            self.__resupply_fleet() 
        
        self.back_home_port()  
        return True
    
    def __need_resupply(self):
        return not self.enable_expedition_check or not exists(self.expedition_img)
    
    @logged
    def __resupply_fleet(self):
        self.clickWithRandomOffset("resupply_all.png")
        sleep(3)
    
if __name__ == "__main__":
    #runner = ResupplyRunner([Fleet(1)], from_small_resuppy=False)
    runner = ResupplyRunner([Fleet(1), Fleet(2), Fleet(3), Fleet(4)], from_small_resuppy=False, enable_expedition_check=True)
    runner.run()