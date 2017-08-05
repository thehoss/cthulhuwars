import sys
sys.path.insert(0, '../../')
sys.path.insert(0, '.')
sys.path.insert(0, './PodSixNet')

from time import sleep
from sys import stdin, exit
import os
from PodSixNet.Connection import connection, ConnectionListener
#from thread import *
from cthulhuwars.cwgame import color as Color
from cthulhuwars.cwgame.unit import Faction
import pygame, math

serveraddress=('localhost', int(10666))

class CWClient(ConnectionListener):
    earth_gate_positions = {'Arctic Ocean': [0.03, 0.9], 'North Atlantic': [-0.23, 0.57],
                            'South Atlantic': [-0.05, 0.24], 'Indian Ocean': [0.69, 0.21],
                            'North Pacific': [-0.9, 0.54], 'South Pacific': [-0.53, 0.09],
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
    width, height = 800, 400

    Factions = ['yellow_sign', 'crawling_chaos', 'cthulhu', 'black_goat']

    FactionColor = {
        'cthulhu': Color.NodeColorINT.GREEN,
        'black_goat': Color.NodeColorINT.RED,
        'crawling_chaos': Color.NodeColorINT.BLUE,
        'yellow_sign': Color.NodeColorINT.YELLOW

    }

    def pygame_coords(self, x, y):
        x = int(x * (self.width * 0.5) + self.width * 0.5)
        y = int((1.0 - y) * (self.height))
        return (x, y)

    def __init__(self, host='localhost', port=int(666)):
        '''
        A thin client.  This class is the user interface to the game.  Game and player state are kept only on the server
        Client requests data and posts commands.
        :param host:
        :param port:
        '''
        self.players = {}
        self.statusLabel = 'connecting'
        self.playersLabel = "0 players"
        self.faction = ''
        self.faction_color = ''
        self.connected = False
        self.Connect((host, port))
        self.in_play = False

        self.resource_dir = '../cwgame/tex'
        self.img_map_west = None
        self.img_map_east = None
        self.img_selectionbg = None
        self.img_gate = None
        self.available_factions = []

        self.gate_data = []
        self.unit_data = []
        self.img_factions = []
        self.img_faction_selection = {
            'cthulhu':{'active':None, 'inactive':None,'selected':None},
            'black_goat': {'active': None, 'inactive': None, 'selected': None},
            'crawling_chaos': {'active': None, 'inactive': None, 'selected': None},
            'yellow_sign': {'active': None, 'inactive': None, 'selected': None}
        }
        pygame.init()

        # initialize the screen
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

    def draw_board(self):
        '''
        draw the board
        :return:
        '''
        self.screen.blit(self.img_map_west, (0, 0))
        self.screen.blit(self.img_map_east, (self.width / 2, 0))

        for zone in self.gate_data:
            (x,y)=self.earth_gate_positions[zone]
            (x,y) = self.pygame_coords(x, y)
            self.screen.blit(self.img_gate, (x - 16, y - 16))

        i = 0
        lastZone = ''
        for (unit_zone, faction_name, unit_type, gate_state) in self.unit_data:
            if i > 0 and unit_zone != lastZone:
                i = 0
            i += 1
            (x,y) = self.earth_gate_positions[unit_zone]
            (x, y) = self.pygame_coords(x, y)
            if gate_state != 2:
                x = x + i*10
            pygame.draw.circle(self.screen, self.FactionColor[faction_name], (x,y), 7, 0)
            pygame.draw.circle(self.screen, (0,0,0), (x, y), 8, 1)
            lastZone = unit_zone

    def draw_selectionScreen(self):
        self.screen.blit(self.img_selectionbg, (0, 0))
        for fac in self.Factions:
            img = self.img_faction_selection[fac]['inactive']
            if self.available_factions[fac] == False:
                img = self.img_faction_selection[fac]['selected']
            self.screen.blit(img, (0, 0))

    def update_selection(self):
        # sleep to make the game 60 fps
        self.clock.tick(60)
        connection.Pump()
        self.Pump()

        # clear the screen
        self.screen.fill(0)
        self.draw_selectionScreen()
        (x,y) = pygame.mouse.get_pos()

        for fac in self.Factions:
            img = self.img_faction_selection[fac]['active']
            bounds = img.get_bounding_rect(min_alpha=1)
            if bounds.collidepoint(x, y) == True:
                self.screen.blit(img, (0, 0))

        for event in pygame.event.get():
            # quit if the quit button was pressed
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEMOTION:
                (x,y) = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                (x,y) = event.pos
                self.faction_selection(x,y)
        # update the screen
        pygame.display.flip()

    def update_game(self):
        # sleep to make the game 60 fps
        self.clock.tick(60)
        connection.Pump()
        self.Pump()

        self.draw_board()

        for event in pygame.event.get():
            # quit if the quit button was pressed
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                (x,y) = event.pos

        # update the screen
        pygame.display.flip()

    def faction_selection(self, x, y):
        for fac in self.Factions:
            img = self.img_faction_selection[fac]['active']
            bounds = img.get_bounding_rect(min_alpha=1)
            #print(bounds)
            if bounds.collidepoint(x,y):
                self.faction = fac
                self.faction_color = self.FactionColor[self.faction]
                self.sprint('joined as faction ' + self.faction)
                connection.Send({"action": "faction", "faction": self.faction})
                self.in_play = True
                return
        #print x,y

    def sprint(self, msg, mode='info', head='[CWClient]: '):
        '''
        for to make pretty printing
        :param msg:
        :param mode:
        :return:
        '''
        if mode == 'info':
            print(Color.TextColor.GREEN+Color.TextColor.BOLD+head+msg)
        if mode == 'error':
            print(Color.TextColor.RED+Color.TextColor.BOLD+head+msg)
        if mode == 'warning':
            print(Color.TextColor.YELLOW+Color.TextColor.BOLD+head+msg)
        if mode == 'chat':
            print(Color.TextColor.BLUE+Color.TextColor.BOLD+msg)
        print(Color.TextColor.ENDC)

    def Launch(self):
        while True:
            if self.in_play:
                self.update_game()
            else:
                self.update_selection()
            sleep(0.001)

    def Network(self, data):
        # print('network:', data)
        pass

    def Network_mapState(self, data):
        '''
        receive gate data
        :param data:
        :return:
        '''
        self.gate_data = data['gate_data']
        self.unit_data = data['unit_data']

    def Network_connected(self, data):
        '''
        called when connected action is sent
        :param data:
        :return:
        '''
        self.statusLabel = "connected"
        self.sprint("Connected to the server")

    def load_resources(self, data):
        pygame.display.set_caption("Loading Resources...")

        self.img_gate = pygame.image.load(os.path.join(self.resource_dir, 'gate.png'))
        self.img_gate = pygame.transform.smoothscale(self.img_gate, (32, 32))
        self.img_gate = self.img_gate.convert_alpha()

        self.img_selectionbg = pygame.image.load(os.path.join(self.resource_dir, 'select_background.png'))

        self.img_selectionbg = pygame.transform.smoothscale(self.img_selectionbg, (self.width, self.height))
        self.img_selectionbg = self.img_selectionbg.convert()

        for k in self.available_factions:
            for state in ['active','inactive','selected']:
                img = os.path.join(self.resource_dir, 'select_%s_%s.png'%(state, k))

                imgsurface = pygame.image.load(img)
                imgsurface = pygame.transform.smoothscale(imgsurface, (self.width, self.height))
                imgsurface = imgsurface.convert_alpha()

                self.img_faction_selection[k][state] = imgsurface

        self.img_map_east = pygame.image.load(data['mapImageData'][1])
        self.img_map_west = pygame.image.load(data['mapImageData'][0])

        west = pygame.transform.smoothscale(self.img_map_west, (int(self.width / 2), self.height))
        east = pygame.transform.smoothscale(self.img_map_east, (int(self.width / 2), self.height))
        self.img_map_east = east.convert()
        self.img_map_west = west.convert()

        pygame.display.set_caption("Cthulhu Warz")

    def Network_error(self, data):
        '''
        report errors from the server
        :param data:
        :return:
        '''
        self.sprint('error:'+str(data['error']), mode='error')

        import traceback
        traceback.print_exc()
        connection.Close()
        exit(-1)

    def Network_initial(self, data):
        '''
        called when initial action is sent by server, after client connect
        :param data:
        :return:
        '''
        self.available_factions = data['factions']
        self.load_resources(data)
        self.connected = True
        self.in_play = False

    def Network_disconnected(self, data):
        self.statusLabel += " - disconnected"
        self.sprint('Server disconnected * ', mode='warning')
        exit()

    def Network_players(self, data):
        '''
        prints the player data from the server
        :param data:
        :return:
        '''
        self.sprint("*** players: " + ", ".join([p for p in data['players']]), head="[SERVER]: ")

    def Network_message(self, data):
        '''
        prints a message from another client
        :param data:
        :return:
        '''
        self.sprint( data['message'], mode='chat', head="["+data['who'] + "]: ")

    def Network_gameMessage(self, data):
        '''
        prints a game message from the server
        :param data:
        :return:
        '''
        msg = data['message']
        self.sprint(''.join(msg), head="[SERVER]: ")

    def Network_gameTurn(self, data ):

        # self.sprint(data['message'])

        selection = input("Action (msg, move, attack, build, summon, end): ")
        command_list = selection.split(' ', 1)

        if command_list[0] in ["msg", "m", "message", "/m"]:
            connection.Send({"action": "message", "message": command_list[1]})
        if command_list[0] in ["end","x", "exit", "quit", "/x"]:
            connection.send({"action": "disconnect"})
            connection.close()

        return

if __name__ == "__main__":
    c = CWClient(host=serveraddress[0], port=serveraddress[1])
    c.Launch()