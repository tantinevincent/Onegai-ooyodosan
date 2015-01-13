from common import Common, logged
from sikuli import *

class DismantlingRunner(Common):
    
    @logged
    def run(self):
        self.clickWithResetMouse("factory.png")
        self.clickWithResetMouse("dismantling.png")
        
        # click sorting button until sorting by "new"
        while not exists( Pattern("sorting_new_button.png").similar(0.85)):
            self.clickWithResetMouse( Pattern("ship_list_titlebar.png").targetOffset(170,0) )
            
        ships = self.safeFindAll("high_speed_mark.png") + self.safeFindAll("low_speed_mark.png")
        for ship in ships:
            click(ship)
            #self.clickWithResetMouse(ship)
            self.clickWithResetMouse("desmantling_command.png")
            wait(3)
        
        #self.back_home_port()    
    
if __name__ == "__main__":
    runner = DismantlingRunner()
    runner.run()