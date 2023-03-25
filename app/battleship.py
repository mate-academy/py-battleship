from app.ship import Ship


class Battleship:
    def __init__(
            self,
            ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.ships: list[Ship] = []
        self.field = {}

        for ship in ships:
            ship_instance = Ship(ship[0], ship[1])
            self.ships.append(ship_instance)
            for deck in ship_instance.decks:
                self.field[(deck.row, deck.column)] = ship_instance

        self._validate_field()

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field.get(location)
            ship.fire(location[0], location[1])

            if ship.is_drowned:
                return "Sunk!"

            return "Hit!"

        return "Miss!"

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise Exception("Number of ships must be 10")
        if sum(len(ship.decks) for ship in self.ships) != 20:
            raise Exception("There must be 4 single-deck ships, "
                            "3 double-deck ships, 2 three-deck ships "
                            "and 1 four-deck ship")
        for i in range(len(self.ships)):
            ship = self.ships[i]

            for count in range(i + 1, len(self.ships)):

                if len(ship.decks_with_margin_cells.intersection(
                    self.ships[count].decks_cells
                )) != 0:
                    raise Exception("Ships shouldn't be located "
                                    "in the neighboring cells "
                                    "(even if cells are neighbors "
                                    "by diagonal)")

    def print_field(self) -> None:
        field_matrix = []

        for _ in range(10):
            row_items = ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"]
            field_matrix.append(row_items)

        for location in self.field:
            ship = self.field.get(location)

            if ship.is_drowned:
                field_matrix[location[0]][location[1]] = "X"

            else:
                deck = ship.get_deck(location[0], location[1])

                if deck.is_alive:
                    field_matrix[location[0]][location[1]] = u"\u25A1"
                else:
                    field_matrix[location[0]][location[1]] = "*"

        print("\n".join(["".join(["{:4}".format(item) for item in row])
                         for row in field_matrix]))