
all_maps = False
specific_map = "Sven's Europe v1.5 (Standard)"

print_map_info = True
print_scenario_info = True
print_map = False
output = False

import os, struct, random
path = "C://Users//isakh//Documents//My Games//Sid Meier's Civilization 5//Maps//"
c = 0
def byte_groups(byte, groups):
    parts = []
    for n in reversed(groups):
        parts.append(byte & 2**n - 1)
        byte >>= n
    return parts[::-1]
def get_neighbors(coords):
    x, y = coords
    if y % 2: # odd
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1), (x+1, y+1), (x+1, y-1)]
    else: # even
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1), (x-1, y+1), (x-1, y-1)]
    return [n for n in neighbors if is_valid(n)]
def is_valid(coords):
    x, y = coords
    return x >= 0 and y >= 0 and x < map_width and y < map_height
for file in os.listdir(path):
    if file[-8:] != ".Civ5Map":
        continue
    if not all_maps and file[:-8] != specific_map:
        continue
    with open(path + file, "rb") as f:

        ### Read map data

        F_HEAD = f.read(1)
        F_MAPWIDTH = f.read(4)
        F_MAPHEIGHT = f.read(4)
        F_PLAYERS_C = f.read(1)
        F_SETTINGS = f.read(4)
        is_scenario, _, version = byte_groups(F_HEAD[0], [1, 3, 4])
        map_width = int.from_bytes(F_MAPWIDTH, "little")
        map_height = int.from_bytes(F_MAPHEIGHT, "little")
        num_players = int.from_bytes(F_PLAYERS_C, "little")
        _, world_wrap, random_resources, random_goodies = byte_groups(F_SETTINGS[0], [5, 1, 1, 1])

        F_TERRAINS_L = f.read(4)
        F_FEATURES_L = f.read(4)
        F_WONDERS_L = f.read(4)
        F_RESOURCES_L = f.read(4)
        F_MODDATA_L = f.read(4)
        F_MAPNAME_L = f.read(4)
        F_MAPDESC_L = f.read(4)
        terrains_l = int.from_bytes(F_TERRAINS_L, "little")
        features_l = int.from_bytes(F_FEATURES_L, "little")
        wonders_l = int.from_bytes(F_WONDERS_L, "little")
        resources_l = int.from_bytes(F_RESOURCES_L, "little")
        mod_data_l = int.from_bytes(F_MODDATA_L, "little")
        title_l = int.from_bytes(F_MAPNAME_L, "little")
        description_l = int.from_bytes(F_MAPDESC_L, "little")

        F_TERRAINS = f.read(terrains_l)
        F_FEATURES = f.read(features_l)
        F_WONDERS = f.read(wonders_l)
        F_RESOURCES = f.read(resources_l)
        F_MODDATA = f.read(mod_data_l)
        F_MAPNAME = f.read(title_l)
        F_MAPDESC = f.read(description_l)
        terrains = F_TERRAINS.split(b'\x00')[:-1]
        features = F_FEATURES.split(b'\x00')[:-1]
        wonders = F_WONDERS.split(b'\x00')[:-1]
        resources = F_RESOURCES.split(b'\x00')[:-1]
        mod_data = F_MODDATA[:-1]
        title = F_MAPNAME[:-1]
        description = F_MAPDESC[:-1]

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
        F_X1 = f.read(4)
        F_MAXTURNS = f.read(4)
        F_X2 = f.read(4)
        F_STARTYEAR = f.read(4)
        F_PLAYERCIVS_C = f.read(1)
        F_MINORCIVS_C = f.read(1)
        F_TEAMS_C = f.read(1)
        F_X3 = f.read(1)
        game_speed = F_GAMESPEED.strip(b'\x00')
        max_turns = int.from_bytes(F_MAXTURNS, "little")
        start_year = struct.unpack("l", F_STARTYEAR)[0]
        num_player_civs = int.from_bytes(F_PLAYERCIVS_C, "little")
        num_minor_civs = int.from_bytes(F_MINORCIVS_C, "little")
        num_teams = int.from_bytes(F_TEAMS_C, "little")

        F_IMPROVEMENTS_L = f.read(4)
        F_UNITS_L = f.read(4)
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
        units_l = int.from_bytes(F_UNITS_L, "little")
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
        F_UNITS = f.read(units_l)
        F_TECHS = f.read(techs_l)
        F_POLICIES = f.read(policies_l)
        F_BUILDINGS = f.read(buildings_l)
        F_PROMOTIONS = f.read(promotions_l)
        F_X4 = f.read(4) if unit_data_l else b''
        F_UNITDATA = f.read(unit_data_l)
        F_UNITNAMES = f.read(unit_names_l)
        F_CITYDATA = f.read(city_data_l)
        F_VICTORYDATA = f.read(victory_data_l)
        F_GAMEOPTIONS = f.read(game_options_l)
        improvements = F_IMPROVEMENTS.split(b'\x00')[:-1]
        units = F_UNITS.split(b'\x00')[:-1]
        techs = F_TECHS.split(b'\x00')[:-1]
        policies = F_POLICIES.split(b'\x00')[:-1]
        buildings = F_BUILDINGS.split(b'\x00')[:-1]
        promotions = F_PROMOTIONS.split(b'\x00')[:-1]
        unit_data = F_UNITDATA
        unit_names = F_UNITNAMES
        city_data = F_CITYDATA
        victory_data = F_VICTORYDATA
        game_options = F_GAMEOPTIONS.split(b'\x00')[:-1]



        
        if print_map_info:
            print(
                f"{is_scenario=}\n{version=}\n{map_width=}\n{map_height=}\n{num_players=}\n{world_wrap=}\n{random_resources=}\n{random_goodies=}\n"
                f"{terrains=}\n{features=}\n{wonders=}\n{resources=}\n{mod_data=}\n{title=}\n{description=}\n{world_size=}\n"
                f"first cell={cells[(0, 0)]}\nlast cell={cells[(map_width-1, map_height-1)]}"
            )
        if print_scenario_info:
            print(
                f"{game_speed=}\n{max_turns=}\n{start_year=}\n{num_player_civs=}\n{num_minor_civs=}\n{num_teams=}\n"
                f"{improvements=}\n{units=}\n{techs=}\n{policies=}\n{buildings=}\n{promotions=}\n{unit_data=}\n{unit_names=}\n{city_data=}\n"
                f"{victory_data=}\n{game_options=}\n"
            )

        def place_coast(filter, chance_for_ocean):
            new_cells = {}
            for coords, cell in cells.items():
                terrain, *other = cell
                if terrain not in filter:
                    new_cells[coords] = cell
                    continue
                for n in get_neighbors(coords):
                    if cells[n][0] not in filter:
                        break
                else:
                    new_cells[coords] = (6, *other)
                    continue
                if random.random() < chance_for_ocean:
                    new_cells[coords] = (6, *other)
                    continue
                new_cells[coords] = (5, *other)
            return new_cells
        cells = place_coast([5, 6], 0)
        #cells = place_coast([6], 0)
        # cells = place_coast([6], 0.5)
        # cells = place_coast([6], 0.75)

        cityable = set()
        for coords, cell in cells.items():
            terrain, _, feature, _, elevation, *_ = cell
            if terrain in [2, 4] and elevation == 0: # desert, snow, flat
                continue
            if terrain in [5, 6]: # coast, ocean
                continue
            if feature in [0, 6]: # ice, fallout
                continue
            if elevation == 2: # mountain
                continue
            cityable.add(coords)
        neighbors_of_cityable = set()
        for coords, cell in cells.items():
            if coords in cityable:
                continue
            terrain, _, feature, _, elevation, *_ = cell
            if terrain in [5, 6]: # coast, ocean
                continue
            if feature in [0, 6]: # ice, fallout
                continue
            if elevation == 2: # mountain
                continue
            for neighbor in get_neighbors(coords):
                if neighbor in cityable or cells[neighbor][0] == 5 or cells[neighbor][6] != -1: # cityable, coast, wonder
                    break
            else:
                continue
            neighbors_of_cityable.add(coords)

        if print_map:
            # grassland, plains, desert, tundra, snow, coast, ocean
            terrain_graphical = "#%:t,~ "
            # ice, jungle, marsh, oasis, flood plains, forest, fallout, atoll, none
            feature_graphical = "IW@¤&^Xö "
            # flat, hill, mountain
            elevation_graphical = " .A"
            wonder_graphical = "*"
            terrain_map = ""
            feature_map = ""
            elevation_map = ""
            for y in range(map_height):
                for x in range(map_width):
                    terrain, _, feature, _, elevation, _, wonder, _ = cells[(x, y)]
                    terrain_map += terrain_graphical[terrain]
                    feature_map += feature_graphical[feature]
                    elevation_map += elevation_graphical[elevation] if wonder == -1 else wonder_graphical
                terrain_map += "\n"
                feature_map += "\n"
                elevation_map += "\n"
            print(terrain_map + "-" * map_width)
            print(feature_map + "-" * map_width)
            print(elevation_map + "-" * map_width)

        print(f"{len(cityable) + len(neighbors_of_cityable)}\t{file}")

        if not output:
            continue

        with open(path + file, "wb") as f:
            f.write(F_HEAD)
