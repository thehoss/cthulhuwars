from cthulhuwars.Unit import Unit, UnitType, UnitState, Faction
from cthulhuwars.Zone import Zone, GateState


class Player(object):
    def __init__(self, faction=Faction.cthulhu, home_zone=Zone('South Pacific', True), name='Player1'):
        self.__name = name
        self.__faction = faction
        self.__home_zone = home_zone
        self.__spells = []
        self.__units = []
        self.__power = 8
        self.__doom_points = 0
        self.__elder_points = 0
        self.__starting_cultists = 6
        self.__current_cultists = 0
        self.__current_gates = 0

    def player_setup(self):
        # add starting gate and cultist to home zone
        self.build_gate_action(self._add_cultist(self.__home_zone), self.__home_zone)
        # add remaining cultists
        for _ in range(1, self.__starting_cultists, 1):
            self._add_cultist(self.__home_zone)

    def _add_cultist(self, zone):
        if self.__power > 0:
            newCultist = Unit(self.__faction, UnitType.cultist, 0, 1, 1, UnitState.in_play, zone)
            self.__units.append(newCultist)
            self.__power -= 1
            self.__current_cultists += 1
            return newCultist
        elif self.__power < 1:
            # TODO: add failure reporting mechanism
            print ('not enough power to summon cultist!')

    @property
    def power(self):
        return self.__power

    def __computePower(self):
        self.__power = self.__current_cultists
        self.__power += self.__current_gates * 2
        # add gates and special stuff.  This method will be overridden by faction specific thingies.
        pass

    def move_action(self):
        pass

    def combat_action(self):
        pass

    def build_gate_action(self, unit, zone):
        zone_state = zone.get_zone_state()
        if zone_state[0] == GateState.noGate:
            if self.power >= 2:
                zone.set_gate_state(GateState.occupied)
                zone.set_gate_unit(unit)
                unit.set_unit_gate_state(GateState.occupied)
                self.__current_gates += 1
                self.__power -= 2
            else:
                print ('Not enough power to build gate!')
        else:
            print ('Gate already exists!')

    def spell_book_action(self):
        pass

    def summon_action(self):
        pass

    def pre_combat_action(self):
        pass

    def post_combat_action(self):
        pass

    def pre_doom_action(self):
        pass

    def post_doom_action(self):
        pass

    def pre_turn_action(self):
        pass

    def post_turn_action(self):
        pass

    def print_state(self):
        self.__computePower()
        print ('name: %s' % self.__name)
        print ('faction: %s' % self.__faction)
        print ('home zone: %s' % self.__home_zone)
        print ('spells: %s' % self.__spells)
        print ('units: %s' % self.__units)
        print ('power: %s' % self.__power)
        print ('doom points: %s' % self.__doom_points)
        print ('elder sign points: %s' % self.__elder_points)
        print ('starting cultists: %s' % self.__starting_cultists)
        print ('current cultists: %s' % self.__current_cultists)
        print ('current gates: %s' % self.__current_gates)


class BlackGoat(Player):
    def __init__(self, faction=Faction.black_goat, home_zone=Zone('Africa', False), name='Player2'):
        super(BlackGoat, self).__init__(faction, home_zone, name)
