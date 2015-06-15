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
        self.clickWithRandomLocationAndResetMouse("docking.png")
        wait("base.png", 20)
        empty_dock_num = self.__get_empty_dock_num()
        if empty_dock_num == 0:
            self.back_home_port()  
            return True
        
        self._click_docker()
        # no fight fleet or empty dock more than one
        chonse_no_fight_ships_flag = (not self.is_fight) or (empty_dock_num > 1)
        ships = self.__list_repairing_candidate(self.is_fight, chonse_no_fight_ships_flag)

        for ship in ships:
            print "click ship"
            self.clickWithRandomOffset(ship, x_offset_base=50, y_offset_base=8)
            success = self.__confirm_docking()
            if not success:
                continue
            if self.__get_empty_dock_num() == 0:
                break
            self._click_docker()

        self.back_home_port()  
        return True
    
    @logged
    def __get_empty_dock_num(self):
        return self.docker_num - len(self.safeFindAll("bucket.png"))
     
    @logged
    def _click_docker(self):
        self.clickWithRandomOffset(Pattern("dock.png").targetOffset(-185,0), x_offset_base=30, y_offset_base=10)
    
    @logged
    def __list_repairing_candidate(self, is_include_fight_fleet, is_include_no_fight_fleet):
        ships = []
        if is_include_fight_fleet:
            ships += self._get_in_fleets_ships()               
        if is_include_no_fight_fleet:
            ships += self._get_not_in_fleets_ships()
        
        return ships

    @logged
    def _get_in_fleets_ships(self):
        ships = []
        for mark_img in self.all_fleet_marks:
            for ship in self.safeFindAll(Pattern(mark_img).similar(0.85)):
                if not ship.right().exists("in_repairing.png"):
                    ships.append(ship.getCenter().offset(250, 0))
                    
        return ships
 
    @logged
    def _get_not_in_fleets_ships(self):
        base_location = find("docking_titlebar.png").getTarget()
        OFFSET_Y = 31
        for i in xrange(1, 11):
            location = base_location.offset(0, i*OFFSET_Y)
            region = Region(location.getX()-200, location.getY()-20, 500, 40)
            if not region.exists("in_repairing.png"):
                return [region.getCenter()] 

        return []
 
    @logged
    def __confirm_docking(self):
        self.clickWithRandomLocationAndResetMouse("docking_start.png")
        if not exists("ok.png"):
            self._return_ship_list()
            return False
    
        self.clickWithRandomLocationAndResetMouse("ok.png")
        waitVanish("ok.png")
        return True
    
    @logged
    def _return_ship_list(self):
        find("base.png").right(50).click()
    
if __name__ == "__main__":
    runner = DockingRunner(2, [Fleet(1)], True)
    runner.run()
    #hover(runner._get_not_in_fleets_ships()[0])
    #hover(runner._get_in_fleets_ships()[0])