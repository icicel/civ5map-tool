
all_maps = False
specific_map = "drake-passage"

print_map_info = True
print_scenario_info = True
print_map = False
export_map = False

import os, random, decodemap
path = "C://Users//isakh//Documents//My Games//Sid Meier's Civilization 5//Maps//"
c = 0

for file in os.listdir(path):
    if file[-8:] != ".Civ5Map":
        continue
    if not all_maps and file[:-8] != specific_map:
        continue
    with open(path + file, "rb") as f:

        m = decodemap.DecodeMap(f)
        
        if print_map_info:
            print(
                f"{m.is_scenario=}\n{m.version=}\n{m.map_width=}\n{m.map_height=}\n{m.num_players=}\n"
                f"{m.world_wrap=}\n{m.random_resources=}\n{m.random_goodies=}\n"
                f"{m.terrains=}\n{m.features=}\n{m.wonders=}\n{m.resources=}\n"
                f"{m.mod_data=}\n{m.title=}\n{m.description=}\n{m.world_size=}\n"
                f"first cell={m.cells[(0, 0)]}\nlast cell={m.cells[(m.map_width-1, m.map_height-1)]}"
            )
        if print_scenario_info:
            print(
                f"{m.game_speed=}\n{m.max_turns=}\n{m.start_year=}\n"
                f"{m.num_player_civs=}\n{m.num_minor_civs=}\n{m.num_teams=}\n"
                f"{m.improvements=}\n{m.unit_types=}\n{m.techs=}\n{m.policies=}\n{m.buildings=}\n{m.promotions=}\n"
                f"{m.units=}\n{m.unit_names=}\n{m.cities=}\n{m.victory_data=}\n{m.game_options=}\n"
                f"{m.teams=}\n{m.players=}\n{m.padding_length=}"
            )

            
        def get_neighbors(coords):
            x, y = coords
            if y % 2: # odd
                neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1), (x+1, y+1), (x+1, y-1)]
            else: # even
                neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1), (x-1, y+1), (x-1, y-1)]
            return [n for n in neighbors if is_valid(n)]
        def is_valid(coords):
            x, y = coords
            return x >= 0 and y >= 0 and x < m.map_width and y < m.map_height

        def place_coast(cells, filter, chance_for_ocean):
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
        cells = m.cells
        # cells = place_coast(cells, [5, 6], 0)
        # cells = place_coast(cells, [6], 0)
        # cells = place_coast(cells, [6], 0.5)
        # cells = place_coast(cells, [6], 0.75)

        cityable = set()
        for coords, cell in cells.items():
            terrain, _, feature, _, _, elevation, *_ = cell
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
            terrain, _, feature, _, _, elevation, *_ = cell
            if terrain in [5, 6]: # coast, ocean
                continue
            if feature in [0, 6]: # ice, fallout
                continue
            if elevation == 2: # mountain
                continue
            for neighbor in get_neighbors(coords):
                if (neighbor in cityable or 
                (cells[neighbor][0] == 5 and cells[neighbor][2] not in [0, 6]) or 
                cells[neighbor][6] != -1): # cityable, coast, wonder
                    break
            else:
                continue
            neighbors_of_cityable.add(coords)

        if print_map:
            # grassland, plains, desert, tundra, snow, coast, ocean
            terrain_graphical = "#%:t,~."
            # ice, jungle, marsh, oasis, flood plains, forest, fallout, atoll, none
            feature_graphical = "Iw@¤&vXö "
            # flat, hill, mountain
            elevation_graphical = " .M"
            elevation_bg = [None, None, "85;85;85"]
            # wonder
            wonder_graphical = "$"
            wonder_bg = "255;0;255"
            feature_map = ""
            scenario_map = ""
            cityable_map = ""
            for y in range(m.map_height-1, -1, -1):
                for x in range(m.map_width):
                    terrain, resource, feature, start_position, river, elevation, continent, wonder, _, _,\
                    city, unit, owner, improvement, route, route_owner = cells[(x, y)]
                    if wonder != -1:
                        feature_map += wonder_graphical
                    elif elevation == 2:
                        feature_map += elevation_graphical[elevation]
                    elif feature != -1:
                        feature_map += feature_graphical[feature]
                    else:
                        feature_map += terrain_graphical[terrain]
                    if city != -1:
                        scenario_map += "C"
                    elif unit != -1:
                        scenario_map += "U"
                    elif improvement != -1:
                        scenario_map += "$"
                    elif route != -1:
                        scenario_map += "/"
                    elif resource != -1:
                        scenario_map += "¤"
                    elif start_position:
                        scenario_map += "O"
                    elif terrain in [5, 6]:
                        scenario_map += "~"
                    else:
                        scenario_map += " "
                    if (x, y) in cityable:
                        cityable_map += "#"
                    else:
                        cityable_map += " "
                feature_map += "\n"
                scenario_map += "\n"
                cityable_map += "\n"
            print(feature_map + "-" * m.map_width)
            print(scenario_map + "-" * m.map_width)
            print(cityable_map + "-" * m.map_width)

        print(f"{len(cityable) + len(neighbors_of_cityable)}\t{file}")

        if not export_map:
            continue

        mf = m.encode()
        with open(path + file + ".Civ5Map", "wb") as f:
            f.write(mf)
