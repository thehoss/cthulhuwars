from core import DiceRoller

if __name__ == "__main__":
    D = DiceRoller(5, 6)
    D.roll_dice()
    print(D.interpret_dice())
