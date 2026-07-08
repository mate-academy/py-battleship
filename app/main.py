class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False
                 ) -> None:
        self.is_drowned = is_drowned
        if start[0] == end[0]:
            self.decks = {(start[0], coord): Deck(start[0], coord)
                          for coord
                          in range(start[1], end[1] + 1)}
        elif start[1] == end[1]:
            self.decks = {(coord, start[1]): Deck(coord, start[1])
                          for coord
                          in range(start[0], end[0] + 1)}
        else:
            raise TypeError("Invalid coord")

    def __len__(self) -> int:
        return len(self.decks)

    def __str__(self) -> str:
        return u"\u25A1"

    def fire(self, row: int, column: int) -> None:
        self.decks[(row, column)].is_alive = False
        for deck in self.decks.values():
            if deck.is_alive:
                return
        self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        self._validate_field(ships)
        for ship in ships:
            try:
                if (not isinstance(ship, tuple)
                        or len(ship) != 2
                        or False
                        or ship[0][0] > ship[1][0]
                        or ship[0][1] > ship[1][1]):
                    raise ValueError
            except (ValueError, TypeError):
                raise ValueError("Incorrect data")
        self.field = {(x, y): "~"
                      for x in range(10)
                      for y in range(10)}
        self.list_ships = [Ship(start, end)
                           for (start, end) in ships]
        for ship in self.list_ships:
            for coord in ship.decks:
                self.field[coord] = ship

    def fire(self, location: tuple) -> str:
        if self.field[location] == "~":
            return "Miss!"
        else:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            else:
                return "Hit!"

    @staticmethod
    def _validate_field(ships: list) -> None:
        field = [["~"] * 10 for _ in range(10)]

        def get_info_around(x_coord: int, y_coord: int, value: str) -> bool:
            for index_x in range(3):
                for index_y in range(3):
                    try:
                        if (field[x_coord - 1 + index_x][y_coord - 1 + index_y]
                                not in value):
                            return False
                    except IndexError:
                        continue
            return True

        for coords in ships:
            for coord in coords:
                if ((coord[0] > 9 or coord[0] < 0)
                        or (coord[1] > 9 or coord[1] < 0)):
                    raise ValueError("Ship outside the field")

        count_ships = {1: 0,
                       2: 0,
                       3: 0,
                       4: 0,
                       }
        list_ships = [Ship(start, end) for start, end in ships]
        name_ship = 0

        for ship in list_ships:
            if 1 <= len(ship) <= 4:
                count_ships[len(ship)] += 1
                for x_coord, y_coord in ship.decks:
                    if get_info_around(x_coord, y_coord, "~" + str(name_ship)):
                        field[x_coord][y_coord] = str(name_ship)
                    else:
                        raise ValueError("Ships shouldn't be located "
                                         "in the neighboring cells "
                                         "(even if cells are "
                                         "neighbors by diagonal).")
                name_ship += 1
            else:
                raise ValueError("Inappropriate ship size")

        for len_ship in count_ships:
            if len_ship != 5 - count_ships[len_ship]:
                raise ValueError("The rules are not followed")

    def __str__(self) -> str:
        result = ""
        for index_x in range(10):
            for index_y in range(10):
                if self.field[(index_x, index_y)] == "~":
                    result += "~" + " "
                elif self.field[(index_x, index_y)].is_drowned:
                    result += "x" + " "
                elif self.field[(index_x,
                                 index_y)].decks[(index_x,
                                                  index_y)].is_alive:
                    result += u"\u25A1" + " "
                else:
                    result += "*" + " "
            result += "\n"
        return result
