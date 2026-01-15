from app.ship import Ship


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        self.ships = ships
        for ship in ships:
            self.place_ship(ship)

    def place_ship(self, ship_coords: tuple) -> None:
        ship = Ship(ship_coords[0], ship_coords[1])
        for deck in ship.decks:
            self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for row in range(0, 10):
            output = ""
            for column in range(0, 10):
                ship = self.field.get((row, column))
                if ship:
                    if ship.is_drowned:
                        output += "x "
                    elif ship.get_deck(row, column).is_alive:
                        output += "□ "
                    else:
                        output += "* "
                else:
                    output += "~ "
            print(output)
