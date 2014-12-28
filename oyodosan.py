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

def command_click(img):
    wait(img,30)
    click(img)
    reset_mouse()

def command_click_if_exists(img):
    if exists(img,1):
        command_click(img)
        
def reset_mouse():
    hover(Location(0,0))
    
def go_back_main_page():
    command_click("base.png")
    
@logged
def depot_command_set():
    command_click("supply.png")
    
    TEAM_DEPOT_IMGS = ["1387032194821.png", "1387036182979.png", "1388059801467.png"]

    for TEAM_DEPOT_IMG in TEAM_DEPOT_IMGS:
        command_click(TEAM_DEPOT_IMG)
        if exists("1411897468603.png"):
            continue
        deployAction()
        
    go_back_main_page()

def expedition_select(team_img, expedition_img):
    command_click(expedition_img)
    if exists("1387038600652.png"):
        return
    command_click("decision.png")
    command_click(team_img)
   
    if exists("1398785493829.png"):
        return
    command_click("expedition_start.png")
@logged
def expedition_start_command_set():
    command_click(Pattern("sortie.png").similar(0.60))
    command_click("expedition.png")
    waitVanish("expedition.png")

    set_expedition_to_team(Pattern("1388846285376.png").similar(0.85), "1387033402847.png", TEAM_2_EXPEDITION)
    set_expedition_to_team(Pattern("1388846322199.png").similar(0.85), "1387033166364.png", TEAM_3_EXPEDITION)
    set_expedition_to_team(Pattern("1388846396919.png").similar(0.85), "1388059885299.png", TEAM_4_EXPEDITION)
    go_back_main_page()

def set_expedition_to_team(expeditionStartingImg,teamImg,expeditionNum):
    go_to_expedition_page(expeditionNum)
    if exists(expeditionStartingImg):
        return_first_expedition_page(expeditionNum)
        return;
    
    expedition_select(teamImg, give_expedition_img(expeditionNum) )
    sleep(3)
    return_first_expedition_page(expeditionNum)
    wait("1392385820341.png")
     
def go_to_expedition_page(expeditionNum):
    if expeditionNum >= 9 and expeditionNum <= 16:
        command_click("world_2.png")
    if expeditionNum >= 17 and expeditionNum <= 23:
        command_click("world_3.png")
    if expeditionNum >= 33 and expeditionNum <= 39:
        command_click("world_5.png")
        
def return_first_expedition_page(expeditionNum):
    if expeditionNum >= 9:
        command_click("world_1.png")
       
def give_expedition_img(expedition_num):
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
    BACK_FLAG_IMG = "1387039183276.png"
    has_back_ship = False
    while( True ):
        print('ready check report')
        wait(Pattern("sortie.png").similar(0.60),60)
        
        if not exists(BACK_FLAG_IMG):
            return has_back_ship;
        SOME_POSITION_IMG = BACK_FLAG_IMG
        command_click(SOME_POSITION_IMG)
        print('click next')
        wait("next.png", 20);
        command_click("next.png")
        command_click("next.png")
        has_back_ship = True

######### BATH Related ###############################
@logged
def bathroom_command_set():
    command_click("docking.png")
    wait("base.png",20)
    print('need_check_bathroom_next')
    emptyBathroomNum = getEmptyBathroomNum()
    if emptyBathroomNum == 0:
        go_back_main_page()
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

    go_back_main_page()    
    #putShipsToBathroom(getTeamOneShipList)
    #putShipsToBathroom(getOtherShipList, True)
    #go_back_main_page()

def getEmptyBathroomNum():
    return BATHROOM_NUM - len(safeFindAll("1415436564714.png"))
def hasBathroom():
    return getEmptyBathroomNum() > 0

def clickBathroom():
    command_click(Pattern("1391244821938.png").targetOffset(-185,0))
    
def getTeamOneShipList():
    ships = safeFind(Pattern("1389513591381.png").similar(0.85)) + safeFindAll(Pattern("1389513609792.png").similar(0.85))
    return filter(isNotRepairing, ships)

def getOtherShip():
    base_location = find(Pattern("1411742433993.png").targetOffset(-40,0)).getTarget().below(20)
    OFFSET_Y = 30
    for i in xrange(0,3):
        target = Region(base_location.getX()-200, base_location.getY()+OFFSET_Y*i-10, 500, 40)
        if not target.exists(Pattern("1389513609792.png").similar(0.85)) and not target.exists(Pattern("1389513591381.png").similar(0.85)) and not target.exists("1391245338826.png"):
            return target.getCenter()

