from typing import Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        is_drowned: bool = False
    ) -> None:
        """
        # Create decks and save them to a list `self.decks`
        """
        self.is_drowned = is_drowned
        self.start = start
        self.end = end
        self.decks = []

        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        """
        # Find the corresponding deck in the list
        """
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        """
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        """
        if self.decks is not None:
            ruin_deck = self.get_deck(row, column)
            ruin_deck.is_alive = False

            if ruin_deck in self.decks:
                count_hit = 0
                for deck in self.decks:
                    if not deck.is_alive:
                        count_hit += 1

                if count_hit == len(self.decks):
                    self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple[tuple]]) -> None:
        """
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        """
        self.fields = {}
        for ship in ships:
            self.ship = Ship(ship[0], ship[1])
            for deck in self.ship.decks:
                self.fields[deck.row, deck.column] = self.ship

    def fire(self, location: tuple[int, int]) -> str:
        """
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        """
        if location not in self.fields:
            return "Miss!"
        else:
            self.fields[location].fire(location[0], location[1])
            if self.fields[location].is_drowned:
                return "Sunk!"
            return "Hit!"
