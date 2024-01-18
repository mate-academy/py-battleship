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


class Ship:

    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        # Create decks and save them to a list `self.decks`

        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = [
            Deck(row, column)
            for row in range(start[0], end[0] + 1)
            for column in range(start[1], end[1] + 1)
        ]
        self.live_decks = len(self.decks)

    def get_deck(
            self,
            row: int,
            column: int
    ) -> Deck:
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def fire(
            self,
            row: int,
            column: int
    ) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed

        wrecked_deck = self.get_deck(row, column)

        if wrecked_deck is not None:
            wrecked_deck.is_alive = False

        if all(deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:

    def __init__(
            self,
            ships: list
    ) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it

        self.field = {ship: Ship(ship[0], ship[1]) for ship in ships}

    def fire(
            self,
            location: tuple
    ) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.

        for ship in self.field.values():
            for deck in ship.decks:
                if (deck.row, deck.column) == location:
                    deck.is_alive = False
                    ship.live_decks -= 1
                    if ship.live_decks == 0:
                        ship.is_drowned = True
                        return "Sunk!"
                    return "Hit!"
        return "Miss!"
