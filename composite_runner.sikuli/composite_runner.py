from common import Common, logged
from sikuli import *

class CompositeRunner():
    
    def __init__(self):
        self.runners = []
    
    def add_runner(self, runner):
        self.runners.append(runner)
    
    @logged
    def run(self):
        for runner in self.runners:
            still_running = runner.run()
            if not still_running:
                break
                
        return True