from core import Board, Actions, Phase

if __name__ == "__main__":
    B = Board()
    B.build_map()
    B.create_players()
    B.start()
    #B.render_map('play.1001')
    i = 1
    num_rounds = 16
    r = 0
    winner = False
    while winner is False:
        B.gather_power_phase()
        #B.print_state()

        #first player phase
        while True:
            print('**Round %s, Turn %s **' % (r,i))
            B.test_actions()

            f = i + 1001
            #B.render_map('play.%s'%str('%04d'%f))
            i += 1
            if not B.is_action_phase():
                break

        #B.render_map('play.%s' % str('%04d'%(r+1001)))
        r += 1
        winner = B.doom_phase()
        B.print_state()

                #doom phase
        #annihilation phase


