from ConfigParser import SafeConfigParser

KANCOLLE_BROWSER = None
WAIT_TIME_SECOND = None
BATHROOM_NUM = None
TEAM_2_EXPEDITION = None
TEAM_3_EXPEDITION = None
TEAM_4_EXPEDITION = None

def logged(f):
    def wrapped():
        print f.__name__ + " start"
        return f()
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
    
def go_back_to_home_port():
    clickWithResetMouse("base.png")
    
@logged
def resupplyFleetsOfExpedition():
    clickWithResetMouse("supply.png")
    for team_mark in ["team_2_mark_not_selected.png", "team_3_mark_not_selected.png", "team_4_mark_not_selected.png"]:
        clickWithResetMouse(team_mark)
        if not exists("status_on_expedition.png"):
            resupplyFleet()
        
    go_back_to_home_port()

@logged
def expedition_start_command_set():
    clickWithResetMouse(Pattern("sortie.png").similar(0.60))
    clickWithResetMouse("expedition.png")
    waitVanish("expedition.png")

    goExpedition(Pattern("team_2_mark.png").similar(0.85), "team_2_mark.png", TEAM_2_EXPEDITION)
    goExpedition(Pattern("team_3_mark.png").similar(0.85), "team_3_mark_not_selected.png", TEAM_3_EXPEDITION)
    goExpedition(Pattern("team_4_mark.png").similar(0.85), "team_4_mark_not_selected.png", TEAM_4_EXPEDITION)
    go_back_to_home_port()

def goExpedition(onExpeditionImg,teamImg,expeditionNum):
    world_img = getWorldImageAboutExpedition(expeditionNum)
    clickWithResetMouse(world_img)
    if exists(onExpeditionImg):
        return;
    
    expedition_img = getExpeditionImage(expeditionNum)
    clickWithResetMouse(expedition_img)
    
    if exists("stop_expedition.png"):
        return
    clickWithResetMouse("decision.png")
    clickWithResetMouse(teamImg)
    if exists("status_on_expedition.png"):
        return
    clickWithResetMouse("expedition_start.png")
    sleep(5)
     
def getWorldImageAboutExpedition(expeditionNum):
    if expeditionNum < 9:
        return "world_1.png"
    if expeditionNum >= 9 and expeditionNum <= 16:
        return "world_2.png"
    if expeditionNum >= 17 and expeditionNum <= 23:
        return "world_3.png"
    if expeditionNum >= 33 and expeditionNum <= 39:
        return "world_5.png"

def getExpeditionImage(expedition_num):
    if expedition_num == 2:
        return "expedition_2.png"
    if expedition_num == 3:
        return "expedition_3.png"
    if expedition_num == 5:
        return "expedition_5.png"
    if expedition_num == 6:
        return "expedition_6.png"
    if expedition_num == 9:
        return "expedition_9.png"
    if expedition_num == 11:
        return "expedition_11.png"
    if expedition_num == 13:
        return "expedition_13.png"
    if expedition_num == 21:
        return "expedition_21.png"
    if expedition_num == 36:
        return "expedition_36.png"
    if expedition_num == 37:
        return "expedition_37.png"
    if expedition_num == 38:
        return "expedition_38.png"

@logged
def click_expedition_report():
    print('check report')
    isFleetBack = False
    while( True ):
        print('ready check report')
        wait(Pattern("sortie.png").similar(0.60),60)
        if not exists("expedition_team_back_message.png"):
            return isFleetBack;
        
        clickWithResetMouse("expedition_team_back_message.png")
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
    ships = getTeamOneShipList()
    
    if emptyBathroomNum > 1:
        otherShip = getOtherShip()
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
    #putShipsToBathroom(getTeamOneShipList)
    #putShipsToBathroom(getOtherShipList, True)
    #go_back_to_home_port()

def getEmptyBathroomNum():
    return BATHROOM_NUM - len(safeFindAll("bucket.png"))
def hasBathroom():
    return getEmptyBathroomNum() > 0

def clickBathroom():
    clickWithResetMouse(Pattern("dock.png").targetOffset(-185,0))
    
def getTeamOneShipList():
    ships = safeFind(Pattern("team_1_flagship_mark.png").similar(0.85)) + safeFindAll(Pattern("team_1_mark.png").similar(0.85))
    return filter(isNotRepairing, ships)

def getOtherShip():
    base_location = find(Pattern("docking_titlebar.png").targetOffset(-40,0)).getTarget().below(20)
    OFFSET_Y = 30
    for i in xrange(0,3):
        target = Region(base_location.getX()-200, base_location.getY()+OFFSET_Y*i-10, 500, 40)
        if not target.exists(Pattern("team_1_mark.png").similar(0.85)) and not target.exists(Pattern("team_1_flagship_mark.png").similar(0.85)) and not target.exists("in_repairing.png"):
            return target.getCenter()

def returnShipList():
    find("base.png").right(50).click()

def confirmShipToBathroom():
    clickWithResetMouse("docking_start.png")
    if not exists("ok.png"):
        returnShipList()
        return False
    
    clickWithResetMouse("ok.png")
    waitVanish("ok.png")
    return True

