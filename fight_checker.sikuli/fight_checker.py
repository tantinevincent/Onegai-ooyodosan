from common import Common, logged
from sikuli import *
from status import Status

class FightChecker(Common):
    def __init__(self):
        self.status = Status(["repairing", "minor_damage", "moderate_damage", "heavily_damage"])
        
    @logged
    def run(self):
        self.clickWithResetMouse("organize.png")
        if self.__is_fleet_tired() or self.__is_fleet_damaged():
            self.back_home_port()
            return False
        
        return True
        
    @logged
    def __is_fleet_tired(self):
        self.clickWithResetMouse("replenishment.png")
        self.clickWithResetMouse(Pattern("mamiya.png").targetOffset(22,-10))
        if exists("mamiya_prompt.png"):
            self.clickWithResetMouse(Pattern("mamiya_prompt.png").targetOffset(14,89))
            return True
            
        self.clickWithResetMouse(Pattern("replenishment_selection.png").targetOffset(241,37))
        return False
        
    @logged
    def __is_fleet_damaged(self):
        for damage_img in self.status.get_images():
            if exists(damage_img):
                return True
        return False
     
if __name__ == "__main__":
    checker = FightChecker(None)
    checker.run()