from common import Common, logged
from fleet import Fleet
from sikuli import *
from config import Config
from status import Status

class ResupplyRunner(Common):
    def __init__(self, fleets, from_small_resuppy=False, enable_expedition_check=False):
        self.fleets = fleets
        self.from_small_resuppy = from_small_resuppy 
        self.enable_expedition_check = enable_expedition_check
        
        if self.enable_expedition_check:
            self.expedition_img = Status(["on_expedition"]).get_images()[0]
        
    @logged
    def run(self):
        if not self.from_small_resuppy:
            supply_btn = "supply.png"
        else:
            supply_btn = "supply_small.png"
        
        self.clickWithResetMouse(supply_btn)
        for fleet in self.fleets:
            self.clickWithResetMouse(fleet.getNotSelectedImage())
            if self.__need_resupply():
                self.__resupply_fleet()
        
        self.back_home_port()  
        return True
    
    def __need_resupply(self):
        return not self.enable_expedition_check or not exists(self.expedition_img)
    
    @logged
    def __resupply_fleet(self):
        location = find(Pattern("resupply_fleet_marks.png").targetOffset(-71,2)).getTarget()
        OFFSET_Y = 50
        for i in xrange(1,7):
            click(location.below(OFFSET_Y*i)) #click all resupply check box
        self.clickWithResetMouse("resupply_everything.png")
        sleep(3)
    
if __name__ == "__main__":
    #runner = ResupplyRunner([Fleet(1)], from_small_resuppy=False)
    runner = ResupplyRunner([Fleet(2), Fleet(3), Fleet(4)], from_small_resuppy=False, enable_expedition_check=True)
    runner.run()
