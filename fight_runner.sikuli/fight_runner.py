from common import Common, logged
from sikuli import *

class FightRunner(Common):
    @logged
    def run(self):
        self.clickWithRandomLocationAndResetMouse(Pattern("sortie.png").similar(0.60))
        self.clickWithRandomLocationAndResetMouse("fight.png")
        self.clickWithRandomOffset(Pattern("worlds.png").targetOffset(4,5))
        #self.clickWithRandomOffset(Pattern("world_3_maps.png").targetOffset(150,-70))
        self.clickWithRandomLocationAndResetMouse("map_3_3.png")
        self.make_decision()
        self.clickWithRandomLocationAndResetMouse("fight_start.png")
        wait("compass.png",600)
        self.clickWithRandomLocationAndResetMouse("compass.png")
        wait("formations.png",600)
        location = self.getLocation("formations.png")
        self.clickWithRandomOffset(Pattern("formations.png").targetOffset(-143,-32))
        self.__read_report()
        self.__send_retreat_command(location)
        return True
        
    @logged    
    def __read_report(self):  
        while not exists("night_attack_or_stop_pursuit.png") and not exists("fight_report.png"):
            sleep(5)

        self.clickIfExistsWithResetMouse(Pattern("night_attack_or_stop_pursuit.png").targetOffset(-100,0))
        #if not is_go_night_fight:
        #    clickIfExistsWithResetMouse(Pattern("night_attack_or_stop_pursuit.png").targetOffset(-100,0))
        #else:
        #    clickIfExistsWithResetMouse(Pattern("night_attack_or_stop_pursuit.png").targetOffset(105,-9))
        
    @logged    
    def __send_retreat_command(self, location):
        while not exists("advance_or_retreat.png"):
            self.clickWithRandomOffset(location, y_offset_base=20)
        
        self.clickWithRandomOffset(Pattern("advance_or_retreat.png").targetOffset(102,-12))
     
if __name__ == "__main__":
    fr = FightRunner()
    fr.run()
    