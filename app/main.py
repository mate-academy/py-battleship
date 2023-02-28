from dataclasses import dataclass


@dataclass
class Deck:
    row: int
    col: int
    is_alive: bool = True


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:

        self.is_drowned: bool = is_drowned
        self.deck_cells = self.create_ship_cells(start, end)

    def create_ship_cells(self, first_cell: tuple, last_cell: tuple) -> list:
        ship_cells = []
        if first_cell[0] == last_cell[0]:
            for col in range(first_cell[1], last_cell[1] + 1):
                ship_cells.append(Deck(first_cell[0], col))
        else:
            for row in range(first_cell[0], last_cell[0] + 1):
                ship_cells.append(Deck(row, first_cell[1]))

        return ship_cells

    def get_deck(self, row: int, column: int) -> Deck:

        for cell in self.deck_cells:
            if cell.row == row and cell.col == column:
                return cell

    def fire(self, row: int, col: int) -> None:

        cell = self.get_deck(row, col)
        cell.is_alive = False
        if all(not cell.is_alive for cell in self.deck_cells):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:

        self.field = self.create_ships(ships)

    def create_ships(self, ships: list[tuple]) -> dict[tuple, Ship]:
        field = {}
        for first_cell, last_cell in ships:
            ship = Ship(first_cell, last_cell)
            key = tuple([(self.cell.row, self.cell.col)
                         for self.cell in ship.deck_cells])
            field[key] = ship

        return field

    def fire(self, location: tuple) -> str:

        for hit_box, ship in self.field.items():
            if location in hit_box:
                ship.fire(location[0], location[1])
                if ship.is_drowned:
                    return "Sunk!"
                return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        deck = ""
        ship_location = {
            location: ship
            for locations, ship in self.field.items()
            for location in locations
        }
        for row in range(10):
            for col in range(10):
                if (row, col) in ship_location:
                    ship = ship_location[row, col]
                    if ship.is_drowned:
                        deck += "✓"
                    else:
                        cell = ship.get_deck(row, col)
                        if cell.is_alive:
                            deck += "□"
                        else:
                            deck += "*"
                else:
                    deck += "~"
                if col == 9:
                    deck += "\n"
        print(deck)
