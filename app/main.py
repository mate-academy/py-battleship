from typing import Union


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
        self, start: tuple, end: tuple, is_drowned: bool = False
    ) -> None:
        print(start, end)
        self.is_drowned = is_drowned
        self.decks = []
        self.create_decks(start, end)

    def create_decks(self, start: tuple, end: tuple) -> None:
        decks = []
        if start[0] == end[0]:
            for num in range(start[1], end[1] + 1):
                decks.append((start[0], num))
        else:
            for num in range(start[0], end[0] + 1):
                decks.append((num, start[1]))

        for deck in decks:
            self.decks.append(Deck(deck[0], deck[1]))

    def get_deck(self, location: tuple) -> Union[Deck, False]:
        for deck in self.decks:
            if (deck.row, deck.column) == location and deck.is_alive:
                return deck
        return False

    def check_for_alive(self) -> bool:
        return True if any(deck.is_alive for deck in self.decks) else False


class Battleship:
    def __init__(self, ships: list[tuple[tuple]]) -> None:
        self.field = {}
        self.add_ships_to_the_field(ships)

    def add_ships_to_the_field(self, ships: list[tuple[tuple]]) -> None:
        for ship_start, ship_end in ships:
            ship = Ship(ship_start, ship_end)
            for deck in ship.decks:
                self.field[deck.row, deck.column] = ship

    def fire(self, location: tuple) -> str:
        if ship := self.field.get(location):
            if ship.get_deck(location):
                ship.get_deck(location).is_alive = False
                if ship.check_for_alive():
                    return "Hit!"
                else:
                    return "Sunk!"

        return "Miss!"
