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

        # click level one ship and dismantling until no locked level one or other ship
        while exists("level_one.png") and not exists("desmantling_command.png"):
            self.clickWithResetMouse(Pattern("level_one.png").targetOffset(0,17))
            self.clickWithResetMouse("desmantling_command.png")
            wait(3)
    
        self.back_home_port()
    
if __name__ == "__main__":
    runner = DismantlingRunner()
    runner.run()