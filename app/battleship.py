from app.ship import Ship


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.field = {}
        for ship in ships:
            start, end = ship
            new_ship = Ship(start, end)
            for deck in new_ship.decks:
                self.field[(deck.row, deck.column)] = new_ship

    def fire(self, location: tuple[int, int]) -> str:
        if location in self.field:
            ship = self.field[location]
            if ship.fire(location[0], location[1]):
                if ship.is_drowned:
                    return "Sunk!"
                else:
                    return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(10):
            line = ""
            for col in range(10):
                if (row, col) in self.field:
                    ship = self.field[(row, col)]
                    if ship.get_deck(row, col).is_alive:
                        line += "□"
                    else:
                        line += "x"
                else:
                    line += "~"
            print(line)

    def _validate_field(self) -> None:
        ship_sizes = [len(ship.decks) for ship in self.field.values()]
        one_deck_ships = ship_sizes.count(1)
        two_deck_ships = ship_sizes.count(2)
        three_deck_ships = ship_sizes.count(3)
        four_deck_ships = ship_sizes.count(4)

        if one_deck_ships != 4 or two_deck_ships != 3 or three_deck_ships != 2 or four_deck_ships != 1: # noqa E501
            raise ValueError("Невірна кількість кораблів!")

        for (row, col), ship in self.field.items():
            for (other_row, other_col), other_ship in self.field.items():
                if ship != other_ship and abs(row - other_row) <= 1 and abs(col - other_col) <= 1: # noqa E501
                    raise ValueError(
                        "Кораблі не повинні бути в сусідніх клітинках!"
                    )
