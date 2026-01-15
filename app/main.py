from __future__ import annotations


class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple[int],
                 end: tuple[int],
                 is_drowned: bool = False) -> None:
        self.is_drowned = is_drowned
        self.decks = self.get_decks(start, end)

    @staticmethod
    def get_decks(start: tuple[int], end: tuple[int]) -> list[Deck]:
        decks = []
        if start[0] != end[0]:
            for x_pos in range(start[0], end[0] + 1):
                decks.append(Deck(x_pos, start[1]))
        elif start[1] != end[1]:
            for y_pos in range(start[1], end[1] + 1):
                decks.append(Deck(start[0], y_pos))
        else:
            decks.append(Deck(start[0], end[1]))
        return decks

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        if self.get_deck(row, column):
            self.get_deck(row, column).is_alive = False
        self.is_drowned = all(not deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}
        for ship in ships:
            cell = Ship(ship[0], ship[1])
            if ship[0][0] != ship[1][0]:
                for x_pos in range(ship[0][0], ship[1][0] + 1):
                    self.field[(ship[0][1], x_pos)] = cell
            if ship[0][1] != ship[1][1]:
                for y_pos in range(ship[0][1], ship[1][1] + 1):
                    self.field[(ship[0][0], y_pos)] = cell
            else:
                self.field[ship[0]] = cell

    def fire(self, location: tuple[int]) -> str:
        if location not in self.field:
            return "Miss!"
        self.field[location].fire(location[0], location[1])
        if self.field[location].is_drowned:
            return "Sunk!"
        return "Hit!"
