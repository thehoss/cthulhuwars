import networkx as nx

class map:
    # available maps

    # Earth, 3 player, Eastern Hemisphere
    earth3PEH = {
        'Africa': ['South Atlantic', 'North Atlantic', 'Indian Ocean', 'Asia'],
        'Europe': ['Asia', 'Arctic Ocean', 'North Atlantic'],
        'Asia': ['North Pacific', 'Arctic Ocean', 'Europe', 'Africa', 'Indian Ocean', 'North Atlantic'],
        'Antarctica': ['South Atlantic', 'Indian Ocean'],

        'Arctic Ocean': ['Europe', 'Asia', 'North Atlantic'],
        'Indian Ocean': ['South Atlantic', 'Antarctica', 'Africa', 'Asia'],
        'North Atlantic': ['South Atlantic', 'Europe', 'Africa'],
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
        'North Atlantic': ['North Pacific', 'South Atlantic', 'North America', 'South America'],
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
        'North Atlantic': ['Artic Ocean', 'South Atlantic', 'West Africa', 'Arabia', 'Europe', 'Scandinavia'],
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
        'Indian Ocean': ['South Atlantic', 'Antarctica', 'North Pacific', 'East Africa', 'South Asia', 'Arabia',
                         'Australia', 'South Pacific', 'New Zealand'],
        'North Atlantic': ['North Pacific', 'South Atlantic', 'North America East', 'Central America',
                           'South America East', 'Europe'],
        'South Atlantic': ['North Atlantic', 'Antarctica', 'South America East', 'South America West', 'South Pacific']
    }

    # map_names = ['celaeno', 'dreamlands', 'earth', 'primeval earth', 'yuggoth']

    def __init__(self, num_players=3, map_name='earth3P'):
        self.num_players = num_players
        self.map_name = map_name

        # we allow number of players and n-player map configurations to be in disagreement for experimentation
        east_ = {}
        west_ = {}

        if self.map_name == 'earth3P':
            east_ = self.earth3PEH
            west_ = self.earth3PWH

        if self.map_name == 'earth5P':
            east_ = self.earth5PEH
            west_ = self.earth5PWH

        if self.map_name == 'earth2Pa' or self.map_name == 'earth4Pa':
            east_ = self.earth3PEH
            west_ = self.earth5PWH

        if self.map_name == 'earth2Pb' or self.map_name == 'earth4Pb':
            east_ = self.earth5PEH
            west_ = self.earth3PWH

        # construct node graphs from dictionary of lists, construct combined node graph with compose()
        self.east = nx.from_dict_of_lists(east_)
        self.west = nx.from_dict_of_lists(west_)
        self.map  = nx.compose(self.east, self.west)
