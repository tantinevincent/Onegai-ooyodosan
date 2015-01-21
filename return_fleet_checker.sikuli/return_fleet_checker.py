from common import Common, logged
from sikuli import *

class ReturnFleetChecker(Common):

    def __init__(self):
        self.hasReturnFleet = False
        
    @logged
    def run(self):
        while( True ):
            wait(Pattern("sortie.png").similar(0.60),60)
            if not exists("return_fleet_message.png"):
                break
            
            self.clickWithResetMouse("return_fleet_message.png")
            wait("next.png", 20)
            self.clickWithResetMouse("next.png")
            self.clickWithResetMouse("next.png")
            self.hasReturnFleet = True
        
        return True
         
if __name__ == "__main__":
    checker = ReturnFleetChecker()
    checker.run()