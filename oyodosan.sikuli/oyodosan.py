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

import random

config = None
level_up_runner = None
expedition_runner = None

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

######### BATH Related ###############################
@logged
def bathroom_command_set():
    clickWithResetMouse("docking.png")
    wait("base.png",20)
    print('need_check_bathroom_next')
    emptyBathroomNum = getEmptyBathroomNum()
    if emptyBathroomNum == 0:
        go_back_to_home_port()
        return
    
    clickBathroom()
    fleets = [Fleet(1)]
    ships = get_need_repairing_ship_in_fleets(fleets)
    
    if emptyBathroomNum > 1:
        otherShip = get_need_repairing_ship_not_in_fleets(fleets)
        ships += [otherShip] if otherShip is not None else []
        
    for ship in ships:
        click(ship)
        success = confirmShipToBathroom()
        if not success:
            continue
        if not hasBathroom():
            break
        clickBathroom()

    go_back_to_home_port()    

@logged
def getEmptyBathroomNum():
    return config.docker_num - len(safeFindAll("bucket.png"))
@logged
def hasBathroom():
    return getEmptyBathroomNum() > 0

@logged
def clickBathroom():
    clickWithResetMouse(Pattern("dock.png").targetOffset(-185,0))

@logged
def get_need_repairing_ship_in_fleets(fleets):
    ships = []
    for fleet in fleets:
        for mark_img in fleet.getAllImages():
            ships += safeFindAll(Pattern(mark_img).similar(0.85))

    return filter(isNotRepairing, ships)

@logged
def get_need_repairing_ship_not_in_fleets(fleets):
    base_location = find(Pattern("docking_titlebar.png").targetOffset(-40,0)).getTarget().below(20)
    OFFSET_Y = 30
    for i in xrange(0,3):
        target = Region(base_location.getX()-200, base_location.getY()+OFFSET_Y*i-10, 500, 40)
        if not is_in_fleets(target, fleets) and not target.exists("in_repairing.png"):
            return target.getCenter()

def is_in_fleets(target, fleets):
    for fleet in fleets:
        for mark_img in fleet.getAllImages():
            if target.exists(Pattern(mark_img).similar(0.85)):
                return True
    return False

@logged
def returnShipList():
    find("base.png").right(50).click()

@logged
def confirmShipToBathroom():
    clickWithResetMouse("docking_start.png")
    if not exists("ok.png"):
        returnShipList()
        return False
    
    clickWithResetMouse("ok.png")
    waitVanish("ok.png")
    return True

@logged
def isNotRepairing(ship):
    return not ship.right().exists("in_repairing.png")

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
        
def dismantle_ship():
    clickWithResetMouse("factory.png")
    clickWithResetMouse("dismantle.png")
    
@logged
def doAllJob(count):
    # Level UP
    level_up_runner.run()
    # Get Resource
    is_back = click_expedition_report()
    bathroom_command_set()
    click_expedition_report()
    setQuest()           
    #click_expedition_report()
    #is_back = True
    #while is_back:
    #   is_back = resupplyAndGoExpedition()
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
    
    level_up_runner = CompositeRunner()
    level_up_runner.add_runner(return_fleet_checker)
    level_up_runner.add_runner(FightChecker())
    level_up_runner.add_runner(ResupplyRunner([Fleet(1)], from_small_resuppy=True))
    level_up_runner.add_runner(return_fleet_checker)
    level_up_runner.add_runner(FightRunner())
    
    expedition_runner = CompositeRunner()
    expedition_runner.add_runner(ResupplyRunner(config.expedition_fleets))
    expedition_runner.add_runner(ExpeditionRunner(config.expedition_fleets, config.expeditions))
    
    mainloopWithException()
            