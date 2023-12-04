from typing import List, Dict


class Deck:
    def __init__(
            self, row: int,
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
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.create_deck()
        self.count_hits = 0

    def create_deck(self) -> List[Deck]:
        decks_for_ship = []
        start_row, start_column = self.start
        end_row, end_column = self.end

        if self.start == self.end:
            one_deck = Deck(self.start[0], self.start[1])
            decks_for_ship.append(one_deck)
            return decks_for_ship

        if start_row == end_row:
            for column in range(start_column, end_column + 1):
                decks_for_ship.append(Deck(start_row, column))

        elif start_column == end_column:
            for row in range(start_row, end_row + 1):
                decks_for_ship.append(Deck(row, start_column))
        return decks_for_ship

    def get_deck(self, row: int, column: int) -> Deck:
        deck = next((
            deck for deck in self.decks
            if deck.row == row and deck.column == column), None
        )
        return deck

    def fire(self, row: int, column: int) -> str:
        message_fire = ""
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                deck.is_alive = False
                message_fire = "Hit!"
                self.count_hits += 1

        if self.count_hits == len(self.decks):
            message_fire = "Sunk!"

        return message_fire


class Battleship:
    def __init__(
            self,
            ships: list[tuple]
    ) -> None:
        self.ships = ships
        self.flot = self.create_flot_ships()
        self.field = self.create_field(self.flot)

    def create_flot_ships(self) -> list[Ship]:
        return [Ship(cell[0], cell[1]) for cell in self.ships]

    @staticmethod
    def create_field(ships: List[Ship]) -> Dict[Deck, Ship]:
        return {
            deck: ship for ship in ships
            for deck in ship.decks
        }

    def fire(self, location: tuple) -> str:
        for deck in self.field:
            if location == (deck.row, deck.column):
                ship = self.field[deck]
                return ship.fire(deck.row, deck.column)
        return "Miss!"
