class Expedition:
    def __init__(self, expeditionNum):
        if expeditionNum <= 0:
            raise ValueError("Expedition number should not less than zero.")
        self.expeditionNum = expeditionNum
        self.worldNum = (expeditionNum-1) / 8 + 1
        
    def getWorldImage(self):
        return "world_" + str(self.worldNum) + ".png"
     
    def getImage(self):
        return "expedition_" + ("0" if self.expeditionNum < 10 else "") + str(self.expeditionNum) + ".png"