class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple[int],
            end: tuple[int],
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        if start[0] == end[0]:
            self.decks = [
                Deck(start[0], index) for index in range(start[1], end[1] + 1)
            ]
        if start[1] == end[1]:
            self.decks = [
                Deck(index, start[1]) for index in range(start[0], end[0] + 1)
            ]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> str:
        fire_deck = self.get_deck(row, column)
        if fire_deck.is_alive:
            fire_deck.is_alive = False
            if all(not deck.is_alive for deck in self.decks):
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"
        return "Miss!"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {ship: Ship(ship[0], ship[1]) for ship in ships}
        self.__validate_field()

    def fire(self, location: tuple[int]) -> str:
        for key, ship in self.field.items():
            if key[0] <= location <= key[1] and not ship.is_drowned:
                return ship.fire(location[0], location[1])
        return "Miss!"

    def print_field(self) -> None:
        field = {item: "~" for item in range(100)}

        for ship in self.field.values():
            for deck in ship.decks:
                field_key = int(str(deck.row) + str(deck.column))
                if deck.is_alive:
                    field[field_key] = u"\u25A0"
                elif not ship.is_drowned:
                    field[field_key] = "*"
                else:
                    field[field_key] = "X"

        for row in range(10):
            for column in range(10):
                print(field[int(str(row) + str(column))], end="  ")
            print(row)
        for column_num in range(10):
            print(column_num, end="  ")

    def __validate_field(self) -> None:
        print(f"Total number of the ships {len(self.field.values())}")
        count_ships = {item: 0 for item in range(1, 5)}
        for ship in self.field.values():
            count_ships[len(ship.decks)] += 1
        for key, value in count_ships.items():
            print(f"{key}-deck ships is {value}")
        self.__validate_ships_neighborhood()

    def __validate_ships_neighborhood(self) -> None:
        all_decks = {}
        for ship_key, ship in self.field.items():
            for deck in ship.decks:
                all_decks[(deck.row, deck.column)] = [
                    (deck.row, deck.column), ship_key
                ]
        valid_ship_list = {}
        for key, value in all_decks.items():
            row, column = key
            neighborhood = [
                all_decks.get((row + delta_r, column + delta_c))
                for delta_r in (-1, 0, 1)
                for delta_c in (-1, 0, 1)
            ]
            for neighbor in neighborhood:
                if neighbor is not None and all_decks[key][1] != neighbor[1]:
                    valid_ship_list[(all_decks[key][1], neighbor[1])] = None
        for key in valid_ship_list.keys():
            print(f"The ships {key[0]} and {key[1]} are very close!")
