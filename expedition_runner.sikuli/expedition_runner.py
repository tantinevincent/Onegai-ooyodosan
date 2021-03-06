from common import Common, logged
from expedition import Expedition
from fleet import Fleet
from sikuli import *
from config import Config

class ExpeditionRunner(Common):
    def __init__(self, fleets, expeditions, message=None):
        self.fleets = fleets
        self.expeditions = expeditions
        self.message = message
        
    @logged
    def run(self):
        if self.message is not None and not self.message.is_need_check():
            return True
    
        self.clickWithRandomLocationAndResetMouse(Pattern("sortie.png").similar(0.60))
        self.clickWithRandomLocationAndResetMouse("expedition.png")
        waitVanish("expedition.png")
        
        for fleet, expedition in zip(self.fleets, self.expeditions):
            self.__go_expedition(fleet, expedition)
            
        self.back_home_port()
        return True
    
    @logged
    def __go_expedition(self, fleet, expedition):
    
        self.clickWithRandomLocationAndResetMouse(expedition.getWorldImage())
        self.clickWithRandomLocationAndResetMouse(expedition.getImage())
	
        if exists("stop_expedition.png"):
            return
            
        self.make_decision()
        self.clickWithResetMouse(fleet.getNotSelectedImage())
        self.clickWithRandomLocationAndResetMouse("expedition_start.png")
        sleep(5)
                
if __name__ == "__main__":
    config_path = sys.argv[0] + "/../../config.ini"        #Executing from console
    config = Config(config_path)
    
    expedition_runner = ExpeditionRunner(config.expedition_fleets, config.expeditions)
    expedition_runner.run()