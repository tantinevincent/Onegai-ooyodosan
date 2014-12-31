class Fleet:
    def __init__(self, fleetNum):
        self.fleetNum = fleetNum
     
    def getImage(self):
        return "fleet_" + str(self.fleetNum) + "_mark.png"
    
    def getNotSelectedImage(self):
        return "fleet_" + str(self.fleetNum) + "_mark_not_selected.png"
