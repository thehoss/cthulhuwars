from core import Board, Actions, Phase

if __name__ == "__main__":
    B = Board()
    B.build_map()
    B.create_players()
    B.start()
    B.print_state()
    B.render_map('play.0001')
    i = 1
    num_rounds = 1
    for r in range(num_rounds):
        B.gather_power_phase()
        B.print_state()

        #first player phase
        while True:
            print('**Round %s, Turn %s **' % (r,i))
            B.test_actions()
            i += 1
            B.render_map('play.%s'%str('%04d'%i))
            if not B.is_action_phase():
                break
        #doom phase
        #annihilation phase


