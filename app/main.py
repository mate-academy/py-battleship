from dataclasses import dataclass, field


@dataclass
class Deck:

    row: int
    column: int
    is_alive: bool = True


@dataclass
class Ship:
    start: tuple
    end: tuple
    is_drowned: bool = False
    decks: list = field(init=False)

    def __post_init__(self) -> None:
        decks = []
        for x_coord in range(self.start[0], self.end[0] + 1):
            for y_coord in range(self.start[1], self.end[1] + 1):
                decks.append(Deck(x_coord, y_coord))
        self.decks = decks

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False

        hit_decks = 0
        for deck in self.decks:
            if deck.is_alive is False:
                hit_decks += 1
        if hit_decks == len(self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self._validate_field(ships)

        field = {}
        for x_coord in range(10):
            for y_coord in range(10):
                field[(x_coord, y_coord)] = None

        for item in ships:
            ship = Ship(item[0], item[1])
            for deck in ship.decks:
                field[(deck.row, deck.column)] = ship

        self.field = field

    @staticmethod
    def _validate_field(ships: list) -> None:

        if len(ships) != 10:
            raise ValueError("There must be 10 ships.")

        for ship in ships:
            other_ships = [
                end for temp in ships if temp != ship for end in temp
            ]
            for end in ship:
                neighbours = [
                    (end[0] - 1, end[1] - 1),
                    (end[0] - 1, end[1]),
                    (end[0] - 1, end[1] + 1),
                    (end[0], end[1] - 1),
                    (end[0], end[1] + 1),
                    (end[0] + 1, end[1] - 1),
                    (end[0] + 1, end[1]),
                    (end[0] + 1, end[1] + 1),
                ]

                for neighbour in neighbours:
                    if neighbour in other_ships:
                        raise ValueError("The ships must not be adjacent.")

        deck_size = []
        for ship in ships:
            deck_size.append(
                (ship[1][0] - ship[0][0]) + (ship[1][1] - ship[0][1]) + 1
            )
        if sorted(deck_size) != [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]:
            raise ValueError("Wrong ship size configuration.")

    def fire(self, location: tuple) -> str:
        row = location[0]
        column = location[1]
        cell = self.field[location]
        if cell is not None:
            cell.fire(row, column)
            if cell.is_drowned is True:
                self.print_field()
                return "Sunk!"
            else:
                self.print_field()
                return "Hit!"

        else:
            self.print_field()
            return "Miss!"

    def print_field(self) -> None:
        counter = 0
        row = ""
        for key, value in self.field.items():
            if value is None:
                row += " 🌊 "
            else:
                if value.get_deck(key[0], key[1]).is_alive:
                    row += " 🚢 "
                elif value.is_drowned:
                    row += " ❌ "
                else:
                    row += " 🔥 "
            counter += 1
            if counter % 10 == 0:
                print(row)
                row = ""
