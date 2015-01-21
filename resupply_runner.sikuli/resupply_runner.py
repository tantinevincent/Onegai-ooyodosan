from common import Common, logged
from fleet import Fleet
from sikuli import *
from config import Config

class ResupplyRunner(Common):
    def __init__(self, fleets, from_small_resuppy=False):
        self.fleets = fleets
        self.from_small_resuppy = from_small_resuppy 
        
    @logged
    def run(self):
        if not self.from_small_resuppy:
            supply_btn = "supply.png"
        else:
            supply_btn = "supply_small.png"
        
        self.clickWithResetMouse(supply_btn)
        for fleet in self.fleets:
            self.clickWithResetMouse(fleet.getNotSelectedImage())
            self.__resupply_fleet()
        
        self.back_home_port()  
        return True
        
    @logged
    def __resupply_fleet(self):
        location = find(Pattern("resupply_fleet_marks.png").targetOffset(-71,2)).getTarget()
        OFFSET_Y = 50
        for i in xrange(1,7):
            click(location.below(OFFSET_Y*i)) #click all resupply check box
        self.clickWithResetMouse("resupply_everything.png")
        sleep(3)
    
if __name__ == "__main__":
    runner = ResupplyRunner([Fleet(1)], None, from_small_resuppy=True)
    runner.run()