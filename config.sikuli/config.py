from ConfigParser import SafeConfigParser
from fleet import Fleet
from quests import Quests
from expedition import Expedition

class Config:

    def __init__(self, config_path):
        parser = SafeConfigParser()
        parser.read(config_path)
        # loading kancolle browser name
        self.browser = parser.get('system', 'KANCOLLE_BROWSER')
        # loading sleep time for each round (second)
        self.sleep_time = parser.getint('system', 'WAIT_TIME_SECOND')
        # loading docker number for repairing
        self.docker_num = parser.getint('fleet', 'BATHROOM_NUM')
        
		# loading enable setting
        self.fight_enabled = parser.getboolean('enable', 'fight')
        self.dismantling_enabled = parser.getboolean('enable', 'dismantling')
        
        # loading fight fleet
        self.fight_fleets = []
        for fleet_num, fight_world in self.__get_section_dict(parser, "fight").items():
            self.fight_fleets.append(Fleet(int(fleet_num)))
        
        # loading expedition fleet and expedition number
        self.expedition_fleets = []
        self.expeditions = []
        for fleet_num, expedition_num in self.__get_section_dict(parser, "expedition").items():
            self.expedition_fleets.append(Fleet(int(fleet_num)))
            self.expeditions.append(Expedition(int(expedition_num)))
            
        # loading quests        
        self.quests_list = []
        for type, ids_raw_str in self.__get_section_dict(parser, "quests").items():
            id_list = [id.strip() for id in ids_raw_str.split(',')]
            self.quests_list.append(Quests(type, id_list))
        
    def __get_section_dict(self, parser, section):
        section_dict = parser._sections[section]
        del section_dict["__name__"]
        return section_dict
        
if __name__ == "__main__":
    config_path = sys.argv[0] + "/../../config.ini"        #Executing from console
    run_config = Config(config_path)
    print run_config.browser
    print run_config.sleep_time
    print run_config.docker_num
    for fleet in run_config.expedition_fleets:
        print fleet.getImage()
        
    for expedition in run_config.expeditions:
        print expedition.getImage()
    
    print run_config.fight_enabled