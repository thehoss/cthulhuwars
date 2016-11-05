from Channel import Channel
import sys

class PrintStream:
    def __init__(self):
        self.data = []
    def write(self, s):
        self.data.append(s)
    def __enter__(self):
        sys.stdout = self
        return self
    def __exit__(self, ext_type, exc_value, traceback):
        sys.stdout = sys.__stdout__

class ClientChannel(Channel):
    """
    This is the server representation of a single connected client.
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
        print "Board State Request"
        with PrintStream() as x:
            self._server.board.print_state()
        #print x.data
        self.Send({"action": "gameMessage", "message": x.data})

    def Network_me(self, data):
        with PrintStream() as x:
            self.player_class.print_state()
        self.Send({"action": "gameMessage", "message": x.data})

    def Network_initial(self, data):
        self.faction = data['faction']

    def Network_message(self, data):
        self._server.SendToAll({"action": "message", "message": data['message'], "who": self.faction})