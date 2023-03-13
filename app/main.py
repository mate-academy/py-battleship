class Ship:
    decks = []

    def __init__(
            self,
            start: tuple,
            end: tuple,
    ) -> None:
        self.deck = self.create_deck(start, end)
        Ship.decks.append(self)

    @staticmethod
    def create_deck(start: tuple, end: tuple) -> list:
        if start[0] == end[0]:
            return [(start[0], point) for point in range(start[1], end[1] + 1)]

        return [(start[1], point) for point in range(start[0], end[0] + 1)]


class NotEnoughShips(Exception):
    pass


class MissingSomeShips(Exception):
    pass


class Battleship:
    battle_field = [["~"] * 10] * 10

    def __init__(self, ships: list) -> None:
        self.field = self.create_field(ships)
        self._validate_field()

    def fire(self, location: tuple) -> str:
        for ship in Ship.decks:
            self.battle_field[location[0]][location[1]] = "x"
            if location in ship.deck and len(ship.deck) == 1:
                Ship.decks.remove(ship)
                return "Sunk!"
            elif location in ship.deck:
                ship.deck.remove(location)
                return "Hit!"
        return "Miss!"

    @staticmethod
    def create_field(ships: list) -> dict:
        return {ship: Ship(start=ship[0], end=ship[1]) for ship in ships}

    def print_field(self) -> None:

        for ship in Ship.decks:
            for point in ship.deck:
                self.battle_field[point[0]][point[1]] = "□"

        for line in self.battle_field:
            print(line)

    def _validate_field(self) -> None:
        check_dict = {
            4: 1,
            3: 2,
            2: 3,
            1: 4
        }
        dic_ships = {
            4: 0,
            3: 0,
            2: 0,
            1: 0
        }
        if len(self.field) != 10:
            raise NotEnoughShips("Pleas enter correct number of ships")
        for ship in Ship.decks:
            dic_ships[len(ship.deck)] += 1
        if dic_ships != check_dict:
            raise MissingSomeShips("Please check the correctness "
                                   "of the entered data")
