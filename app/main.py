class Deck:
    def __init__(self, row: int, column: int, is_alive=True):
        self.row = row
        self.column = column
        self.location = (self.row, self.column)
        self.is_alive = is_alive

    def __repr__(self):
        return f"Deck_obj: {self.location}"


class Ship:
    def __init__(self, start: tuple, end: tuple, is_drowned=False):
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.is_horizontal = False
        self.is_vertical = False
        self.is_one_deck = False
        self.decks = []

        if self.start == self.end:
            self.is_one_deck = True

        elif self.start[0] == self.end[0] and self.start[1] < self.end[1]:
            self.is_horizontal = True

        elif self.start[1] == self.end[1] and self.start[0] < self.end[0]:
            self.is_vertical = True

        if self.is_horizontal:
            for i in range(self.start[1], self.end[1] + 1):
                self.decks.append(Deck(self.start[0], i))

        elif self.is_vertical:
            for j in range(self.start[0], self.end[0] + 1):
                self.decks.append(Deck(j, self.start[1]))

        else:
            self.decks.append(Deck(self.start[0], self.start[1]))

    def __repr__(self):
        return f"{self.decks}"

    def get_deck(self, row, column):
        for deck in self.decks:

            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int):
        ship_deck = self.get_deck(row, column)
        ship_deck.is_alive = False
        decks_status = [deck.is_alive for deck in self.decks]

        if any(decks_status) is False:
            self.is_drowned = True
            return "Sunk!"


class Battleship:
    def __init__(self, ships: list[tuple]):
        self.field = {ship: Ship(ship[0], ship[1])for ship in ships}
        self.battlefield = [["\u301C" for _ in range(10)] for _ in range(10)]
        self._validate_field()

    def fire(self, location: tuple):
        result = None

        for ship in self.field.values():
            for deck in ship.decks:

                if deck.row == location[0] and deck.column == location[1]:
                    if ship.fire(location[0], location[1]):
                        return ship.fire(location[0], location[1])

                    else:
                        return "Hit!"

                else:
                    result = "Miss!"

        return result

    def show(self):
        for ship in self.field.values():
            for deck in ship.decks:

                if deck.is_alive:
                    self.battlefield[deck.row][deck.column] = "\U0001F6A2"

                else:
                    self.battlefield[deck.row][deck.column] = "\U0001F525"

                if ship.is_drowned:
                    self.battlefield[deck.row][deck.column] = "\U0000274C"

        rows = [f"|{i}|" for i in range(10)]
        print("| |  " + " ⦙⦙⦙ ".join(rows))

        for index, element in enumerate(self.battlefield):
            print(f"|{index}|  " + "     ".join(element) + "\n")

    def _validate_field(self):
        counter = {}.fromkeys((i for i in range(1, 5)), 0)
        for ship in self.field.values():

            if len(ship.decks) == 4:
                counter[4] += 1

            elif len(ship.decks) == 3:
                counter[3] += 1

            elif len(ship.decks) == 2:
                counter[2] += 1

            elif len(ship.decks) == 1:
                counter[1] += 1

        if len(self.field) > 10:
            raise Exception(f"Total ships count must be 10."
                            f"You have: {len(self.field)}")

        if counter != {1: 4, 2: 3, 3: 2, 4: 1}:
            raise Exception(f"Ships with wrong deck count.\n"
                            f"Must be:             You have:\n"
                            f"singe-deck: 4        singe-deck: {counter[1]}\n"
                            f"double-deck: 3       double-deck: {counter[2]}\n"
                            f"three-deck: 2        three-deck: {counter[3]}\n"
                            f"four-deck: 1         four-deck: {counter[4]}")
