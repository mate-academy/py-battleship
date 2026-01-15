from app.ship import Ship


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = [Ship(ship_tuple[0], ship_tuple[1])
                      for ship_tuple in ships]

    def _validate_field(self) -> None:
        assert len(self.ships) == 10

        sizes = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in self.ships:
            sizes[ship.get_length()] += 1

        assert sizes == {1: 4, 2: 3, 3: 2, 4: 1}

        for ship in self.ships:
            for ship_other in self.ships:
                if ship is not ship_other:
                    assert ship != ship_other

    def fire(self, location: tuple) -> str:
        for ship in self.ships:
            if ship.get_deck(location[0], location[1]) is not None:
                return ship.fire(location[0], location[1])
        return "Miss!"

    def check_ship(self, row: int, column: int) -> str:
        for ship in self.ships:
            if ship.get_deck(row, column) is not None:
                if ship.is_drowned:
                    return "x"
                else:
                    if ship.get_deck(row, column).is_alive:
                        return u"\u25A1"
                    return "*"
        return "~"

    def print_field(self) -> None:
        for x_cord in range(10):
            line = ""
            for y_cord in range(10):
                line += self.check_ship(x_cord, y_cord) + " "
            print(line)
