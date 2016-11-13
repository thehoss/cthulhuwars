from Channel import Channel
from PrintStream import PrintStream

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
        self._server.DelPlayer(self)

    ##################################
    ### Network specific callbacks ###
    ##################################

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
        print data
    def Network_faction(self, data):
        f = data['faction']
        self._server.board.player_dict[f]['active'] = True

        #with PrintStream() as x:
            #self._server.board.player_dict[f]['class'].player_setup()
        #self._server.SendToAll({"action": "gameMessage", "message": x.data})

        self.player_class = self._server.board.player_dict[f]['class']
        self.faction = f


    def Network_message(self, data):
        '''
        Pass a message from this client to all other clients
        :param data:
        :return:
        '''
        self._server.SendToAll({"action": "message", "message": data['message'], "who": self.faction})