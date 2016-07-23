"""
 Black Goat faction class
 Home Zone is Africa or East Africa:
 Zone('Africa', False)
"""


# TODO: implement spell conditions
# TODO: implement Avatar ability for shub-nuggurath
# TODO: implement Fertility Cult in summoning logic
from core import Player
from cthulhuwars.Color import TextColor, NodeColor
from cthulhuwars.DiceRoller import DiceRoller
from cthulhuwars.Unit import Unit, UnitType, UnitState, Faction
from cthulhuwars.Zone import Zone, GateState

POOL = Zone('Pool')


class BlackGoat(Player):
    def __init__(self, home_zone, name='The Black Goat'):
        super(BlackGoat, self).__init__(Faction.black_goat, home_zone, name)
        '''
        Unit Lists
        The following lists are conveniences linking the relevant units from self._units
        '''
        self._dark_young = []
        self._fungi = []
        self._ghouls = []
        self._shub_niggurath = None
        '''
        spell flags
        True = spell has been acquired by player
        '''
        self.spell_thousand_young = False
        self.spell_frenzy = False
        self.spell_necrophagy = False
        self.spell_ghroth = False
        self.spell_red_sign = False
        self.spell_blood_sacrifice = False
        '''
        drawing colors
        '''
        self._color = TextColor.RED
        self.node_color = NodeColor.RED

    @property
    def dark_young_in_play(self):
        result = 0
        for dy in self._dark_young:
            if dy.unit_state is UnitState.in_play:
                result += 1
        return result

    @property
    def fungi_in_play(self):
        result = 0
        for dy in self._fungi:
            if dy.unit_state is UnitState.in_play:
                result += 1
        return result

    @property
    def ghouls_in_play(self):
        result = 0
        for dy in self._ghouls:
            if dy.unit_state is UnitState.in_play:
                result += 1
        return result

    @property
    def goo_in_play(self):
        return self._shub_niggurath.__len__()

    def player_setup(self):
        super(BlackGoat, self).player_setup()
        n_dark_young = 3
        n_ghoul = 2
        n_fungi = 4
        for _ in range(n_dark_young):
            new_dy = DarkYoung(self, POOL)
            self.add_unit(new_dy)
            self._dark_young.append(new_dy)

        for _ in range(n_ghoul):
            new_g = Ghoul(self, POOL)
            self.add_unit(new_g)
            self._ghouls.append(new_g)

        for _ in range(n_fungi):
            new_f = Fungi(self, POOL)
            self.add_unit(new_f)
            self._fungi.append(new_f)

        self._shub_niggurath = ShubNiggurath(self, POOL)
        self.add_unit(self._shub_niggurath)

    def summon_fungi(self, unit_zone):
        unit_cost = 2
        if self.spell_thousand_young:
            unit_cost = 1
        if self.power >= unit_cost:
            for fungi in self._fungi:
                if fungi.unit_state is UnitState.in_reserve:
                    if self.spend_power(unit_cost):
                        print(
                            self._color + TextColor.BOLD + 'A Fungi From Yuggoth has materialized!' + TextColor.ENDC)
                        fungi.set_unit_state(UnitState.in_play)
                        fungi.set_unit_zone(unit_zone)
                        return True
        return False

    def summon_ghoul(self, unit_zone):
        unit_cost = 1
        if self.spell_thousand_young:
            unit_cost = 0
        if self.power >= unit_cost:
            for ghoul in self._ghouls:
                if ghoul.unit_state is UnitState.in_reserve:
                    if self.spend_power(unit_cost):
                        print(self._color + TextColor.BOLD + 'A Ghoul appears!' + TextColor.ENDC)
                        ghoul.set_unit_state(UnitState.in_play)
                        ghoul.set_unit_zone(unit_zone)
                        return True
        return False

    def summon_dark_young(self, unit_zone):
        unit_cost = 3
        if self.spell_thousand_young:
            unit_cost = 2
        if self.power >= unit_cost:
            for dark_young in self._dark_young:
                if dark_young.unit_state is UnitState.in_reserve:
                    if self.spend_power(unit_cost):
                        print(self._color + TextColor.BOLD + 'A Dark Young has been summoned!' + TextColor.ENDC)
                        dark_young.set_unit_state(UnitState.in_play)
                        dark_young.set_unit_zone(unit_zone)
                        return True
        return False

    def summon_shub_niggurath(self, unit_zone):
        assert isinstance(unit_zone, Zone)
        print(
            self._color + TextColor.BOLD + 'The Black Goat is attempting to awaken Shub-Niggurath!' + TextColor.ENDC)
        unit_cost = 8
        # Do we have enough power?
        if self.power >= unit_cost:
            # is there a gate in the summoning zone, and do we occupy it?
            if unit_zone.gate_state is GateState.occupied:
                if unit_zone.gate_unit.faction == self:
                    # make sure we have enough cultists to sacrifice.
                    # Per Errata: must have controlled gate and two cultists anywhere
                    # interact with user to determine which cultists to sacrifice
                    # assumes gate occupying cultists will not be sacrificed
                    if self.current_cultists >= 2:
                        for _ in range(2):
                            kill_list = []
                            for unit in self._units:
                                if unit.unit_type is UnitType.cultist and unit.unit_state is UnitState.in_play:
                                    # TODO: remove occupancy assumption, replace with logic
                                    if unit.gate_state is not GateState.occupied:
                                        kill_list.append(unit)
                            print(self._color + 'Pick a cultist to sacrifice:')
                            for n in range(kill_list.__len__()):
                                print('  [' + str(n) + '] Cultist in %s' % kill_list[n].unit_zone.name)
                            while True:
                                sacrifice = int(raw_input('Selection:'))
                                if sacrifice < kill_list.__len__():
                                    break
                            self.remove_unit(kill_list[sacrifice])
                        # put shub_niggurath on the board, and spend the power
                        self._shub_niggurath.set_unit_zone(unit_zone)
                        self._shub_niggurath.set_unit_state(UnitState.in_play)
                        self.spend_power(unit_cost)
                        self._elder_points += DiceRoller(1, 3).roll_dice()[0]
                        print(
                            self._color + TextColor.BOLD + 'Shub-Niggurath Successfully Summoned!' + TextColor.ENDC)
                        return True
        return False

    def spell_play_thousand_young(self):
        self.spell_thousand_young = True

    def spell_play_red_sign(self):
        self.spell_red_sign = True

    def spell_play_frenzy(self):
        self.spell_frenzy = True
        for cultist in self._cultists:
            cultist.set_combat_power(1)

    def spell_play_ghroth(self):
        self.spell_ghroth = True

    def spell_play_necrophagy(self):
        self.spell_necrophagy = True

    def take_new_spell(self):
        # check conditions for taking a new spell:
        # Have Units in four Areas
        # Have Units in six Areas
        # Have Units in eight Areas
        # As your Action for a Round, eliminate two of your Cultists
        # Share Areas with all enemies (i.e. both you and your enemy have Units there.)
        # Awaken Shub-Niggurath
        pass

    def summon_action(self):
        unit_zone = None

        summon = [self.summon_cultist,
                  self.summon_dark_young,
                  self.summon_fungi,
                  self.summon_ghoul,
                  self.summon_shub_niggurath]

        for cultist in self._cultists:
            if cultist.gate_state is GateState.occupied:
                unit_zone = cultist.unit_zone

        if unit_zone is not None:
            '''RANDOM_PLAYOUT'''
            while True:
                dice = DiceRoller(1, summon.__len__()-1)
                dice_result = dice.roll_dice()[0] - 1
                if not summon[dice_result](unit_zone):
                    summon.pop(dice_result)
                else:
                    break

    def recompute_power(self):
        super(BlackGoat, self).recompute_power()
        if self.spell_red_sign:
            self._power += self.dark_young_in_play


class Ghoul(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=0):
        super(Ghoul, self).__init__(unit_parent, unit_zone, UnitType.ghoul, combat_power=0, cost=unit_cost,
                                    base_movement=1,
                                    unit_state=UnitState.in_reserve)


class Fungi(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=0):
        super(Fungi, self).__init__(unit_parent, unit_zone, UnitType.fungi, combat_power=1, cost=unit_cost,
                                    base_movement=1,
                                    unit_state=UnitState.in_reserve)


class DarkYoung(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=0):
        super(DarkYoung, self).__init__(unit_parent, unit_zone, UnitType.dark_young, combat_power=2, cost=unit_cost,
                                        base_movement=1,
                                        unit_state=UnitState.in_reserve)


class ShubNiggurath(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=8):
        super(ShubNiggurath, self).__init__(unit_parent, unit_zone, UnitType.GOO, combat_power=0, cost=unit_cost,
                                            base_movement=1,
                                            unit_state=UnitState.in_reserve)

    @property
    def combat_power(self):
        total_combat_power = self.faction.current_cultists + self.faction.current_gates
        if self.faction.spell_red_sign:
            total_combat_power += self.faction.dark_young_in_play
        return total_combat_power
