from typing import Union


class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True
                 ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False
                 ) -> None:
        self.decks = [Deck(row=row, column=column)
                      for row in range(start[0], end[0] + 1)
                      for column in range(start[1], end[1] + 1)]
        self.is_drowned = is_drowned

    def get_deck(self,
                 row: int,
                 column: int
                 ) -> Union[Deck, None]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self,
             row: int,
             column: int
             ) -> None:
        target_deck = self.get_deck(row, column)
        target_deck.is_alive = False
        is_drowned = True
        if any([deck.is_alive for deck in self.decks]):
            is_drowned = False
        self.is_drowned = is_drowned


class Battleship:
    def __init__(self,
                 ships: tuple
                 ) -> None:
        self.ships = (Ship(start, end) for start, end in ships)
        self.field = {
            (deck.row, deck.column): ship
            for ship in self.ships
            for deck in ship.decks
        }

    def fire(self,
             location: tuple
             ) -> str:
        ship = self.field.get(location)
        if ship:
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
