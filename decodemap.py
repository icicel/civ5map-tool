import struct

# Help functions

def get_structs_of_size(byte_string, size):
    if len(byte_string) % size != 0:
        raise ValueError("Byte string of length", len(byte_string), "can not be composed of structs of size", size)
    structs = []
    for i in range(0, len(byte_string), size):
        structs.append(byte_string[i:i+size])
    return structs
def strip_at_first_null(byte_string):
    return byte_string.split(b'\x00')[0]

# File handler (I think)

class DecodeMap:
    def __init__(self, f):

        ### Read map data

        F_HEAD = f.read(1)
        F_MAPWIDTH = f.read(4)
        F_MAPHEIGHT = f.read(4)
        F_PLAYERS_C = f.read(1)
        F_SETTINGS = f.read(4)
        is_scenario = F_HEAD[0] & 0b10000000 >> 7
        version = F_HEAD[0] & 0b00001111
        map_width = int.from_bytes(F_MAPWIDTH, "little")
        map_height = int.from_bytes(F_MAPHEIGHT, "little")
        num_players = int.from_bytes(F_PLAYERS_C, "little")
        world_wrap = F_SETTINGS[0] & 0b00000100 >> 2
        random_resources = F_SETTINGS[0] & 0b00000010 >> 1
        random_goodies = F_SETTINGS[0] & 0b00000001

        F_TERRAINS_L = f.read(4)
        F_FEATURES_L = f.read(4)
        F_WONDERS_L = f.read(4)
        F_RESOURCES_L = f.read(4)
        F_MODDATA_L = f.read(4)
        F_TITLE_L = f.read(4)
        F_DESCRIPTION_L = f.read(4)
        terrains_l = int.from_bytes(F_TERRAINS_L, "little")
        features_l = int.from_bytes(F_FEATURES_L, "little")
        wonders_l = int.from_bytes(F_WONDERS_L, "little")
        resources_l = int.from_bytes(F_RESOURCES_L, "little")
        mod_data_l = int.from_bytes(F_MODDATA_L, "little")
        title_l = int.from_bytes(F_TITLE_L, "little")
        description_l = int.from_bytes(F_DESCRIPTION_L, "little")

        F_TERRAINS = f.read(terrains_l)
        F_FEATURES = f.read(features_l)
        F_WONDERS = f.read(wonders_l)
        F_RESOURCES = f.read(resources_l)
        F_MODDATA = f.read(mod_data_l)
        F_TITLE = f.read(title_l)
        F_DESCRIPTION = f.read(description_l)
        terrains = F_TERRAINS.split(b'\x00')[:-1]
        features = F_FEATURES.split(b'\x00')[:-1]
        wonders = F_WONDERS.split(b'\x00')[:-1]
        resources = F_RESOURCES.split(b'\x00')[:-1]
        mod_data = F_MODDATA[:-1]
        title = F_TITLE[:-1]
        description = F_DESCRIPTION[:-1]

        F_WORLDSIZE_L = f.read(4)
        world_size_l = int.from_bytes(F_WORLDSIZE_L, "little")

        F_WORLDSIZE = f.read(world_size_l)
        world_size = F_WORLDSIZE.strip(b'\x00')

        F_CELLS = f.read(map_height * map_width * 8)
        cells = {}
        c = 0
        for y in range(map_height):
            for x in range(map_width):
                cell = F_CELLS[c:c+8]
                c += 8
                terrain, resource, feature, river, elevation, continent, wonder, resource_c = struct.unpack("8b", cell)
                cells[(x, y)] = (terrain, resource, feature, river, elevation, continent, wonder, resource_c)



        ### Read scenario data

        F_GAMESPEED = f.read(64)
        f.read(4)
        F_MAXTURNS = f.read(4)
        f.read(4)
        F_STARTYEAR = f.read(4)
        F_PLAYERCIVS_C = f.read(1)
        F_MINORCIVS_C = f.read(1)
        F_TEAMS_C = f.read(1)
        f.read(1)
        game_speed = F_GAMESPEED.strip(b'\x00')
        max_turns = int.from_bytes(F_MAXTURNS, "little")
        start_year = struct.unpack("l", F_STARTYEAR)[0]
        num_player_civs = int.from_bytes(F_PLAYERCIVS_C, "little")
        num_minor_civs = int.from_bytes(F_MINORCIVS_C, "little")
        num_teams = int.from_bytes(F_TEAMS_C, "little")

        F_IMPROVEMENTS_L = f.read(4)
        F_UNITTYPES_L = f.read(4)
        F_TECHS_L = f.read(4)
        F_POLICIES_L = f.read(4)
        F_BUILDINGS_L = f.read(4)
        F_PROMOTIONS_L = f.read(4)
        F_UNITDATA_L = f.read(4)
        F_UNITNAMES_L = f.read(4)
        F_CITYDATA_L = f.read(4)
        F_VICTORYDATA_L = f.read(4)
        F_GAMEOPTIONS_L = f.read(4)
        improvements_l = int.from_bytes(F_IMPROVEMENTS_L, "little")
        unit_types_l = int.from_bytes(F_UNITTYPES_L, "little")
        techs_l = int.from_bytes(F_TECHS_L, "little")
        policies_l = int.from_bytes(F_POLICIES_L, "little")
        buildings_l = int.from_bytes(F_BUILDINGS_L, "little")
        promotions_l = int.from_bytes(F_PROMOTIONS_L, "little")
        unit_data_l = int.from_bytes(F_UNITDATA_L, "little")
        unit_names_l = int.from_bytes(F_UNITNAMES_L, "little")
        city_data_l = int.from_bytes(F_CITYDATA_L, "little")
        victory_data_l = int.from_bytes(F_VICTORYDATA_L, "little")
        game_options_l = int.from_bytes(F_GAMEOPTIONS_L, "little")

        F_IMPROVEMENTS = f.read(improvements_l)
        F_UNITTYPES = f.read(unit_types_l)
        F_TECHS = f.read(techs_l)
        F_POLICIES = f.read(policies_l)
        F_BUILDINGS = f.read(buildings_l)
        F_PROMOTIONS = f.read(promotions_l)
        F_UNITDATA = f.read(unit_data_l)[4:] if unit_data_l else b''
        F_UNITNAMES = f.read(unit_names_l)[4:] if unit_names_l else b''
        F_CITYDATA = f.read(city_data_l)[4:] if city_data_l else b''
        F_VICTORYDATA = f.read(victory_data_l)
        F_GAMEOPTIONS = f.read(game_options_l)
        improvements = F_IMPROVEMENTS.split(b'\x00')[:-1]
        unit_types = F_UNITTYPES.split(b'\x00')[:-1]
        techs = F_TECHS.split(b'\x00')[:-1]
        policies = F_POLICIES.split(b'\x00')[:-1]
        buildings = F_BUILDINGS.split(b'\x00')[:-1]
        promotions = F_PROMOTIONS.split(b'\x00')[:-1]
        units = []
        unit_l = 48 if version == 11 else 84
        for unit in get_structs_of_size(F_UNITDATA, unit_l):
            if version == 12:
                _, name_index, xp, health, unit_type, owner, facing, status, _, promotion = struct.unpack("2shLLLBBBc64s", unit)
            elif version == 11:
                _, name_index, xp, health, unit_type, owner, facing, status, promotion = struct.unpack("2shLLBBBB32s", unit)
            units.append((name_index, xp, health, unit_type, owner, facing, status, promotion))
        unit_names = []
        unit_name_l = 64
        for unit_name in get_structs_of_size(F_UNITNAMES, unit_name_l):
            unit_names.append(strip_at_first_null(unit_name))
        cities = []
        city_l = 104 if version == 11 else 136
        for city in get_structs_of_size(F_CITYDATA, city_l):
            if version == 12:
                city_name, owner, city_settings, population, health, building_data = struct.unpack("64sBBHL64s", city)
            elif version == 11:
                city_name, owner, city_settings, population, health, building_data = struct.unpack("64sBBHL32s", city)
            cities.append((strip_at_first_null(city_name), owner, city_settings, population, health, building_data))
        victory_data = []
        for victory in F_VICTORYDATA.split(b'\x00')[:-1]:
            victory_data.append((victory[0], victory[1:]))
        game_options = []
        for option in F_GAMEOPTIONS.split(b'\x00')[:-1]:
            game_options.append((option[0], option[1:]))



        ### Holy shit

        self.is_scenario = is_scenario
        self.version = version
        self.map_width = map_width
        self.map_height = map_height
        self.num_players = num_players
        self.world_wrap = world_wrap
        self.random_resources = random_resources
        self.random_goodies = random_goodies
        self.terrains = terrains
        self.features = features
        self.wonders = wonders
        self.resources = resources
        self.mod_data = mod_data
        self.title = title
        self.description = description
        self.world_size = world_size
        self.cells = cells
        self.game_speed = game_speed
        self.max_turns = max_turns
        self.start_year = start_year
        self.num_player_civs = num_player_civs
        self.num_minor_civs = num_minor_civs
        self.num_teams = num_teams
        self.improvements = improvements
        self.unit_types = unit_types
        self.techs = techs
        self.policies = policies
        self.buildings = buildings
        self.promotions = promotions
        self.units = units
        self.unit_names = unit_names
        self.cities = cities
        self.victory_data = victory_data
        self.game_options = game_options


