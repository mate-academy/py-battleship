class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        self.create_ship()

    def create_ship(self):
        if self.start[0] == self.end[0]:
            for i in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], i))
        else:
            for i in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(i, self.start[1]))

    def get_deck(self, row, column):
        for deck in self.decks:
            if deck.row == row:
                if deck.column == column:
                    return deck

    def fire(self, row, column):
        deck = self.get_deck(row, column)
        deck.is_alive = False
        hit_counter = 0
        for deck in self.decks:
            if deck.is_alive is False:
                hit_counter += 1
        if hit_counter == len(self.decks):
            self.is_drowned = True
        return self


class Battleship:
    def __init__(self, ships: list):
        self.field = {}
        for ship in ships:
            some_ship = Ship(ship[0], ship[1])
            for deck in some_ship.decks:
                self.field[tuple[deck.row, deck.column]] = some_ship

    def fire(self, location: tuple):
        ship = self.field.get(tuple[location[0], location[1]], "Miss!")
        if ship != "Miss!":
            ship.fire(location[0], location[1])
            if ship.is_drowned is False:
                return "Hit!"
            return "Sunk!"
        return "Miss!"

    def print_field(self):
        problems = self._validate_field()
        if len(problems) > 0:
            print("Field is not validate because:")
            for problem in problems:
                print(problem)
            return None
        for i in range(0, 10):
            line = ""
            for j in range(0, 10):
                ship = self.field.get(tuple[i, j], "0")
                if isinstance(ship, Ship):
                    if ship.is_drowned is True:
                        line += "X"
                    if ship.is_drowned is False:
                        deck = ship.get_deck(i, j)
                        if deck.is_alive is False:
                            line += "*"
                        line += "\u25A1"
                else:
                    line += "~"
            print(line)

    def _validate_field(self):
        ships_links = [ship for ship in self.field.values()]
        ships = set(ships_links)
        problems = []
        if len(ships) != 10:
            problem = f"The total number of the ships " \
                      f"should be 10. You have {len(ships)}"
            problems.append(problem)
        ships_types = {}
        for ship in ships:
            name = "deck_" + str(len(ship.decks))
            ships_types[name] = ships_types.get(name, 0) + 1
        for k, v in ships_types.items():
            if k == "deck_1":
                if v != 4:
                    problem = f"There should be 4 single-deck ships. " \
                              f"You have {v}"
                    problems.append(problem)
            if k == "deck_2":
                if v != 3:
                    problem = f"There should be 3 double-deck ships. " \
                              f"You have {v}"
                    problems.append(problem)
            if k == "deck_3":
                if v != 2:
                    problem = f"There should be 2 three-deck ships. " \
                              f"You have {v}"
                    problems.append(problem)
            if k == "deck_4":
                if v != 1:
                    problem = f"There should be 1 four-deck ship. You have {v}"
                    problems.append(problem)
        must_be_empty = []
        for ship in ships:
            if ship.start[0] == ship.end[0]:
                must_be_empty.append(tuple[ship.start[0], ship.start[1] - 1])
                must_be_empty.append(tuple[ship.end[0], ship.end[1] + 1])
                for i in range(ship.start[1], ship.end[1] + 1):
                    must_be_empty.append(tuple[ship.start[0] - 1, i])
                    must_be_empty.append(tuple[ship.start[0] + 1, i])
            else:
                must_be_empty.append(tuple[ship.start[0] - 1, ship.start[1]])
                must_be_empty.append(tuple[ship.end[0] + 1, ship.end[1]])
                for i in range(ship.start[0], ship.end[0] + 1):
                    must_be_empty.append(tuple[i, ship.start[1] - 1])
                    must_be_empty.append(tuple[i, ship.start[1] - 1])
        for position in must_be_empty:
            if position in self.field.keys():
                problem = "Ships shouldn't be located in the neighboring cells"
                problems.append(problem)
                break
        return problems
