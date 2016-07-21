from core import Board

if __name__ == "__main__":
    B = Board()
    B.build_map()
    B.create_players()
    B.start()
    B.gather_power_phase()
    B.print_state()
    B.test_move_actions()
    B.test_move_actions()
    B.test_move_actions()
    B.print_state()

