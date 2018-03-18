import cwgame.board as Board
import server.CWServer as CWServer
import server.CWClient as CWClient

serveraddress=('localhost', int(10666))

def main():
    numPlayers = int(input('number of players: '))
    B = Board(num_players=numPlayers, server_mode=False, draw_map=True)

def client():
    c =CWClient.CWClient(host=serveraddress[0], port=serveraddress[1])
    c.Launch()

def server():
    s = CWServer.CWServer(localaddr=serveraddress, num_players = 2)
    s.Launch()

if __name__ == "__main__":
    selection = int( input (" (1) Launch Server \n (2) Launch Client \n (3) Launch Self-Playing Game\n") )

    if (selection == 1):
        server()
    elif(selection == 2):
        client()
    else:
        main()

