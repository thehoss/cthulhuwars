from Channel import Channel

class ClientChannel(Channel):
    """
    This is the server representation of a single connected client.
    """

    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.id = str(self._server.NextId())

        self.faction = ''

    def PassOn(self, data):
        # pass on what we received to all connected clients
        data.update({"id": self.id})
        self._server.SendToAll(data)

    def Close(self):
        self._server.DelPlayer(self)

    ##################################
    ### Network specific callbacks ###
    ##################################

    def Network_boardState(data):
        print "Board State:", data

    def Network_initial(self, data):
        self.faction = data['faction']

    def Network_message(self, data):
        self._server.SendToAll({"action": "message", "message": data['message'], "who": self.faction})