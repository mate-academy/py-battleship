class ShipsValidator:
    def __get__(self, instance: object, owner: object) -> list:
        return instance._ships

    def __set__(self, instance: object, ships: list) -> None:
        self._amount_ships_validator(ships)
        self._distance_between_ships_validator(ships)
        instance._ships = ships

    @staticmethod
    def _amount_ships_validator(ships: list) -> None:

        amount_of_the_ships = {
            "ships with one deck": 0,
            "ships with two decks": 0,
            "ships with tree decks": 0,
            "ships with four decks": 0
        }

        for ship in ships:
            if len(ship.decks) == 1:
                amount_of_the_ships["ships with one deck"] += 1
            elif len(ship.decks) == 2:
                amount_of_the_ships["ships with two decks"] += 1
            elif len(ship.decks) == 3:
                amount_of_the_ships["ships with tree decks"] += 1
            elif len(ship.decks) == 4:
                amount_of_the_ships["ships with four decks"] += 1
            else:
                raise ValueError("The ship is too big!")

        amount_of_the_decks = 4
        for ship, amount in amount_of_the_ships.items():
            if amount != amount_of_the_decks:
                raise ValueError(f"There should be {amount_of_the_decks} "
                                 f"{ship}")
            amount_of_the_decks -= 1

    @staticmethod
    def _distance_between_ships_validator(value: list) -> None:
        free_area = []
        ships_area = []

        for ship in value:
            for deck in ship.decks:
                x, y = deck.row, deck.column
                ships_area.append((x, y))

        for ship in value:
            for deck in ship.decks:
                x, y = deck.row, deck.column
                if ((x, y - 1) not in free_area
                        and (x, y - 1) not in ships_area):
                    free_area.append((x, y - 1))
                if ((x - 1, y - 1) not in free_area
                        and (x - 1, y - 1) not in ships_area):
                    free_area.append((x - 1, y - 1))
                if ((x - 1, y) not in free_area
                        and (x - 1, y) not in ships_area):
                    free_area.append((x - 1, y))
                if ((x - 1, y + 1) not in free_area
                        and (x - 1, y + 1) not in ships_area):
                    free_area.append((x - 1, y + 1))
                if ((x, y + 1) not in free_area
                        and (x, y + 1) not in ships_area):
                    free_area.append((x, y + 1))
                if ((x + 1, y + 1) not in free_area
                        and (x + 1, y + 1) not in ships_area):
                    free_area.append((x + 1, y + 1))
                if ((x + 1, y) not in free_area
                        and (x + 1, y) not in ships_area):
                    free_area.append((x + 1, y))
                if ((x + 1, y - 1) not in free_area
                        and (x + 1, y - 1) not in ships_area):
                    free_area.append((x + 1, y - 1))

        for ship in value:
            for deck in ship.decks:
                x, y = deck.row, deck.column
                if (x, y) in free_area:
                    raise ValueError("The ships are too close")


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple[int], end: tuple[int],
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        if self.start[0] == self.end[0]:
            self.decks = [Deck(self.start[0], num)
                          for num in range(self.start[1], self.end[1] + 1)]
        else:
            self.decks = [Deck(num, self.start[1])
                          for num in range(self.start[0], self.end[0] + 1)]

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        deck.is_alive = False

        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"


class Battleship:
    ships = ShipsValidator()

    def __init__(self, ships: list[tuple]) -> None:
        self.ships = [Ship(*ship) for ship in ships]
        self.field = {tuple((deck.row, deck.column)
                      for deck in ship.decks): ship
                      for ship in self.ships}

    def fire(self, location: tuple) -> str:
        for coordinates, ship in self.field.items():
            if location in coordinates:
                return ship.fire(*location)
        return "Miss!"
