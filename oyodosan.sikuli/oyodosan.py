from expedition import Expedition 
from fleet import Fleet
from quests import Quests
from config import Config
from fight_runner import FightRunner
from expedition_runner import ExpeditionRunner
from return_fleet_checker import ReturnFleetChecker
from resupply_runner import ResupplyRunner
from fight_checker import FightChecker
from composite_runner import CompositeRunner
from docking_runner import DockingRunner

import random

config = None
level_up_runner = None
expedition_runner = None
docking_runner = None

class Cron:
    def __init__(self, round=3):
        self.round = round
        self.count = 0
    def __call__(self, f):
        dctr_self = self
        def wrapped(*args, **kwargs):
            dctr_self.count += 1
            if (dctr_self.count-1) % dctr_self.round == 0:
                return f(*args, **kwargs)
        return wrapped    
        
def logged(f):
    def wrapped(*args, **kwargs):
        print f.__name__ + " start"
        return f(*args, **kwargs)
    return wrapped 

def safeFindAll(target):
    try:
        result = [x for x in findAll(target)]
    except FindFailed:
        result = []
    return result

def safeFind(target):
    try:
        result = [find(target)]
    except FindFailed:
        result = []
    return result

def clickWithResetMouse(img):
    wait(img,30)
    click(img)
    reset_mouse()

def clickIfExistsWithResetMouse(img):
    if exists(img,1):
        clickWithResetMouse(img)
       
def reset_mouse():
    hover(Location(0,0))

@logged    
def go_back_to_home_port():
    clickWithResetMouse("base.png")
    
@logged
def click_expedition_report():
    isFleetBack = False
    while( True ):
        print('ready check report')
        wait(Pattern("sortie.png").similar(0.60),60)
        if not exists("expedition_fleet_back_message.png"):
            return isFleetBack;
        
        clickWithResetMouse("expedition_fleet_back_message.png")
        print('click next')
        wait("next.png", 20);
        clickWithResetMouse("next.png")
        clickWithResetMouse("next.png")
        isFleetBack = True

@Cron(round = 5)
@logged
def setQuest():
    clickWithResetMouse("quest.png")
    clickWithResetMouse("oyodo.png")
    
    while True:
        while exists("quest_success.png"):
            clickWithResetMouse("quest_success.png")
            
            while exists("close.png"):
                clickWithResetMouse("close.png")

        sleep(2)
        for quests in config.quests_list:
            quest_type = quests.getTypeImage()
            print "find " + quest_type
            if not exists(Pattern(quest_type).similar(0.85)):
                continue
            for quest_img in quests.getAllImages():
                print "find " + quest_img
                clickQuest(Pattern(quest_img).similar(0.90))
        
        if not exists("quest_next_page.png"):
            break
           
        clickWithResetMouse("quest_next_page.png")
        
    clickWithResetMouse("back.png")

@logged
def clickQuest(img):
    if exists(img,1) and not find(img).right().exists("quest_activating.png"):
        clickWithResetMouse(img)
        
@logged
def doAllJob(count):
    # Level UP
    level_up_runner.run()
    # Get Resource
    docking_runner.run()
    click_expedition_report()
    setQuest()           
    expedition_runner.run()      
    #click_expedition_report()
    reset_mouse()

@logged
def mainloopWithException():
    count = 0
    while(True):
        try:
            print(count)
            switchApp(config.browser)
            doAllJob(count)
            random_sleep_time = random.randrange(int(config.sleep_time*0.9), int(config.sleep_time*1.1))
            print "sleep " + str(random_sleep_time) + " sec..."
            sleep(random_sleep_time)
            count += 1
        except FindFailed :
            print("find failed")
            returnToBase()

@logged
def returnToBase():
    clickIfExistsWithResetMouse("base.png")
    clickIfExistsWithResetMouse("back.png")
    sleep(3)
    if exists("sortie.png"):
        return
    
    # Can not back to base, restart kancolle
    restartKancolle()

@logged
def restartKancolle():
    isOnWelcomePage = False
    while not isOnWelcomePage:
        clickWithResetMouse(Pattern("reload.png").similar(0.80))
        sleep(10)
        isOnWelcomePage = exists(Pattern("welcome_page.png").targetOffset(209,156))
    clickWithResetMouse(Pattern("welcome_page.png").targetOffset(209,156))
    sleep(10)

if __name__ == "__main__":
    #config_path = sys.argv[0] + ".sikuli/../config.ini"   #Executing from sikuli IDE
    config_path = sys.argv[0] + "/../../config.ini"        #Executing from console
    config = Config(config_path)
    
    return_fleet_checker = ReturnFleetChecker()
    fight_fleets = [Fleet(1)]
    
    level_up_runner = CompositeRunner()
    level_up_runner.add_runner(return_fleet_checker)
    level_up_runner.add_runner(FightChecker())
    level_up_runner.add_runner(ResupplyRunner(fight_fleets, from_small_resuppy=True))
    level_up_runner.add_runner(return_fleet_checker)
    level_up_runner.add_runner(FightRunner())
    
    expedition_runner = CompositeRunner()
    expedition_runner.add_runner(return_fleet_checker)
    expedition_runner.add_runner(ResupplyRunner(config.expedition_fleets))
    expedition_runner.add_runner(return_fleet_checker)
    expedition_runner.add_runner(ExpeditionRunner(config.expedition_fleets, config.expeditions))
    
    docking_runner = CompositeRunner()
    docking_runner.add_runner(return_fleet_checker)
    docking_runner.add_runner(DockingRunner(config.docker_num, fight_fleets))
    
    mainloopWithException()
            