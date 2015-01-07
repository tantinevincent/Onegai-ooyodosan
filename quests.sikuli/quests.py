class Quests:
    def __init__(self, type, id_list):
        self.type = type
        self.id_list = id_list
        
    def getTypeImage(self):
        return "quest_type_" + self.type + ".png"
        
    def getAllImages(self):
        return ["quest_" + id + ".png" for id in self.id_list]