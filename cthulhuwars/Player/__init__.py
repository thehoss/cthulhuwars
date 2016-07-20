from Cthulhu import Cthulhu
from BlackGoat import BlackGoat

if __name__ == "__main__":
    P1 = Cthulhu(name='Mrs. Reynolds')
    P1.player_setup()
    print(P1.print_state())

    P2 = BlackGoat(name='Mrs. Haase')
    P2.player_setup()
    print(P2.print_state())