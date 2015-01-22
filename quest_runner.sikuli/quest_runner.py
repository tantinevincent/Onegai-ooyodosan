from common import Common, logged
from fleet import Fleet
from sikuli import *
from config import Config

class QuestRunner(Common):
    def __init__(self, quests_list):
        self.quests_list = quests_list 
        
    @logged
    def run(self):
        self.clickWithResetMouse("quest.png")
        self.clickWithResetMouse("oyodo.png")
        
        while True:
            self.__check_quest_page()
            if not exists("quest_next_page.png"):
                break    
            
            self.clickWithResetMouse("quest_next_page.png")
            
        self.back_home_port()  
        return True
     
    @logged
    def __check_quest_page(self):
        while exists("quest_success.png"):
            self.__recieve_reward()
        
        sleep(2) # wait update quest list
        for quests in self.quests_list:
            if not exists(Pattern(quests.getTypeImage()).similar(0.85)):
                continue
        
            for quest_img in quests.getAllImages():
                self.__click_quest(Pattern(quest_img).similar(0.90))
    
    @logged
    def __click_quest(self,img):
        if not exists(img):
            return 
    
        if not find(img).right().exists("quest_activating.png"):
            self.clickWithResetMouse(img)
    
    @logged
    def __recieve_reward(self):
        self.clickWithResetMouse("quest_success.png")
        while exists("close.png"):
            self.clickWithResetMouse("close.png")
    
    @logged
    def back_home_port(self):
        self.clickWithResetMouse("back.png")
    
if __name__ == "__main__":
    config_path = sys.argv[0] + "/../../config.ini"        #Executing from console
    config = Config(config_path)
    runner = QuestRunner(config.quests_list)
    runner.run()