from core import Board

if __name__ == "__main__":
    B = Board()
    B.build_map()
    B.create_players()
    B.start()
    B.test_move_actions()
