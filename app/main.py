from __future__ import annotations


class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"Deck - ({self.row}-{self.column})"

    def __eq__(self, other: tuple) -> bool:
        if (self.row, self.column) == other:
            return True
        return False


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
    ) -> None:
        self.decks = []
        self.coords = []
        self.is_horizontal = False
        self.is_drowned = False
        self.lentgh = self.find_lentgh(start, end)
        self.find_lentgh(start, end)
        self.create_decks(start, end)

    def find_lentgh(
            self,
            start: tuple[int, int],
            end: tuple[int, int]
    ) -> int:
        if start[0] == end[0]:
            return abs(end[1] - start[1]) + 1
        self.is_horizontal = True
        return abs(end[0] - start[0]) + 1

    def check_is_drowned(self) -> bool:
        for deck in self.decks:
            if deck.is_alive:
                return False
        return True

    def create_decks(
            self,
            start: tuple[int, int],
            end: tuple[int, int]
    ) -> None:
        if start == end:
            self.decks.append(Deck(*start))
            self.coords.append(start)
            return
        for deck in range(self.lentgh):
            if self.is_horizontal:
                self.decks.append(Deck(*start))
                self.coords.append(start)
                if abs(start[0] + 1 - end[0]) < abs(start[0] - end[0]):
                    temp_list = list(start)
                    temp_list[0] += 1
                    start = tuple(temp_list)
                    self.coords.append(start)

                else:
                    temp_list = list(start)
                    temp_list[0] -= 1
                    start = tuple(temp_list)
                    self.coords.append(start)

            else:
                self.decks.append(Deck(*start))
                self.coords.append(start)
                if abs(start[1] + 1 - end[1]) < abs(start[1] - end[1]):
                    temp_list = list(start)
                    temp_list[1] += 1
                    start = tuple(temp_list)
                    self.coords.append(start)
                else:
                    temp_list = list(start)
                    temp_list[1] -= 1
                    start = tuple(temp_list)
                    self.coords.append(start)
        self.coords = sorted(list(set(self.coords)))

    def __repr__(self) -> str:
        if self.is_drowned:
            return "x"
        return "□"

    def get_deck(self, row: int, column: int) -> None:
        for deck in self.decks:
            if (deck.row, deck.column) == (row, column):
                return deck
        return None


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.playground = self.make_playground()
        self.field = {}
        for ship_coords in ships:
            ship = Ship(*ship_coords)
            ship_coords = ship.coords
            for coords in ship_coords:
                self.field[coords] = ship
        self.set_ships()

    def set_ships(self) -> None:
        for deck in self.field.keys():
            self.playground[deck[0]][deck[1]] = self.field[deck]

    def fire(self, location: tuple) -> str:
        if location in self.field.keys():
            ship = self.field[location]
            ship.decks[ship.decks.index(location)].is_alive = False
            if self.field[location].check_is_drowned():
                for deck in ship.decks:
                    row = deck.row
                    column = deck.column
                    self.playground[row][column] = "x"
                return "Sunk!"
            row = ship.decks[ship.decks.index(location)].row
            column = ship.decks[ship.decks.index(location)].column
            self.playground[row][column] = "*"
            return "Hit!"
        return "Miss!"

    @classmethod
    def make_playground(cls) -> list[list[str]]:
        ground = []
        for _ in range(10):
            ground.append(["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", ])
        return ground

    def print_playground(self) -> None:
        print("Playground")
        for row in range(10):
            for cell in range(10):
                print(f" {self.playground[row][cell]}  ", end="")
            print()
        print()
