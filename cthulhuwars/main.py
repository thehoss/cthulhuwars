from cwgame.board import Board

def main():
    numPlayers = int(input('number of players: '))
    B = Board(num_players=numPlayers, server_mode=False, draw_map=True)

if __name__ == "__main__":
    main()

