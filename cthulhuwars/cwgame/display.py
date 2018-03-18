import os
import sys
import pygame
import math as m
from .color import NodeColor, NodeColorINT, TextColor
from .unit import Unit, UnitType, UnitState, Faction, Cultist
from .zone import Zone, GateState

class Display(object):
    def __init__(self):
        cwd = os.path.dirname(os.path.abspath(__file__))        
        self.font = None
        self.screen = None
        self.display = True
        self.img_gate = None
        self.img_map_east = None
        self.img_map_west = None
        self.nx_map = None
        self.basepath = os.path.join(cwd, 'tex')
        self.fontpath = os.path.join(cwd, 'fonts')
        self.imagepath = cwd
        self.file_format = '.png'
        self.width, self.height = 2000, 1000
        self.unit_size = 10
        self.unit_spacing = 25
        self.text_size = 19
        self.gate_size = 40


    def init(self, east_map_filename, west_map_filename, map):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font( os.path.join(self.fontpath, 'abaddon.ttf'), self.text_size)
        #self.font = pygame.font.Font('display.ttf', 16)
        #self.font = pygame.font.SysFont(None, 18)
        # initialize the screen
        self.screen = pygame.display.set_mode((self.width, self.height))
        # self.clock = pygame.time.Clock()

        self.img_map_east = pygame.image.load( os.path.join(self.basepath, east_map_filename + self.file_format))
        self.img_map_west = pygame.image.load( os.path.join(self.basepath, west_map_filename + self.file_format))

        west = pygame.transform.smoothscale(self.img_map_west, (int(m.floor(self.width / 2)), int(self.height)))
        east = pygame.transform.smoothscale(self.img_map_east, (int(m.floor(self.width / 2)), int(self.height)))
        self.img_map_east = east.convert()
        self.img_map_west = west.convert()

        self.img_gate = pygame.image.load(os.path.join(self.basepath, 'gate.png'))
        self.img_gate = pygame.transform.smoothscale(self.img_gate, (self.gate_size, self.gate_size))
        self.img_gate = self.img_gate.convert_alpha()
        self.map = map
        self.display = True

    def show_map(self, save_image = True, image_prefix='image'):
        if self.display:
            self.screen.blit(self.img_map_west, (0, 0))
            self.screen.blit(self.img_map_east, (self.width / 2, 0))

            for node in self.map.nx_map.node:
                zone = self.map.nx_map.node[node]['zone']

                (x,y) = self.map.earth_gate_positions[zone.name]

                (x,y) = self.pygame_coords(x, y)

                if zone.gate_state is not GateState.noGate:
                    self.screen.blit(self.img_gate, (x - (self.gate_size/2), y - (self.gate_size/2)))
                i = 0
                for unit in zone.occupancy_list:
                    unit_x = x

                    if unit.gate_state == GateState.occupied:
                        print(unit.type, unit.gate_state, unit, zone.gate_state)
                    else:
                        unit_x = x + (i * self.unit_spacing)
                        i += 1;

                    unit_color = NodeColorINT.FactionColor[str(unit.faction._faction.value)]
                    pygame.draw.circle(self.screen, unit_color, (unit_x, y), self.unit_size, 0)
                    pygame.draw.circle(self.screen, (0, 0, 0, 0.25), (unit_x, y), self.unit_size + 1, 1)  # Black Border

                    textsurface = self.font.render(unit.unit_type.value, True, unit_color)
                    textsurface = pygame.transform.rotate(textsurface, 45)
                    shadowsurface = self.font.render(unit.unit_type.value, True, (0,0,0, 0.125))
                    shadowsurface = pygame.transform.rotate(shadowsurface, 45)

                    self.screen.blit(shadowsurface, (m.floor(unit_x - shadowsurface.get_width() * 0.5),
                                                     m.floor(y - shadowsurface.get_height() * 0.5) + 1))
                    self.screen.blit(shadowsurface, (m.floor(unit_x - shadowsurface.get_width() * 0.5),
                                                     m.floor(y - shadowsurface.get_height() * 0.5) - 1))

                    self.screen.blit(shadowsurface, (m.floor(unit_x - shadowsurface.get_width() * 0.5) + 1,
                                                     m.floor(y - shadowsurface.get_height() * 0.5)))
                    self.screen.blit(shadowsurface, (m.floor(unit_x - shadowsurface.get_width() * 0.5) - 1,
                                                      m.floor(y - shadowsurface.get_height() * 0.5) + 1))

                    self.screen.blit(textsurface, (m.floor(unit_x - textsurface.get_width()*0.5), m.floor(y-textsurface.get_height()*0.5)) )


                    # i += 1

            if save_image:
                print(image_prefix+self.file_format)
                pygame.image.save(self.screen, image_prefix+self.file_format)

    def pygame_coords(self, x, y):
        x = int(x * (self.width * 0.5) + self.width * 0.5)
        y = int((1.0 - y) * (self.height))
        return (x, y)
