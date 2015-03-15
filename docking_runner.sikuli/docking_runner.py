from common import Common, logged
from fleet import Fleet
from sikuli import *

class DockingRunner(Common):
    def __init__(self, docker_num, fleets, is_fight=True):
        self.is_fight = is_fight
        self.docker_num = docker_num 
        self.all_fleet_marks = []
        for fleet in fleets:
            for mark_img in fleet.getAllImages():
                self.all_fleet_marks.append(mark_img)
        
    @logged
    def run(self):
        self.clickWithResetMouse("docking.png")
        wait("base.png",20)
        empty_dock_num = self.__get_empty_dock_num()
        if empty_dock_num == 0:
            self.back_home_port()  
            return True
        
        self.__click_docker()
        # no fight fleet or empty dock more than one
        chonse_no_fight_ships_flag = (not self.is_fight) or (empty_dock_num > 1)
        ships = self.__list_repairing_candidate(self.is_fight, chonse_no_fight_ships_flag)

        for ship in ships:
            click(ship)
            success = self.__confirm_docking()
            if not success:
                continue
            if self.__get_empty_dock_num() == 0:
                break
            self.__click_docker()

        self.back_home_port()  
        return True
    
    @logged
    def __get_empty_dock_num(self):
        return self.docker_num - len(self.safeFindAll("bucket.png"))
     
    @logged
    def __click_docker(self):
        self.clickWithResetMouse(Pattern("dock.png").targetOffset(-185,0))
    
    @logged
    def __list_repairing_candidate(self, is_include_fight_fleet, is_include_no_fight_fleet):
        ships = []
        if is_include_fight_fleet:
            ships += self.__get_in_fleets_ships()               
        if is_include_no_fight_fleet:
            ships += self.__get_not_in_fleets_ships()
        
        return ships

    @logged
    def __get_in_fleets_ships(self):
        ships = []
        for mark_img in self.all_fleet_marks:
            for ship in self.safeFindAll(Pattern(mark_img).similar(0.85)):
                if not ship.right().exists("in_repairing.png"):
                    ships.append(ship)
                    
        return ships
 
    @logged
    def __get_not_in_fleets_ships(self):
        base_location = find(Pattern("docking_titlebar.png").targetOffset(-40,0)).getTarget().below(20)
        OFFSET_Y = 30
        for i in xrange(0,self.docker_num):
            target = Region(base_location.getX()-200, base_location.getY()+OFFSET_Y*i-10, 500, 40)
            if not target.exists("in_repairing.png"):
                return [target.getCenter()] 
                
    @logged
    def __confirm_docking(self):
        self.clickWithResetMouse("docking_start.png")
        if not exists("ok.png"):
            self.__return_ship_list()
            return False
    
        self.clickWithResetMouse("ok.png")
        waitVanish("ok.png")
        return True
    
    @logged
    def __return_ship_list(self):
        find("base.png").right(50).click()
    
if __name__ == "__main__":
    runner = DockingRunner(2, [Fleet(1)], False)
    runner.run()
    