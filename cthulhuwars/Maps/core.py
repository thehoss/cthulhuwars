# coding=utf-8
from __future__ import print_function

"""
cthulhuWars
Map Class
Builds a network of map zones

TODO:
Replace string nodes with a zone class (TBD)
Add traversal methods
Flesh out graph visualization to represent class data
"""

import networkx as nx
import matplotlib.pylab as P
import matplotlib.image as mpimg
import numpy as np
from cthulhuwars.Zone import Zone
from cthulhuwars import arnoldRender

import os


class Map:
    # available maps
    # Earth, 3 player, Eastern Hemisphere
    earth3PEH = {
        'Africa': ['South Atlantic', 'North Atlantic', 'Indian Ocean', 'Asia'],
        'Europe': ['Asia', 'Arctic Ocean', 'North Atlantic'],
        'Asia': ['North Pacific', 'Arctic Ocean', 'Europe', 'Africa', 'Indian Ocean', 'North Atlantic'],
        'Antarctica': ['South Atlantic', 'Indian Ocean'],

        'Arctic Ocean': ['Europe', 'Asia', 'North Atlantic'],
        'Indian Ocean': ['South Atlantic', 'Antarctica', 'Africa', 'Asia'],
        'North Atlantic': ['Arctic Ocean', 'South Atlantic', 'Europe', 'Africa'],
        'South Atlantic': ['North Atlantic', 'Antarctica', 'Indian Ocean', 'Africa'],
        'North Pacific': ['Asia', 'Arctic Ocean', 'Indian Ocean'],
    }

    # Earth, 3 player, Western Hemisphere
    earth3PWH = {
        'Europe': ['North Atlantic'],
        'North America': ['North Pacific', 'North Atlantic', 'Arctic Ocean', 'South America'],
        'South America': ['North America', 'North Pacific', 'South Pacific', 'North Atlantic', 'South Atlantic'],
        'Australia': ['Indian Ocean', 'South Pacific'],
        'Antarctica': ['South Atlantic', 'South Pacific'],

        'Arctic Ocean': ['North America', 'North Atlantic', 'North Pacific'],
        'Indian Ocean': ['South Atlantic', 'Antarctica', 'North Pacific', 'Australia', 'South Pacific'],
        'North Atlantic': ['Arctic Ocean', 'North Pacific', 'South Atlantic', 'North America', 'South America'],
        'South Atlantic': ['North Atlantic', 'Antarctica', 'Indian Ocean', 'South America', 'South Pacific'],
        'North Pacific': ['North America', 'Arctic Ocean', 'Indian Ocean', 'South America', 'South Pacific'],
        'South Pacific': ['North Pacific', 'Australia', 'South America', 'Antarctica', 'South Atlantic'],
    }

    # Earth, 5 player, Eastern Hemisphere
    earth5PEH = {
        'East Africa': ['South Atlantic', 'West Africa', 'Arabia', 'Indian Ocean'],
        'West Africa': ['North Atlantic', 'South Atlantic', 'East Africa', 'Arabia'],
        'Europe': ['Arabia', 'North Asia', 'North Atlantic', 'Scandinavia'],
        'Scandinavia': ['Arctic Ocean', 'North Atlantic', 'North Asia', 'Europe'],
        'Arabia': ['Europe', 'North Asia', 'South Asia', 'Indian Ocean', 'East Africa', 'West Africa'],
        'North Asia': ['North Pacific', 'Arctic Ocean', 'Europe', 'Scandinavia', 'Arabia', 'South Asia'],
        'South Asia': ['North Pacific', 'Indian Ocean', 'Arabia', 'North Asia'],
        'Antarctica': ['South Atlantic', 'Indian Ocean'],

        'Arctic Ocean': ['Scandinavia', 'North Asia', 'North Atlantic', 'North Pacific'],
        'North Pacific': ['Arctic Ocean', 'Indian Ocean', 'North Asia', 'South Asia'],
        'Indian Ocean': ['South Atlantic', 'Antarctica', 'North Pacific', 'East Africa', 'South Asia', 'Arabia'],
        'North Atlantic': ['Arctic Ocean', 'South Atlantic', 'West Africa', 'Arabia', 'Europe', 'Scandinavia'],
        'South Atlantic': ['North Atlantic', 'Antarctica', 'Indian Ocean', 'East Africa', 'West Africa']
    }

    # Earth, 5 player, Western Hemisphere
    earth5PWH = {
        'Europe':  ['North Atlantic'],
        'North America East': ['North Atlantic', 'Arctic Ocean', 'North America West'],
        'North America West': ['North America East', 'Central America', 'North Atlantic', 'North Pacific',
                               'Arctic Ocean'],
        'Central America': ['North America West', 'South America West', 'South America East', 'North Atlantic',
                            'North Pacific'],
        'South America East': ['South America West', 'Central America', 'North Atlantic', 'South Atlantic'],
        'South America West': ['Central America', 'South America East', 'South Pacific', 'North Pacific', ],
        'Australia': ['Indian Ocean', 'New Zealand'],
        'New Zealand': ['Australia', 'Indian Ocean', 'South Pacific'],
        'Antarctica': ['South Atlantic', 'South Pacific'],

        'Arctic Ocean': ['North America East', 'North America West', 'North Atlantic', 'North Pacific'],
        'North Pacific': ['Central America', 'North America West', 'Arctic Ocean', 'Indian Ocean',
                          'South America West', 'South Pacific'],
        'South Pacific': ['North Pacific', 'New Zealand', 'South America West', 'Antarctica', 'South Atlantic'],
        'Indian Ocean': ['South Atlantic', 'Antarctica', 'North Pacific', 'Australia', 'South Pacific', 'New Zealand'],
        'North Atlantic': ['North Pacific', 'South Atlantic', 'North America East', 'Central America',
                           'South America East', 'Europe', 'Arctic Ocean'],
        'South Atlantic': ['North Atlantic', 'Antarctica', 'South America East', 'South America West', 'South Pacific']
    }

    earth_oceans = ['Arctic Ocean', 'North Atlantic', 'South Atlantic', 'Indian Ocean', 'North Pacific',
                    'South Pacific']

    earth_gate_positions = {'Arctic Ocean': [0.03, 0.9], 'North Atlantic': [-0.23, 0.57],
                            'South Atlantic': [-0.05, 0.24], 'Indian Ocean': [0.69, 0.21],
                            'North Pacific':[-0.9, 0.54], 'South Pacific': [-0.53, 0.09],
                            'North America': [-0.58, 0.7], 'South America': [-0.33, 0.28],
                            'North America West': [-0.63, 0.75], 'North America East': [-0.36, 0.72],
                            'South America East': [-0.24, 0.31], 'South America West': [-0.4, 0.29],
                            'Central America': [-0.66, 0.55], 'Australia': [-0.9, 0.2],
                            'New Zealand': [-0.69, 0.25], 'Antarctica': [-0.025, 0.06],
                            'Africa': [0.21, 0.47], 'East Africa': [0.43, 0.25],
                            'West Africa': [0.21, 0.47], 'Europe': [0.37, 0.71],
                            'Scandinavia': [0.38, 0.87], 'Arabia': [0.56, 0.47], 'Asia': [0.68, 0.75],
                            'North Asia': [0.75, 0.79], 'South Asia': [0.85, 0.55]
                            }


    earth_map_configs = {'earth3P': ['earth3PWH', 'earth3PEH'], 'earth2Pa': ['earth5PWH', 'earth3PEH'],
                         'earth4Pa': ['earth5PWH', 'earth3PEH'], 'earth2Pb': ['earth3PWH', 'earth5PEH'],
                         'earth4Pb': ['earth3PWH', 'earth5PEH'], 'earth5P': ['earth5PWH', 'earth5PEH']
                         }

    # map_names = ['celaeno', 'dreamlands', 'earth', 'primeval earth', 'yuggoth']

    def __init__(self, num_players=3, map_name='earth3P'):
        self.num_players = num_players
        self.map_name = map_name

        # we allow number of players and n-player map configurations to be in disagreement for experimentation
        west_map = {}
        east_map = {}

        if self.map_name == 'earth3P':
            west_map = self.earth3PWH
            east_map = self.earth3PEH

        if self.map_name == 'earth2Pa' or self.map_name == 'earth4Pa':
            west_map = self.earth5PWH
            east_map = self.earth3PEH

        if self.map_name == 'earth2Pb' or self.map_name == 'earth4Pb':
            west_map = self.earth3PWH
            east_map = self.earth5PEH

        if self.map_name == 'earth5P':
            west_map = self.earth5PWH
            east_map = self.earth5PEH

        # construct node graphs from dictionary of lists
        self._west_map = nx.from_dict_of_lists(west_map)
        self._east_map = nx.from_dict_of_lists(east_map)
        # construct combined node graph with compose()
        self.map = nx.compose(self._east_map, self._west_map)
        self.map.graph['name'] = self.map_name

        # relable nodes with zone objects
        node_list = self.map.nodes()

        for node_name in node_list:
            is_ocean = False
            if node_name in self.earth_oceans:
                is_ocean = True
            self.map.node[node_name]['zone'] = Zone(node_name, is_ocean)
            self.map.node[node_name]['pos'] = [0.5, 0.5]
        # ^ map.nodes(data=True) will show the attributes of node label 'blah'
        '''
        # optionally, swap labeled nodes with name-tagged zone objects
        # warning: you might have to retype this to experiment
        # 'cos I may have drunkenly added some weird characters
        node_list = G.nodes()
        zone_list = []

        for node_name in node_list: 
            is_ocean = False 
            if node_name in self.earth_oceans: 
                is_ocean = True 
            zone_list.append(Zone(node_name, is_ocean))  
        mapping = dict(zip(node_list, zone_list))
         self.map = nx.relabel_nodes(G, mapping)
        '''
    def zone_by_name(self, zone):
        return self.map.node[zone]['zone']

    def find_neighbors(self, zone, radius=1):
        if radius == 1:
            return self.map.neighbors(zone)
        if radius == 2:
            ego_graph = nx.ego_graph(self.map, zone, 2, center=False, undirected=True)
            return ego_graph.nodes()

    def show_map(self, image_prefix='image'):
        basepath = '../../tex'
        imagepath = '../../img'
        file_format = '.png'

        print(self.map_name)
        west_map_filename = self.earth_map_configs[self.map_name][0] + file_format
        img_west_path = os.path.join(basepath, west_map_filename)
        print(img_west_path)
        img_west = mpimg.imread(img_west_path)
        print(img_west.shape)

        east_map_filename = self.earth_map_configs[self.map_name][1] + file_format
        img_east_path = os.path.join(basepath, east_map_filename)
        print(img_east_path)
        img_east = mpimg.imread(img_east_path)
        print(img_east.shape)


        img = np.concatenate((img_west, img_east), axis=1)

        P.imshow(img, extent=[-1, 1, 0, 1])

        #pos = nx.spring_layout(self.map, iterations=100)

        pos = {}
        cols = []
        for node in self.map.node:
            cols.append(self.map.node[node]['zone'].compute_color())
            pos[node] = self.earth_gate_positions[node]

        nx.draw(self.map, pos, font_size=12, with_labels=False, node_color=cols)
        #for p in pos:  # raise text positions
        #    pos[p][1] += 0.07
        #nx.draw_networkx_labels(self.map, pos)
        img_name = imagepath+'/'+image_prefix+file_format
        P.savefig(img_name)
        #P.show()

    def render_map(self, image_prefix='image'):
        ar = arnoldRender.ArnoldRender(image_prefix)
        ar.do_render(1, self.map)

    def move_unit(self, unit, fromeZone, toZone):

        pass
