class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = {}
        self.single_deck_ships = {}
        self.double_deck_ships = [{}, {}, {}]
        self.three_deck_ships = [{}, {}]
        self.four_deck_ships = {}

        for ship in ships:
            if ship[0] == ship[1]:
                self.single_deck_ships.update({ship[0]: u"\u25A1"})
                self.field.update({ship[0]: u"\u25A1"})

            if ship[1][1] == ship[0][1] + 1 or ship[1][0] == ship[0][0] + 1:
                for i in range(len(self.double_deck_ships)):
                    if len(self.double_deck_ships[i]) < 2:
                        self.double_deck_ships[i] = (
                            self.double_deck_ships[i].fromkeys(ship, u"\u25A1")
                        )
                        break
            if ship[1][1] == ship[0][1] + 2:
                list_three_deck = list(ship)
                list_three_deck.append((ship[0][0], ship[0][1] + 1))
                ship = tuple(list_three_deck)
                for i in range(len(self.three_deck_ships)):
                    if len(self.three_deck_ships[i]) < 3:
                        self.three_deck_ships[i] = (
                            self.three_deck_ships[i].fromkeys(ship, u"\u25A1")
                        )
                        break
            if ship[1][0] == ship[0][0] + 2:

                list_three_deck = list(ship)
                list_three_deck.append((ship[0][0] + 1, ship[0][1]))
                ship = tuple(list_three_deck)
                for i in range(len(self.three_deck_ships)):
                    if len(self.three_deck_ships[i]) < 3:
                        self.three_deck_ships[i] = (
                            self.three_deck_ships[i].fromkeys(ship, u"\u25A1")
                        )
                        break
            if ship[1][1] == ship[0][1] + 3:
                list_four_deck = list(ship)
                list_four_deck.append((ship[0][0], ship[0][1] + 1))
                list_four_deck.append((ship[0][0], ship[0][1] + 2))
                ship = tuple(list_four_deck)

                self.four_deck_ships = self.four_deck_ships.fromkeys(
                    ship,
                    u"\u25A1"
                )
            if ship[1][0] == ship[0][0] + 3:
                list_four_deck = list(ship)
                list_four_deck.append((ship[0][0] + 1, ship[0][1]))
                list_four_deck.append((ship[0][0] + 2, ship[0][1]))
                ship = tuple(list_four_deck)
                self.four_deck_ships = self.four_deck_ships.fromkeys(
                    ship,
                    u"\u25A1"
                )
        self.field.update(self.single_deck_ships)
        self.field.update(self.four_deck_ships)
        for double_deck in self.double_deck_ships:
            self.field.update(double_deck)
        for three_deck in self.three_deck_ships:
            self.field.update(three_deck)
        print(self.field)

    def fire(self, location: tuple) -> str:

        list_all_ships = [self.four_deck_ships]
        for double_deck in self.double_deck_ships:
            list_all_ships.append(double_deck)
        for three_deck in self.three_deck_ships:
            list_all_ships.append(three_deck)

        if location in self.single_deck_ships.keys():
            self.single_deck_ships[location] = "x"
            self.field[location] = "x"
            return "Sunk!"
        for deck in list_all_ships:
            if location in deck.keys():
                deck[location] = "*"
                self.field[location] = "*"
                if u"\u25A1" in deck.values():
                    return "Hit!"
                else:
                    for key in deck.keys():
                        deck[key] = "x"
                        self.field[key] = "x"
                    return "Sunk!"
        return "Miss!"

    def print_field(self) -> None:
        board = [["~"] * 10 for _ in range(10)]
        for row, column in self.field:
            board[row][column] = self.field[(row, column)]
        for row in board:
            print("   ".join(row))

    def _validate_field(self) -> None:
        if len(self.field) // 2 != 10:
            raise "There should be 10 ships"
        if len(self.single_deck_ships) != 4:
            raise "There should be 4 single-deck ships"
        if len(self.double_deck_ships) // 2 != 3:
            raise "There should be 3 double-deck ships"
        if len(self.three_deck_ships) // 3 != 2:
            raise "There should be 2 three-deck ships"
        if len(self.four_deck_ships) // 4 != 1:
            raise "There should be 1 four-deck ships"
