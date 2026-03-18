class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
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
        coordinates = {}
        if start[0] == end[0]:
            for i in range(start[1], end[1] + 1):
                coordinates[(start[0], i)] = Deck(start[0], i)
        if start[1] == end[1]:
            for i in range(start[0], end[0] + 1):
                coordinates[(i, start[1])] = Deck(i, start[1])
        self.coordinates = coordinates
        self.is_drowned = is_drowned
        print(self.coordinates)

    def get_deck(self, row: int, column: int) -> None:
        # Find the corresponding deck in the list
        pass

    def fire(self, row: int, column: int) -> None:
        self.coordinates[(row, column)].is_alive = False
        if all(deck.is_alive is False for deck in self.coordinates.values()):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list) -> None:
        field_dict = {}
        ship_dict = {}
        for i in range(len(ships)):
            ship_dict[i] = Ship(ships[i][0], ships[i][1])
            for coordinates in ship_dict[i].coordinates:
                field_dict[coordinates] = ship_dict[i]
        self.field = field_dict

    def fire(self, location: tuple) -> str:
        if location in self.field:
            self.field[location].fire(location[0], location[1])
            if self.field[location].is_drowned:
                return "Sunk!"
            else:
                return "Hit!"
        else:
            return "Miss!"
