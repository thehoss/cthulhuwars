import os

import pygame
import math as m
from .zone import Zone, GateState
import cthulhuwars.cwgame.color as Color

class Display(object):
    def __init__(self):
        self.font = None
        self.screen = None
        self.display = False
        self.img_gate = None
        self.img_map_east = None
        self.img_map_west = None
        self.nx_map = None
        self.basepath = './tex'
        self.imagepath = '.'
        self.file_format = '.png'
        self.width, self.height = 1000, 500

    def init(self, east_map_filename, west_map_filename, map):
        pygame.init()
        pygame.font.init()
        # self.font = pygame.font.Font('display.ttf', 10)
        self.font = pygame.font.SysFont(None, 16)
        # initialize the screen
        self.screen = pygame.display.set_mode((self.width, self.height))
        # self.clock = pygame.time.Clock()

        self.img_map_east = pygame.image.load(east_map_filename)
        self.img_map_west = pygame.image.load(west_map_filename)

        west = pygame.transform.smoothscale(self.img_map_west, (m.floor(self.width / 2), self.height))
        east = pygame.transform.smoothscale(self.img_map_east, (m.floor(self.width / 2), self.height))
        self.img_map_east = east.convert()
        self.img_map_west = west.convert()

        self.img_gate = pygame.image.load(os.path.join(self.basepath, 'gate.png'))
        self.img_gate = pygame.transform.smoothscale(self.img_gate, (32, 32))
        self.img_gate = self.img_gate.convert_alpha()
        self.map = map
        self.display = True

    def show_map(self, save_image = False, image_prefix='image'):
        if self.display:
            self.screen.blit(self.img_map_west, (0, 0))
            self.screen.blit(self.img_map_east, (self.width / 2, 0))

            for node in self.map.nx_map.node:

                zone = self.map.nx_map.node[node]['zone']
                (x,y) = self.map.earth_gate_positions[zone.name]
                (x,y) = self.map.pygame_coords(x, y)

                if zone.gate_state != GateState.noGate:
                    self.screen.blit(self.img_gate, (x - 16, y - 16))
                i = 0
                for unit in zone.occupancy_list:
                    unit_x = x
                    if unit.gate_state != GateState.occupied:
                        unit_x = x + (i * 20)

                    unit_color = Color.NodeColorINT.FactionColor[str(unit.faction._faction.value)]
                    pygame.draw.circle(self.screen, unit_color, (unit_x, y), 7, 0)
                    pygame.draw.circle(self.screen, (0, 0, 0), (unit_x, y), 8, 1)  # Black Border

                    textsurface = self.font.render(unit.unit_type.value, True, unit_color)
                    textsurface = pygame.transform.rotate(textsurface, 45)
                    shadowsurface = self.font.render(unit.unit_type.value, True, (0,0,0, 0.25))
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


                    i += 1

            if save_image:
                pygame.image.save(self.screen, image_prefix+self.file_format)