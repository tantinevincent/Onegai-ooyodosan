from common import Common, logged
from sikuli import *

class FightRunner(Common):
    @logged
    def run(self):
        self.clickWithResetMouse(Pattern("sortie.png").similar(0.60))
        self.clickWithResetMouse("fight.png")
        self.clickWithResetMouse(Pattern("worlds.png").targetOffset(4,5))
        self.clickWithResetMouse(Pattern("world_3_maps.png").targetOffset(150,-70))
        self.make_decision()
        self.clickWithResetMouse("fight_start.png")
        wait("compass.png",600)
        self.clickWithResetMouse("compass.png")
        wait("formations.png",600)
        self.clickWithResetMouse(Pattern("formations.png").targetOffset(-143,-32))
        self.__read_report()
        self.__send_retreat_command()
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
    def __send_retreat_command(self):
        while not exists("advance_or_retreat.png"):
            click(Location(700,200))
        
        self.clickWithResetMouse(Pattern("advance_or_retreat.png").targetOffset(102,-12))
     
if __name__ == "__main__":
    fr = FightRunner()
    fr.run()