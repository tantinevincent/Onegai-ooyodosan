from common import Common, logged
from fleet import Fleet
from sikuli import *

class EnableRunner(Common):
    def __init__(self, enabled):
       self.enabled = enabled
       
    def run(self):
        return self.enabled
   
if __name__ == "__main__":
    runner = EnableRunner(True)
    print runner.run()