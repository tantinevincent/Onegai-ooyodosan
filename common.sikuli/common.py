from sikuli import *
from random import uniform

def logged(f):
    def wrapped(*args, **kwargs):
        print f.__name__ + " start"
        return f(*args, **kwargs)
    return wrapped 

class Common:
    def safeFindAll(self, target):
        try:
            result = [x for x in findAll(target)]
        except FindFailed:
            result = []
        return result

    def safeFind(self, target):
        try:
            result = [find(target)]
        except FindFailed:
            result = []
        return result

    def clickWithResetMouse(self, img):
        wait(img,30)
        click(img)
        self.reset_mouse()
        sleep(uniform(0,0.5))

    def clickIfExistsWithResetMouse(self, img):
        if exists(img,1):
            self.clickWithResetMouse(img)
    
    def getLocation(self, img): 
        return find(img).getCenter()
    
    def reset_mouse(self):
        hover(Location(0,0))
        
    def make_decision(self):
        self.clickWithResetMouse("decision.png")
        
    def back_home_port(self):
        self.clickWithResetMouse("home_port.png")