from typing import Any


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def got_hit(self) -> None:
        self.is_alive = False


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False
                 ) -> None:
        # Create decks and save them to a list `self.decks`
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        self.length = len(self.decks)
        if self.start[0] == self.end[0]:
            for num in range(self.start[1], self.end[1] + 1):
                deck = Deck(self.start[0], num)
                self.decks.append(deck)
                self.length += 1
        else:
            for num in range(self.start[0], self.end[0] + 1):
                deck = Deck(num, self.start[1])
                self.decks.append(deck)
                self.length += 1

    def get_deck(self, row: int, column: int) -> Deck:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck_to_hit = self.get_deck(row, column)
        deck_to_hit.got_hit()
        count_hit_decks = 0
        for deck in self.decks:
            if deck.is_alive is False:
                count_hit_decks += 1
        if count_hit_decks == len(self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: Any) -> None   :
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}
        self.list_of_ships = []
        for ship in ships:
            created_ship = Ship(ship[0], ship[1])
            self.list_of_ships.append(created_ship)
            for deck in created_ship.decks:
                self.field[deck.row, deck.column] = created_ship

    def _validate_field(self) -> None:
        if len(self.list_of_ships) != 10:
            print("The total number of the ships should be 10.")
        dict_of_lengths = {"single-deck": 4,
                           "double-deck": 3,
                           "three-deck": 2,
                           "four-deck": 1}
        list_of_lengths = []
        prohibited_filed_list = []
        for ship in self.list_of_ships:
            list_of_lengths.append(ship.length)
            for line in range(ship.start[0] - 1, ship.end[0] + 2):
                for column in range(ship.start[1] - 1, ship.end[1] + 2):
                    prohibited_filed_list.append((line, column))

        single_deck = dict_of_lengths.get("single-deck")
        double_deck = dict_of_lengths.get("double-deck")
        three_deck = dict_of_lengths.get("three-deck")
        four_deck = dict_of_lengths.get("four-deck")
        if list_of_lengths.count(single_deck) != single_deck:
            print(f"The amount of single-deck ships is not correct, "
                  f"it should be {single_deck}.")
        elif list_of_lengths.count(double_deck) != double_deck:
            print(f"The amount of double_deck ships is not correct, "
                  f"it should be {double_deck}.")
        elif list_of_lengths.count(three_deck) != three_deck:
            print(f"The amount of three_deck ships is not correct, "
                  f"it should be {three_deck}.")
        elif list_of_lengths.count(four_deck) != four_deck:
            print(f"The amount of four_deck ships is not correct, "
                  f"it should be {four_deck}.")

        for cell in self.field:
            if cell in prohibited_filed_list:
                print("Ships shouldn't be located in the neighboring cells.")
                break

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if location in self.field.keys():
            ship = self.field.get(location)
            ship.fire(location[0], location[1])
            if ship.is_drowned is True:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        for line in range(10):
            for cell in range(10):
                cell_to_check = (line, cell)
                if cell_to_check in self.field.keys():
                    ship = self.field.get(cell_to_check)
                    deck = ship.get_deck(line, cell)
                    if deck.is_alive:
                        print("□", end=" ")
                    elif ship.is_drowned:
                        print("x", end=" ")
                    else:
                        print("*", end=" ")
                else:
                    print("~", end=" ")
            print("\n")
