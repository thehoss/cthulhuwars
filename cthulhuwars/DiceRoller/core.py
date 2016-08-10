import random


class DiceRoller:

    def __init__(self, num_dice=2, num_sides=6):
        self.num_dice = num_dice
        self.num_sides = num_sides
        self.dice_results = []

    def __roll(self):
        result = random.randint(1, self.num_sides)
        return result

    def roll_dice(self):
        self.dice_results = []
        for _ in range(self.num_dice):
            self.dice_results.append(int(self.__roll()))
        return self.dice_results

    def interpret_dice(self):
        results = []

        self.roll_dice()

        for roll in self.dice_results:
            if roll == 4 or roll == 5:
                results.append('pain')
            elif roll == 6:
                results.append('kill')
        return results