import struct
debug = False

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
def pad_to_length(byte_string, length):
    return byte_string + b'\x00' * (length - len(byte_string))

# File handler (I think)

class DecodeMap:
    def __init__(self, f):

        ### Read map data

        F_HEAD = f.read(1)
        F_MAPWIDTH = f.read(4)
        F_MAPHEIGHT = f.read(4)
        F_PLAYERS_C = f.read(1)
        F_SETTINGS = f.read(4)
        is_scenario = (F_HEAD[0] & 0b10000000) >> 7
        version = F_HEAD[0] & 0b00001111
        map_width = int.from_bytes(F_MAPWIDTH, "little")
        map_height = int.from_bytes(F_MAPHEIGHT, "little")
        num_players = int.from_bytes(F_PLAYERS_C, "little")
        world_wrap = (F_SETTINGS[0] & 0b00000100) >> 2
        random_resources = (F_SETTINGS[0] & 0b00000010) >> 1
        random_goodies = F_SETTINGS[0] & 0b00000001



        ### Read map arrays

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
        world_size = strip_at_first_null(F_WORLDSIZE)

        F_CELLS = f.read(map_height * map_width * 8)



        ### Read scenario data

        F_GAMESPEED = f.read(64)
        F_X1 = f.read(4)
        F_MAXTURNS = f.read(4)
        F_X2 = f.read(4)
        F_STARTYEAR = f.read(4)
        F_PLAYERCIVS_C = f.read(1)
        F_MINORCIVS_C = f.read(1)
        F_TEAMS_C = f.read(1)
        F_X3 = f.read(1)
        game_speed = strip_at_first_null(F_GAMESPEED)
        max_turns = int.from_bytes(F_MAXTURNS, "little")
        start_year = struct.unpack("l", F_STARTYEAR)[0]
        num_player_civs = int.from_bytes(F_PLAYERCIVS_C, "little")
        num_minor_civs = int.from_bytes(F_MINORCIVS_C, "little")
        num_teams = int.from_bytes(F_TEAMS_C, "little")



        ### Read scenario arrays

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
        F_UNITDATA = f.read(unit_data_l) if unit_data_l else b''
        F_UNITNAMES = f.read(unit_names_l) if unit_names_l else b''
        F_CITYDATA = f.read(city_data_l) if city_data_l else b''
        F_VICTORYDATA = f.read(victory_data_l)
        F_GAMEOPTIONS = f.read(game_options_l)
        improvements = F_IMPROVEMENTS.split(b'\x00')[:-1]
        unit_types = F_UNITTYPES.split(b'\x00')[:-1]
        techs = F_TECHS.split(b'\x00')[:-1]
        policies = F_POLICIES.split(b'\x00')[:-1]
        buildings = F_BUILDINGS.split(b'\x00')[:-1]
        promotions = F_PROMOTIONS.split(b'\x00')[:-1]
        units = []
        for unit in get_structs_of_size(F_UNITDATA[4:], 48 if version == 11 else 84):
            if version == 12:
                _, name_index, xp, health, unit_type, owner, facing, status, _, promotion_data \
                 = struct.unpack("2shLLLBBBc64s", unit)
            elif version == 11:
                _, name_index, xp, health, unit_type, owner, facing, status, promotion_data \
                 = struct.unpack("2shLLBBBB32s", unit)
            units.append((name_index, xp, health, unit_type, owner, facing, status, promotion_data))
        unit_names = []
        for unit_name in get_structs_of_size(F_UNITNAMES[4:], 64):
            unit_names.append(strip_at_first_null(unit_name))
        cities = []
        for city in get_structs_of_size(F_CITYDATA[4:], 104 if version == 11 else 136):
            if version == 12:
                city_name, owner, city_settings, population, health, building_data \
                 = struct.unpack("64sBBHL64s", city)
            elif version == 11:
                city_name, owner, city_settings, population, health, building_data \
                 = struct.unpack("64sBBHL32s", city)
            city_name = strip_at_first_null(city_name)
            cities.append((city_name, owner, city_settings, population, health, building_data))
        victory_data = []
        for victory in F_VICTORYDATA.split(b'\x00')[:-1]:
            victory_data.append((victory[0], victory[1:]))
        game_options = []
        for option in F_GAMEOPTIONS.split(b'\x00')[:-1]:
            game_options.append((option[0], option[1:]))



        ### Read the rest

        # The size of F_PADDING varies in an unknown manner
        teams_l = 64*num_teams
        players_l = 436*num_player_civs+436*num_minor_civs
        cell_improvements_l = 8*map_width*map_height
        rest = f.read()
        padding_l = len(rest)-teams_l-players_l-cell_improvements_l

        F_PADDING = rest[:padding_l]
        F_TEAMS = rest[padding_l:padding_l+teams_l]
        F_PLAYERS = rest[padding_l+teams_l:padding_l+teams_l+players_l]
        F_CELLIMPROVEMENTS = rest[padding_l+teams_l+players_l:]
        teams = []
        for team in get_structs_of_size(F_TEAMS, 64):
            teams.append(strip_at_first_null(team))
        players = []
        for player in get_structs_of_size(F_PLAYERS, 436):
            policy_data, leader_override, name_override, name, color, era, handicap, culture, gold, start_x, start_y, team, is_playable, _ \
             = struct.unpack("32s64s64s64s64s64s64sLLllBB2s", player)
            leader_override = strip_at_first_null(leader_override)
            name_override = strip_at_first_null(name_override)
            name = strip_at_first_null(name)
            color = strip_at_first_null(color)
            era = strip_at_first_null(era)
            handicap = strip_at_first_null(handicap)
            start_position = (start_x, start_y)
            players.append((
                policy_data, leader_override, name_override, name, color, era, handicap, 
                culture, gold, start_position, team, is_playable
            ))


    
        ### Read cells

        cells = {}
        c = 0
        for y in range(map_height):
            for x in range(map_width):
                cell = F_CELLS[c:c+8]
                cell_improvements = F_CELLIMPROVEMENTS[c:c+8]
                c += 8
                terrain, resource, feature, bitmap, elevation, continent, wonder, resource_c = \
                 struct.unpack("BbbBBBbb", cell)
                city, unit, owner, improvement, route, route_owner = \
                 struct.unpack("hhbbbb", cell_improvements)
                river = bitmap & 0b00000111
                X1 = (bitmap & 0b00111000) >> 3
                start_position = (bitmap & 0b11000000) >> 6
                cells[(x, y)] = (
                    terrain, resource, feature, start_position, river, elevation, continent, wonder, resource_c, X1,
                    city, unit, owner, improvement, route, route_owner
                )



        ### Some variables...

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
        self.padding_length = padding_l
        self.teams = teams
        self.players = players
        
  
        self.file = (
            F_HEAD, F_MAPWIDTH, F_MAPHEIGHT, F_PLAYERS_C, F_SETTINGS, F_TERRAINS_L, F_FEATURES_L, F_WONDERS_L, 
            F_RESOURCES_L, F_MODDATA_L, F_TITLE_L, F_DESCRIPTION_L, F_TERRAINS, F_FEATURES, F_WONDERS, F_RESOURCES, 
            F_MODDATA, F_TITLE, F_DESCRIPTION, F_WORLDSIZE_L, F_WORLDSIZE, F_CELLS, F_GAMESPEED, F_X1, F_MAXTURNS, F_X2, 
            F_STARTYEAR, F_PLAYERCIVS_C, F_MINORCIVS_C, F_TEAMS_C, F_X3, F_IMPROVEMENTS_L, F_UNITTYPES_L, F_TECHS_L, 
            F_POLICIES_L, F_BUILDINGS_L, F_PROMOTIONS_L, F_UNITDATA_L, F_UNITNAMES_L, F_CITYDATA_L, 
            F_VICTORYDATA_L, F_GAMEOPTIONS_L, F_IMPROVEMENTS, F_UNITTYPES, F_TECHS, F_POLICIES, F_BUILDINGS, 
            F_PROMOTIONS, F_UNITDATA, F_UNITNAMES, F_CITYDATA, F_VICTORYDATA, F_GAMEOPTIONS, F_PADDING, F_TEAMS,
            F_PLAYERS, F_CELLIMPROVEMENTS
        )





    def encode(self):

        f = []

        ### Encode map data

        f.append((self.is_scenario << 7 | self.version).to_bytes(1, "little"))
        f.append(self.map_width.to_bytes(4, "little"))
        f.append(self.map_height.to_bytes(4, "little"))
        f.append(self.num_players.to_bytes(1, "little"))
        f.append((self.world_wrap << 2 | self.random_resources << 1 | self.random_goodies).to_bytes(4, "little"))



        ### Encode map arrays

        terrains = b''.join([b + b'\x00' for b in self.terrains])
        features = b''.join([b + b'\x00' for b in self.features])
        wonders = b''.join([b + b'\x00' for b in self.wonders])
        resources = b''.join([b + b'\x00' for b in self.resources])
        mod_data = self.mod_data + (b'\x00' if self.mod_data else b'')
        title = self.title + b'\x00'
        description = self.description + b'\x00'
        f.append(len(terrains).to_bytes(4, "little"))
        f.append(len(features).to_bytes(4, "little"))
        f.append(len(wonders).to_bytes(4, "little"))
        f.append(len(resources).to_bytes(4, "little"))
        f.append(len(mod_data).to_bytes(4, "little"))
        f.append(len(title).to_bytes(4, "little"))
        f.append(len(description).to_bytes(4, "little"))
        f.append(terrains)
        f.append(features)
        f.append(wonders)
        f.append(resources)
        f.append(mod_data)
        f.append(title)
        f.append(description)

        f.append(b'\x40\x00\x00\x00')
        f.append(pad_to_length(self.world_size, 64))

        cells = b''
        for y in range(self.map_height):
            for x in range(self.map_width):
                terrain, resource, feature, start_position, river, elevation, continent, wonder, resource_c, X1, *_ = self.cells[(x, y)]
                bitmap = start_position << 6 | X1 << 3 | river
                print(X1)
                cells += struct.pack("BbbBBBbb", 
                 terrain, resource, feature, bitmap, elevation, continent, wonder, resource_c)
        f.append(cells)



        ### Encode scenario data

        f.append(pad_to_length(self.game_speed, 64))
        f.append(b'\x00' * 4)
        f.append(self.max_turns.to_bytes(4, "little"))
        f.append(b'\x00' * 4)
        f.append(struct.pack("l", self.start_year))
        f.append(self.num_player_civs.to_bytes(1, "little"))
        f.append(self.num_minor_civs.to_bytes(1, "little"))
        f.append(self.num_teams.to_bytes(1, "little"))
        f.append(b'\x00')



        ### Encode scenario arrays

        improvements = b''.join([b + b'\x00' for b in self.improvements])
        unit_types = b''.join([b + b'\x00' for b in self.unit_types])
        techs = b''.join([b + b'\x00' for b in self.techs])
        policies = b''.join([b + b'\x00' for b in self.policies])
        buildings = b''.join([b + b'\x00' for b in self.buildings])
        promotions = b''.join([b + b'\x00' for b in self.promotions])
        units = b'unit' if self.units else b''
        for name_index, xp, health, unit_type, owner, facing, status, promotion_data in self.units:
            if self.version == 12:
                units += struct.pack("2shLLLBBBc64s", 
                 b'\xff\xff', name_index, xp, health, unit_type, owner, facing, status, b'\x00', promotion_data)
            elif self.version == 11:
                units += struct.pack("2shLLBBBB32s", 
                 b'\xff\xff', name_index, xp, health, unit_type, owner, facing, status, promotion_data)
        unit_names = b'name' if self.unit_names else b''
        for unit_name in self.unit_names:
            unit_names += pad_to_length(unit_name, 64)
        cities = b'city' if self.cities else b''
        for city_name, owner, city_settings, population, health, building_data in self.cities:
            city_name = pad_to_length(city_name, 64)
            if self.version == 12:
                cities += struct.pack("64sBBHL64s", 
                 city_name, owner, city_settings, population, health, building_data)
            elif self.version == 11:
                cities += struct.pack("64sBBHL32s", 
                 city_name, owner, city_settings, population, health, building_data)
        victory_data = b''
        for data, victory_type in self.victory_data:
            victory_data += data.to_bytes(1, "little") + victory_type + b'\x00'
        game_options = b''
        for data, option in self.game_options:
            game_options += data.to_bytes(1, "little") + option + b'\x00'
        f.append(len(improvements).to_bytes(4, "little"))
        f.append(len(unit_types).to_bytes(4, "little"))
        f.append(len(techs).to_bytes(4, "little"))
        f.append(len(policies).to_bytes(4, "little"))
        f.append(len(buildings).to_bytes(4, "little"))
        f.append(len(promotions).to_bytes(4, "little"))
        f.append(len(units).to_bytes(4, "little"))
        f.append(len(unit_names).to_bytes(4, "little"))
        f.append(len(cities).to_bytes(4, "little"))
        f.append(len(victory_data).to_bytes(4, "little"))
        f.append(len(game_options).to_bytes(4, "little"))
        f.append(improvements)
        f.append(unit_types)
        f.append(techs)
        f.append(policies)
        f.append(buildings)
        f.append(promotions)
        f.append(units)
        f.append(unit_names)
        f.append(cities)
        f.append(victory_data)
        f.append(game_options)

        
        
        ### Encode the rest

        players = b''
        for policy_data, leader_override, name_override, name, color, era, handicap, culture, gold, start_position, team, is_playable in self.players:
            leader_override = pad_to_length(leader_override, 64)
            name_override = pad_to_length(name_override, 64)
            name = pad_to_length(name, 64)
            color = pad_to_length(color, 64)
            era = pad_to_length(era, 64)
            handicap = pad_to_length(handicap, 64)
            start_x, start_y = start_position
            players += struct.pack("32s64s64s64s64s64s64sLLllBB2s", 
             policy_data, leader_override, name_override, name, color, era, handicap, culture, gold, start_x, start_y, team, is_playable, b'\x00\x00')
        cell_improvements = b''
        for y in range(self.map_height):
            for x in range(self.map_width):
                _, _, _, _, _, _, _, _, _, _, city, unit, owner, improvement, route, route_owner = self.cells[(x, y)]
                cell_improvements += struct.pack("hhbbbb", 
                 city, unit, owner, improvement, route, route_owner)
        f.append(b'\x00' * self.padding_length)
        f.append(b''.join([pad_to_length(team, 64) for team in self.teams]))
        f.append(players)
        f.append(cell_improvements)



        names = (
            "F_HEAD", "F_MAPWIDTH", "F_MAPHEIGHT", "F_PLAYERS_C", "F_SETTINGS", "F_TERRAINS_L", "F_FEATURES_L", 
            "F_WONDERS_L", "F_RESOURCES_L", "F_MODDATA_L", "F_TITLE_L", "F_DESCRIPTION_L", "F_TERRAINS", "F_FEATURES", 
            "F_WONDERS", "F_RESOURCES", "F_MODDATA", "F_TITLE", "F_DESCRIPTION", "F_WORLDSIZE_L", "F_WORLDSIZE", "F_CELLS", 
            "F_GAMESPEED", "F_X1", "F_MAXTURNS", "F_X2", "F_STARTYEAR", "F_PLAYERCIVS_C", "F_MINORCIVS_C", "F_TEAMS_C", 
            "F_X3", "F_IMPROVEMENTS_L", "F_UNITTYPES_L", "F_TECHS_L", "F_POLICIES_L", "F_BUILDINGS_L", "F_PROMOTIONS_L", 
            "F_UNITDATA_L", "F_UNITNAMES_L", "F_CITYDATA_L", "F_VICTORYDATA_L", "F_GAMEOPTIONS_L", "F_IMPROVEMENTS", 
            "F_UNITTYPES", "F_TECHS", "F_POLICIES", "F_BUILDINGS", "F_PROMOTIONS", "F_UNITDATA", "F_UNITNAMES", 
            "F_CITYDATA", "F_VICTORYDATA", "F_GAMEOPTIONS", "F_PADDING", "F_TEAMS", "F_PLAYERS", "F_CELLIMPROVEMENTS"
        )

        if debug:
            for new, old, name in zip(f, self.file, names):
                bad = False
                if new != old:
                    bad = True
                    print("Difference in", name)
                    for i, (newc, oldc) in enumerate(zip(new, old)):
                        if newc != oldc:
                            break
                    print("Old:", old[max(0,i-50):i], old[i:i+50])
                    print("New:", new[max(0,i-50):i], new[i:i+50])
                if bad:
                    quit()

        return b''.join(f)