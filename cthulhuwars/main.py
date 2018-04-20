from cwgame.board import Board
import server.CWServer as CWServer
import server.CWClient as CWClient
import sys, os
import argparse
parser = argparse.ArgumentParser(description='Play some Cthulu Wars')
parser.add_argument('--num_players', type=int, help='the number of players')
parser.add_argument('--headless', help='run without a display', action="store_true")
parser.add_argument('--server', help='start in server mode', action="store_true")
parser.add_argument('--client', help='start in client mode', action="store_true")
parser.add_argument('--self-play', help='start in self-play mode', action="store_true")
parser.add_argument('--player1', type=str, help='the faction for player 1 (cthulu,black_goat,crawling_chaos,yellow_sign)')
parser.add_argument('--player2', type=str, help='the faction for player 2 (cthulu,black_goat,crawling_chaos,yellow_sign)')
parser.add_argument('--player3', type=str, help='the faction for player 3 (cthulu,black_goat,crawling_chaos,yellow_sign)')
parser.add_argument('--player4', type=str, help='the faction for player 4 (cthulu,black_goat,crawling_chaos,yellow_sign)')

serveraddress=('localhost', int(10666))

def main(num_players,headless,player1,player2,player3,player4):
    if not num_players:
        num_players = int(input('number of players: '))
    draw_map = False if headless else True
    B = Board(num_players=num_players, server_mode=False,
              draw_map=draw_map,
              player1=player1,
              player2=player2,
              player3=player3,
              player4=player4,
              )

def client():
    c =CWClient.CWClient(host=serveraddress[0], port=serveraddress[1])
    c.Launch()

def server(num_players):
    if not num_players:
        num_players=2
    s = CWServer.CWServer(localaddr=serveraddress, num_players=num_players)
    s.Launch()

if __name__ == "__main__":
    cwd = os.path.dirname(os.path.abspath(__file__))
    sys.path.extend([cwd])
    args = parser.parse_args()
    if args.server:
        server(num_players=args.num_players)
    elif args.client:
        client()
    elif args.self_play:
        main(num_players=args.num_players,
             headless=args.headless,
             player1=args.player1,
             player2=args.player2,
             player3=args.player3,
             player4=args.player4)
    else:
        selection = int( input (" (1) Launch Server \n (2) Launch Client \n (3) Launch Self-Playing Game\n") )
        
        if (selection == 1):
            server(num_players=args.num_players)
        elif(selection == 2):
            client()
        else:
            main(num_players=args.num_players,
                 headless=args.headless,
                 player1=args.player1,
                 player2=args.player2,
                 player3=args.player3,
                 player4=args.player4)

