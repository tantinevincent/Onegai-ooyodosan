from common import Common, logged
from fleet import Fleet
from sikuli import *

class WhileRunner(Common):
    def __init__(self, img, runner):
        self.img = img 
        self.runner = runner
        
    @logged
    def run(self):
       while exists(self.img, 10):
           self.runner.run()
           
       return True
    