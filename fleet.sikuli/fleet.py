class Fleet:
    def __init__(self, fleet_num):
        self.fleet_num = fleet_num
        self.has_flag_ship = (fleet_num == 1)
     
    def getImage(self):
        return "fleet_" + str(self.fleet_num) + "_mark.png"
    
    def getNotSelectedImage(self):
        return "fleet_" + str(self.fleet_num) + "_mark_not_selected.png"
        
    def getAllImages(self):
        ship_mark = "fleet_" + str(self.fleet_num) + "_mark.png"
        if not self.has_flag_ship:
            return [ship_mark]
            
        flag_ship_mark = "fleet_" + str(self.fleet_num) + "_flagship_mark.png"
        return [flag_ship_mark, ship_mark]
        
