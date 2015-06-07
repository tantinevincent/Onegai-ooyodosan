from sikuli import *
from random import uniform, randint

def logged(f):
    def wrapped(*args, **kwargs):
        print f.__name__ + " start"
        return f(*args, **kwargs)
    return wrapped 

class Common:
    def safeFindAll(self, target, target_region=None):
        try:
            if target_region is None:
                result = [x for x in findAll(target)]
            else:
                result = [x for x in target_region.findAll(target)]
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
        match = wait(img,30)
        sleep(uniform(0,0.1))
        click(match)
        self.reset_mouse()

    def clickWithRandomLocationAndResetMouse(self, img):
        match = wait(img,30)
        sleep(uniform(0,0.5))
        x = randint(match.getX(), match.getX()+match.getW())
        y = randint(match.getY(), match.getY()+match.getH())
        #hover(Location(x,y))
        click(Location(x,y))
        self.reset_mouse()
    
    def clickWithRandomOffset(self, img, x_offset_base=5, y_offset_base=5, is_reset_mouse=True):
        x, y = 0, 0
        if not isinstance(img, Location):
            match = wait(img,30)
            x = match.getTarget().getX() + randint(-x_offset_base, x_offset_base)
            y = match.getTarget().getY() + randint(-y_offset_base, y_offset_base)
        else:
            x = img.getX() + randint(-x_offset_base, x_offset_base)
            y = img.getY() + randint(-y_offset_base, y_offset_base)
        
        sleep(uniform(0,0.5))
        click(Location(x,y))
        if is_reset_mouse:
            self.reset_mouse()
        
    def clickIfExistsWithResetMouse(self, img):
        if exists(img,1):
            self.clickWithResetMouse(img)
    
    def getLocation(self, img): 
        return find(img).getCenter()
    
    def reset_mouse(self):
        hover(Location(0,0))
        
    def make_decision(self):
        self.clickWithRandomLocationAndResetMouse("decision.png")
        
    def back_home_port(self):
        self.clickWithRandomLocationAndResetMouse("home_port.png")
        
        