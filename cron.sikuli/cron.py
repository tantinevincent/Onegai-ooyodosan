from sikuli import *

class Cron:
    def __init__(self, round):
        self.round = round
        self.count = 0
        
    def run(self):
        self.count += 1
        return (self.count-1) % self.round == 0