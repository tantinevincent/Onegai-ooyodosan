from common import Common, logged
from fleet import Fleet
from sikuli import *
from config import Config
from factory_quest_checker import FactoryQuestChecker

class FactoryRunner(Common):
    def __init__(self):
        self.target_quest = None      
        
    @logged
    def set_target_quest(self, quest):
        self.target_quest = quest 

    @logged
    def run(self):
        if self.target_quest == None:
            return True
        
        self.clickWithResetMouse("factory.png")
        if self.target_quest == "quest_f5.png":
            self.__development()
        if self.target_quest == "quest_f6.png":
            self.__construction()
        if self.target_quest == "quest_f7.png":   
            for _ in xrange(3):
                self.__development()
            
        self.back_home_port()
        self.target_quest = None
        return True
    
    def __development(self):
        self.clickWithResetMouse("development.png")
        self.clickWithResetMouse("start_development.png")
        sleep(10)
        self.clickWithResetMouse("back.png")
    
    def __construction(self):
        self.clickWithResetMouse("construction.png")
        self.clickWithResetMouse("start_construction.png")
        sleep(5)
    
if __name__ == "__main__":
    config_path = sys.argv[0] + "/../../config.ini"        #Executing from console
    config = Config(config_path)
    
    runner = FactoryRunner()
    checker = FactoryQuestChecker(config.quests_list, runner)
    checker.check()
    print "check over."
    sleep(5)
    runner.run()