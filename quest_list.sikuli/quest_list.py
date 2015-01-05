class QuestList:
    def __init__(self, quest_type, quest_num_list):
        self.quest_type = quest_type
        self.quest_num_list = quest_num_list
        
    def getQuestTypeImage(self):
        return "quest_type_" + self.quest_type + ".png"
        
    def getAllQuestImages(self):
        return ["quest_" + self.quest_type + str(num) + ".png" for num in self.quest_num_list]