class Deck:
    counter = 0

    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive
        
    def __repr__(self) -> str:
        return f"Deck: {self.row} : {self.column}"

    def __str__(self) -> str:
        return f"Deck: {self.row} : {self.column}"


class Ship:

    def __init__(self, start: tuple, end: tuple, is_drowned=False):
        self.decks = self._decks_generator(start, end)
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> bool:
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.is_alive = False
        decks_available = [deck for deck in self.decks if deck.is_alive]
        if not decks_available:
            self.is_drowned = True    
        

    @staticmethod
    def _decks_generator(start: tuple, end: tuple) -> list:
        start_row, start_column = start
        end_row, end_column = end
        if start_row == end_row:
            return [Deck(start_row, column)
                    for column in range(start_column, end_column + 1)]
        return [Deck(row, start_column)
                for row in range(start_row, end_row + 1)]


class Battleship:

    def __init__(self, ships):
        self.field = self.get_field(ships)
        self.draw_playfield()

    def _validate_fields(self) -> str:
        ships = self.field.values() 
        if set(ships) != 10:
            return "10 ships should be in battle"

        single, double, three, four = 0, 0, 0, 0
        for ship in set(ships):
            if len(ship.decks) == 1:
                single += 1
            if len(ship.decks) == 2:
                double += 1
            if len(ship.decks) == 3:
                three += 1
            if len(ship.decks) == 4:
                four += 1

        if single != 1:
            return "You should have 4 single-deck ships"
        if double != 2:
            return "You should have 3 double-deck ships"
        if three != 3:
            return "You should have 2 three-deck ships"
        if four != 4:
            return "You should have 1 four-deck ships"

    def fire(self, location: tuple):
        ship = self.field.get(location)

        if ship:
            self.field.pop(location)
            row, column = location
            ship.fire(row, column)
            self.playfield[row][column] = "*"
            if ship.is_drowned:
                for deck in ship.decks:
                    self.playfield[deck.row][deck.column] = "x"
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    @staticmethod
    def get_field(ships) -> dict:
        field = {}
        ships = [Ship(start, end) for start, end in ships]
        for ship in ships:

            for deck in ship.decks:
                field[deck.row, deck.column] = ship

        return field

    def draw_playfield(self) -> None:
        self.playfield = [["~" for _ in range(10)] for _ in range(10)]
        for deck in self.field.keys():
            row, column = deck
            self.playfield[row][column] = "□"

        print(self.playfield)
