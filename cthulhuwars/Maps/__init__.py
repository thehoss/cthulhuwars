from .core import Map

if __name__ == "__test__":
    M = Map(4, 'earth4Pa')
    M.zone_by_name('Africa')
    M.find_neighbors('Africa')
    M.show_map()