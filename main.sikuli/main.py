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
from quest_runner import QuestRunner
from cron import Cron
from dismantling_runner import DismantlingRunner
from enable_runner import EnableRunner
from while_runner import WhileRunner

import random

config = None
level_up_runner = None
expedition_runner = None
docking_runner = None
questing_runner = None
dismantling_runner = None

def logged(f):
    def wrapped(*args, **kwargs):
        print f.__name__ + " start"
        return f(*args, **kwargs)
    return wrapped 

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
def doAllJob(count):
    # Level UP
    level_up_runner.run()
    # Docking
    docking_runner.run()
    # Fleet expedition
    expedition_runner.run()    
    # Quest check
    questing_runner.run()  
    # Dismantling
    dismantling_runner.run()
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
    
    level_up_runner = CompositeRunner()
    level_up_runner.add_runner(EnableRunner(config.fight_enabled))
    level_up_runner.add_runner(return_fleet_checker)
    level_up_runner.add_runner(FightChecker())
    level_up_runner.add_runner(ResupplyRunner(config.fight_fleets, from_small_resuppy=True))
    level_up_runner.add_runner(return_fleet_checker)
    level_up_runner.add_runner(FightRunner())
    
    docking_runner = CompositeRunner()
    docking_runner.add_runner(return_fleet_checker)
    docking_runner.add_runner(DockingRunner(config.docker_num, config.fight_fleets, is_fight=config.fight_enabled))
    
    resupply_runner = CompositeRunner()
    resupply_runner.add_runner(return_fleet_checker)
    resupply_runner.add_runner(ResupplyRunner(config.expedition_fleets))
    
    expedition_runner = CompositeRunner()
    expedition_runner.add_runner(resupply_runner)
    expedition_runner.add_runner(WhileRunner("return_fleet_message.png", resupply_runner))
    expedition_runner.add_runner(ExpeditionRunner(config.expedition_fleets, config.expeditions))
    
    questing_runner = CompositeRunner()
    questing_runner.add_runner(Cron(5))
    questing_runner.add_runner(return_fleet_checker)
    questing_runner.add_runner(QuestRunner(config.quests_list))
    
    dismantling_runner = CompositeRunner()
    dismantling_runner.add_runner(EnableRunner(config.dismantling_enabled))
    dismantling_runner.add_runner(Cron(30))
    dismantling_runner.add_runner(return_fleet_checker)
    dismantling_runner.add_runner(DismantlingRunner())
    
    mainloopWithException()
            