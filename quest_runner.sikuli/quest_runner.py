from common import Common, logged
from fleet import Fleet
from sikuli import *
from config import Config

class QuestRunner(Common):
    def __init__(self, quests_list):
        self.quests_list = quests_list 
        
    @logged
    def run(self):
        self.clickWithRandomLocationAndResetMouse("quest.png")
        while exists("oyodo.png"):
            self.clickWithRandomLocationAndResetMouse("oyodo.png")
            sleep(1)

        self.clickWithRandomLocationAndResetMouse("accepted_quest.png")
        self.__recieve_all_rewards()

	quest_categories = ["quest_category_daily.png",
                            "quest_category_weekly.png"]
        
	for category in quest_categories:
            while True:
                self.clickWithRandomLocationAndResetMouse(category)
                self.__check_quest_page()
                if not exists("quest_next_page.png"):
                    break    
            
                self.clickWithRandomOffset("quest_next_page.png", 
                                           x_offset_base=3, y_offset_base=2)
            
        self.back_home_port_from_quest()  
        return True

    @logged
    def __recieve_all_rewards(self):
        while exists("quest_success.png"):            
            self.clickWithRandomLocationAndResetMouse("quest_success.png")
            while exists("close.png"):
                self.clickWithRandomLocationAndResetMouse("close.png")            
    @logged
    def __check_quest_page(self):       
        sleep(2) # wait update quest list
        for quests in self.quests_list:
            for quest_img in quests.getAllImages():
                self._click_quest(Pattern(quest_img).similar(0.90))
    
    def _click_quest(self, img):
        match = exists(img)
        if not match:
            return 
    
        if match.right().exists("quest_activating.png"):
            return
        
        region = Region(match.x + match.w, match.y, 60, 60)
        self.clickWithRandomLocationAndResetMouse(region)
    

if __name__ == "__main__":
    config_path = sys.argv[0] + "/../config.ini"        #Executing from console
    config = Config(config_path)
    runner = QuestRunner(config.quests_list)
    runner.run()