def returnShipList():
    find("base.png").right(50).click()

def confirmShipToBathroom():
    command_click("docking_start.png")
    if not exists("ok.png"):
        returnShipList()
        return False
    
    command_click("ok.png")
    waitVanish("ok.png")
    return True

def isNotRepairing(ship):
    return not ship.right().exists("1391245338826.png")

@logged
def setQuest():
    command_click("quest.png")
    command_click("oyodo.png")
    
    while True:
        while exists("quest_success.png"):
            command_click("quest_success.png")
            
            while exists("close.png"):
                command_click("close.png")

        sleep(2)
        clickQuest(Pattern("1395100897154.png").similar(0.85))
        clickQuest(Pattern("1395054972516.png").similar(0.85))
        clickQuest("1389624013080.png")
        clickQuest(Pattern("1390781513309.png").similar(0.95))
        clickQuest(Pattern("1390710610032.png").similar(0.95))
        clickQuest(Pattern("1390726151408.png").similar(0.95))
        clickQuest(Pattern("1414973590474.png").similar(0.90))
        clickQuest(Pattern("1414316070741.png").similar(0.90))
        
        if not exists("1388156384056.png"):
            break
           
        command_click("1388156384056.png")
        
    command_click("back.png")

def clickQuest(img):
    if exists(img,1) and not find(img).right().exists("quest_activating.png"):
        command_click(img)

def readReport(is_go_night_fight= False):  
    while not exists("night_attack_or_stop_pursuit.png") and not exists("1389422324464.png"):
        sleep(5)

    if not is_go_night_fight:
        command_click_if_exists(Pattern("night_attack_or_stop_pursuit.png").targetOffset(-100,0))
    else:
        command_click_if_exists(Pattern("night_attack_or_stop_pursuit.png").targetOffset(105,-9))

def sendBackCommand(is_night_fight = False):
    while not exists(Pattern("advance_or_retreat.png").targetOffset(102,-12),1):
        click(Location(700,200))
        
    command_click(Pattern("advance_or_retreat.png").targetOffset(102,-12))
@logged
def checkTeamStatus():    
    command_click("organize.png")

    # Check Tired
    command_click("replenishment.png")
    command_click(Pattern("mamiya.png").targetOffset(22,-10))
    is_need_rest = exists("mamiya_prompt.png")
    command_click_if_exists(Pattern("mamiya_prompt.png").targetOffset(-73,71))
    command_click_if_exists(Pattern("replenishment_selection.png").targetOffset(241,37))

    if is_need_rest:
        go_back_main_page()
        return False
    
    # Check Damega
    DMAMGE_IMGS = ["bathing.png","minor_damage.png","moderate_damage.png","heavily_damage.png"]
    for damage_img in DMAMGE_IMGS:
        if exists(damage_img):
            can_fight = False
            go_back_main_page()
            return False
        
    command_click("supply_small.png")
    
    deployAction()
    go_back_main_page()
    return True

@logged
def goLevelUp():
    command_click(Pattern("sortie.png").similar(0.60))
    command_click("fight.png")
    command_click(Pattern("1401557578765.png").targetOffset(4,5))
    command_click(Pattern("1410532310092.png").targetOffset(150,-70))
    command_click("decision.png")
    command_click("fight_start.png")
    wait("compass.png",600)
    command_click("compass.png")
    wait("formations.png",600)
    command_click(Pattern("formations.png").targetOffset(-143,-32))
    readReport()
    sendBackCommand()

@logged
def deployAction():
    location = find(Pattern("1411739357686.png").targetOffset(-71,2)).getTarget()
    OFFSET_Y = 50
    for i in xrange(1,7):
        click(location.below(OFFSET_Y*i)) #click all supply checkbox
    command_click("resupply_everything .png")
    sleep(3)

@logged
def deployAndExpedition():
    is_back = True
    while is_back:
        depot_command_set()
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
        is_back = deployAndExpedition()
          
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
    command_click_if_exists("base.png")
    command_click_if_exists("back.png")
    sleep(3)
    if exists("sortie.png"):
        return
    
    # Can not back to base, restart kancolle
    restartKancolle()

@logged
def restartKancolle():
    isOnWelcomePage = False
    while not isOnWelcomePage:
        command_click(Pattern("reload.png").similar(0.80))
        sleep(10)
        isOnWelcomePage = exists(Pattern("welcome_page.png").targetOffset(209,156))
    command_click(Pattern("welcome_page.png").targetOffset(209,156))
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
