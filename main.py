
all_maps = False
specific_map = "drake-passage"

print_map_info = True
print_scenario_info = True
print_map = False
output = True

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
                f"{m.units=}\n{m.unit_names=}\n{m.cities=}\n"
                f"{m.victory_data=}\n{m.game_options=}\n"
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
            for y in range(m.map_height):
                for x in range(m.map_width):
                    terrain, _, feature, _, _, elevation, _, wonder, _ = cells[(x, y)]
                    terrain_map += terrain_graphical[terrain]
                    feature_map += feature_graphical[feature]
                    elevation_map += elevation_graphical[elevation] if wonder == -1 else wonder_graphical
                terrain_map += "\n"
                feature_map += "\n"
                elevation_map += "\n"
            print(terrain_map + "-" * m.map_width)
            print(feature_map + "-" * m.map_width)
            print(elevation_map + "-" * m.map_width)

        #print(f"{m.len(cityable) + len(neighbors_of_cityable)}\t{m.file}")

        if not output:
            continue

        mf = m.encode()
        # with open(path + file, "wb") as f:
        #     f.write(mf)
