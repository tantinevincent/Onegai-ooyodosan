from common import Common, logged
from expedition import Expedition
from fleet import Fleet
from sikuli import *
from config import Config

class ExpeditionRunner(Common):
    def __init__(self, fleets, expeditions):
        self.fleets = fleets
        self.expeditions = expeditions
        
    @logged
    def run(self):
        self.clickWithResetMouse(Pattern("sortie.png").similar(0.60))
        self.clickWithResetMouse("expedition.png")
        waitVanish("expedition.png")
        
        for fleet, expedition in zip(self.fleets, self.expeditions):
            self.__go_expedition(fleet, expedition)
            
        self.back_home_port()    
    
    @logged
    def __go_expedition(self, fleet, expedition):
    
        self.clickWithResetMouse(expedition.getWorldImage())
        # if fleet is on expedition
        if exists(fleet.getImage()):
            return;
    
        self.clickWithResetMouse(expedition.getImage())
	
        if exists("stop_expedition.png"):
            return
            
        self.make_decision()
        self.clickWithResetMouse(fleet.getNotSelectedImage())
        self.clickWithResetMouse("expedition_start.png")
        sleep(5)
                
if __name__ == "__main__":
    config_path = sys.argv[0] + "/../../config.ini"        #Executing from console
    config = Config(config_path)
    
    expedition_runner = ExpeditionRunner(config.expedition_fleets, config.expeditions)
    expedition_runner.run()