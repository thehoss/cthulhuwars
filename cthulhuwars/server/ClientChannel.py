from Channel import Channel
from PrintStream import PrintStream
from cthulhuwars.Zone import GateState

class ClientChannel(Channel):
    """
    This is the server representation of a single connected client.
    This class contains a reference to the player faction object.
    Clients do NOT get a local reference to this data.  State is only
    maintained by the server
    """

    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.id = str(self._server.NextId())
        self.faction = ''
        self.player_class = None

    def PassOn(self, data):
        # pass on what we received to all connected clients
        data.update({"id": self.id})
        self._server.SendToAll(data)

    def Close(self):
        self._server.board.player_dict[self.faction]['active'] = False
        self._server.DelPlayer(self)

    ##################################
    ### Network specific callbacks ###
    ##################################

    def Network_mapState(self, data):
        gate_data = []
        unit_data = []
        for node in self._server.board.map.nx_map.node:
            zone = self._server.board.map.zone_by_name(node)
            if zone.gate_state is not GateState.noGate:
                gate_data.append(zone.name)

        for p in self._server.board.players:
            units = p.units_in_play
            for unit in units:
                unit_data.append( (unit.unit_zone.name, unit.faction.short_name, unit.unit_type.value, unit.gate_state.value) )

        print unit_data
        self._server.SendToAll({"action": "mapState", "gate_data": gate_data, "unit_data": unit_data})


    def Network_boardState(self, data):
        '''
        The current state of the board from the server has been requested. send it to the client
        :param data:
        :return:
        '''
        print "Board State Request"
        with PrintStream() as x:
            self._server.board.print_state()
        #print x.data
        self.Send({"action": "gameMessage", "message": x.data})

    def Network_me(self, data):
        '''
        The state of the current player has been requested.  Send it only to the client this channel represents.
        :param data:
        :return:
        '''
        with PrintStream() as x:
            self.player_class.print_state()
        self.Send({"action": "gameMessage", "message": x.data})

    def Network_disconnect(self, data):
        self._server.SendToAll({"action": "gameMessage", "message": [('%s is disconnecting')%(self.faction)]})
        self._server.board.player_dict[self.faction]['active'] = False
        self.Close()

    def Network_initial(self, data):
        '''
        Called when a client connects
        :param data:
        :return:
        '''
        print data


    def Network_gameTurn(self, data):
        '''
        Called when a client connects
        :param data:
        :return:
        '''
        self.Network_mapState(data)
        print data

    def Network_faction(self, data):
        f = data['faction']
        self._server.board.player_dict[f]['active'] = True

        with PrintStream() as x:
            self._server.board.player_dict[f]['class'].player_setup()


        self.player_class = self._server.board.player_dict[f]['class']
        self.faction = f
        self.Network_mapState(data)

        available_factions = {}
        for k, v in self._server.board.player_dict.items():
            available_factions[k] = self._server.board.player_dict[k]['active']

        self._server.SendToAll({"action": "gameMessage", "message": x.data, "factions": available_factions})


    def Network_message(self, data):
        '''
        Pass a message from this client to all other clients
        :param data:
        :return:
        '''
        self._server.SendToAll({"action": "message", "message": data['message'], "who": self.faction})