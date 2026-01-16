class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False
                 ) -> None:

        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        if self.start == self.end:
            self.decks.append(Deck(row=self.start[0],
                                   column=self.start[1]))
            return
        if self.start[0] == self.end[0]:
            for num in range(self.start[1], self.end[1] + 1):
                self.decks.append(
                    Deck(row=self.start[0],
                         column=num))
        else:
            for num in range(self.start[0], self.end[0] + 1):
                self.decks.append(
                    Deck(row=num,
                         column=self.start[1]))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        deck.is_alive = False
        for deck in self.decks:
            if deck.is_alive:
                return
        self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        self._validate_input()
        for ship in ships:
            ship = Ship(start=ship[0], end=ship[1])
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        if location not in self.field.keys():
            return "Miss!"
        ship = self.field[location]
        ship.fire(location[0], location[1])
        if not ship.is_drowned:
            return "Hit!"
        return "Sunk!"

    def _validate_input(self) -> None:
        ships = set(self.field.values())
        if len(ships) > 10:
            raise Exception("The total number of the ships should be 10")
        if len(ships) == 10:
            dec_count = {1: 0, 2: 0, 3: 0, 4: 0}
            for ship in ships:
                dec_count[len(ship.decks)] += 1
            limit = 4
            for key, value in dec_count.items():
                if key != limit:
                    raise Exception("Check number of ships "
                                    "or decks of the ships")
                limit -= 1

    def print_field(self) -> list:
        battle_field = [["~" for _ in range(10)] for _ in range(10)]
        for deck in self.field.keys():
            battle_field[deck[0]][deck[1]] = "□"
        for ship in set(self.field.values()):
            for deck_ in ship.decks:
                if not deck_.is_alive and ship.is_drowned is False:
                    battle_field[deck_.row][deck_.column] = "*"
                if not deck_.is_alive and ship.is_drowned is True:
                    battle_field[deck_.row][deck_.column] = "x"
        for row in battle_field:
            for element in row:
                print(element, "   ", end=" ")
            print("\n")
        return battle_field
