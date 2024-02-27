from app.main import Battleship


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.fleet = {
            "single_deck": 0, "double_deck": 0, "three_deck": 0,
            "four_deck": 0
        }
        # self.battleship = Battleship()

    def _validate_field(self, ship: tuple[tuple, tuple]) -> None:
        if sum(self.fleet.values()) > 10:
            raise ValueError("The total number of the ships should be 10")
        count_deck = abs(
            (ship[1][0] - ship[0][0]) - (ship[1][1] - ship[0][1])) + 1
        if count_deck == 1:
            self.fleet["single_deck"] += 1
        elif count_deck == 2:
            self.fleet["double_deck"] += 1
        elif count_deck == 3:
            self.fleet["three_deck"] += 1
        elif count_deck == 4:
            self.fleet["four_deck"] += 1
        if self.fleet["single_deck"] > 4:
            raise ValueError("there should be 4 single-deck ships")
        if self.fleet["double_deck"] > 3:
            raise ValueError("there should be 3 double-deck ships")
        if self.fleet["three_deck"] > 2:
            raise ValueError("there should be 2 three-deck ships")
        if self.fleet["four_deck"] > 1:
            raise ValueError("there should be 1 four-deck ship")
        for row in range(ship[0][0] - 1, ship[1][0] + 2):
            for column in range(ship[0][1] - 1, ship[1][1] + 2):
                if (row, column) in self.field:
                    raise ValueError("Ships should not be located in "
                                     "neighboring cells")

    def my_fleet(self) -> None:
        pass

    def add_ship(self, ship_coordinates: tuple[tuple, tuple]) -> None:
        pass


player = Player("Alex")
player.add_ship(((0, 0), (0, 3)))
