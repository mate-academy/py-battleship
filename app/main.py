from app.naval_battlefield import NavalBattlefield
from app.shipyard import build_battleships
from app.number_of_ships import check_number_of_ships
from app.ships_neighboring import are_ships_separated
from app.bounding_ships_and_decks import create_field


class Battleship:
    """# Create a dict `self.field`.
    Its keys are tuples - the coordinates of the non-empty cells,
    A value for each cell is a reference to the ship which is located in it"""
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = ships
        self.battle_field = NavalBattlefield()
        self.fleet = build_battleships(self.ships)
        self.field = create_field(self.fleet)

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError("The total number of the ships should be 10")
        check_number_of_ships(self.fleet)
        are_ships_separated(self.ships)

    def print_field(self) -> None:
        for coordinates, ship in self.field.items():
            row, column = coordinates
            print(row, column, ship)
            self.battle_field.grid[row][column] = u"\u25A1"
            for deck in ship.decks:
                print(deck.row, deck.column, deck.is_alive)
                if ship.is_drowned is True:
                    self.battle_field.grid[row][column] = "x"
                elif deck.is_alive is not True:
                    self.battle_field.grid[deck.row][deck.column]\
                        = "*"
        for element in self.battle_field.grid:
            line = "   ".join(element)
            print(line)

    def fire(self, location: tuple) -> str:
        """This function should check whether the location
        is a key in the `self.field`
        If it is, then it should check if this cell
        is the last alive in the ship or not."""
        if location not in self.field:
            return "Miss!"
        elif location in self.field:
            row, column = location
            self.field[location].fire(row, column)
            if not self.field[location].is_drowned:
                return "Hit!"
            return "Sunk!"
