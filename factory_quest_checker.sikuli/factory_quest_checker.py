from common import logged
from fleet import Fleet
from sikuli import *
from config import Config

class FactoryQuestChecker():
    def __init__(self, quests_list, factory_runner):
        self.factory_quests = None
        for quests in quests_list:
            if quests.type == "factory":
                self.factory_quests = quests
         
        self.factory_runner = factory_runner        
        
    @logged
    def check(self):
        if self.factory_quests == None:
            return
    
        for quest_img in self.factory_quests.getAllImages():
            if exists(Pattern(quest_img).similar(0.95)) and find(quest_img).right().exists("activated.png"):
                self.factory_runner.set_target_quest(quest_img)
                break