def isNotRepairing(ship):
    return not ship.right().exists("in_repairing.png")

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
        clickQuest(Pattern("quest_d2.png").similar(0.85))
        clickQuest(Pattern("quest_d4.png").similar(0.85))
        clickQuest("quest_type_docking_or_supply.png")
        clickQuest(Pattern("quest_bd1.png").similar(0.95))
        clickQuest(Pattern("quest_bd2.png").similar(0.95))
        clickQuest(Pattern("quest_bd3.png").similar(0.95))
        clickQuest(Pattern("quest_d9.png").similar(0.90))
        clickQuest(Pattern("quest_d11.png").similar(0.90))
        
        if not exists("quest_next_page.png"):
            break
           
        clickWithResetMouse("quest_next_page.png")
        
    clickWithResetMouse("back.png")

def clickQuest(img):
    if exists(img,1) and not find(img).right().exists("quest_activating.png"):
        clickWithResetMouse(img)

def readReport(is_go_night_fight= False):  
    while not exists("night_attack_or_stop_pursuit.png") and not exists("fight_report.png"):
        sleep(5)

    if not is_go_night_fight:
        clickIfExistsWithResetMouse(Pattern("night_attack_or_stop_pursuit.png").targetOffset(-100,0))
    else:
        clickIfExistsWithResetMouse(Pattern("night_attack_or_stop_pursuit.png").targetOffset(105,-9))

def sendBackCommand(is_night_fight = False):
    while not exists(Pattern("advance_or_retreat.png").targetOffset(102,-12),1):
        click(Location(700,200))
        
    clickWithResetMouse(Pattern("advance_or_retreat.png").targetOffset(102,-12))

@logged
def checkTeamStatus():    
    clickWithResetMouse("organize.png")

    # Check Tired
    clickWithResetMouse("replenishment.png")
    clickWithResetMouse(Pattern("mamiya.png").targetOffset(22,-10))
    if not exists("mamiya_prompt.png"):
        clickWithResetMouse(Pattern("replenishment_selection.png").targetOffset(241,37))
        go_back_to_home_port()
        return False
    clickIfExistsWithResetMouse(Pattern("mamiya_prompt.png").targetOffset(14,89))
    # Check Damega
    for damage_img in ["status_repair_damage.png","status_minor_damage.png","status_moderate_damage.png","status_heavily_damage.png"]:
        if exists(damage_img):
            go_back_to_home_port()
            return False
        
    clickWithResetMouse("supply_small.png")
    resupplyFleet()
    go_back_to_home_port()
    return True

@logged
def goLevelUp():
    clickWithResetMouse(Pattern("sortie.png").similar(0.60))
    clickWithResetMouse("fight.png")
    clickWithResetMouse(Pattern("worlds.png").targetOffset(4,5))
    clickWithResetMouse(Pattern("world_3_maps.png").targetOffset(150,-70))
    clickWithResetMouse("decision.png")
    clickWithResetMouse("fight_start.png")
    wait("compass.png",600)
    clickWithResetMouse("compass.png")
    wait("formations.png",600)
    clickWithResetMouse(Pattern("formations.png").targetOffset(-143,-32))
    readReport()
    sendBackCommand()

@logged
def resupplyFleet():
    location = find(Pattern("resupply_team_marks.png").targetOffset(-71,2)).getTarget()
    OFFSET_Y = 50
    for i in xrange(1,7):
        click(location.below(OFFSET_Y*i)) #click all resupply check box
    clickWithResetMouse("resupply_everything.png")
    sleep(3)

@logged
def resupplyAndGoExpedition():
    is_back = True
    while is_back:
        resupplyFleetsOfExpedition()
        is_back = click_expedition_report()
        
    expedition_start_command_set()
    return click_expedition_report()

def doAllJob(count):
    # Level UP
    is_back = click_expedition_report()   
    can_figit = checkTeamStatus()    
    is_back = click_expedition_report()
    if can_figit:
        goLevelUp()
    # Get Resource
    is_back = click_expedition_report()
    bathroom_command_set()
    if count %5 == 0:    
        click_expedition_report()
        setQuest()
            
    click_expedition_report()
    is_back = True
    while is_back:
        is_back = resupplyAndGoExpedition()
          
    #click_expedition_report()
    reset_mouse()
    
def mainloopWithException():
    count = 0
    while(True):
        try:
            print(count)
            switchApp(KANCOLLE_BROWSER)
            doAllJob(count)
            sleep(WAIT_TIME_SECOND)
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
    config_path = sys.argv[0] + ".sikuli/config"
    parser = SafeConfigParser()
    parser.read(config_path)
    WAIT_TIME_SECOND = parser.getint('system', 'WAIT_TIME_SECOND')
    KANCOLLE_BROWSER = parser.get('system', 'KANCOLLE_BROWSER')
    BATHROOM_NUM = parser.getint('fleet', 'BATHROOM_NUM')
    TEAM_2_EXPEDITION = parser.getint('expedition', 'TEAM_2')
    TEAM_3_EXPEDITION = parser.getint('expedition', 'TEAM_3')
    TEAM_4_EXPEDITION = parser.getint('expedition', 'TEAM_4')

    mainloopWithException()
