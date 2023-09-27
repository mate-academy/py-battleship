def validate_field(self) -> bool:
    total_ship = 0
    single_ship = 0
    double_ship = 0
    three_ship = 0
    four_ship = 0

    for ship in self.ships:
        total_ship += 1
        deck_count = len(ship.decks)
        if deck_count == 1:
            single_ship += 1
        elif deck_count == 2:
            double_ship += 1
        elif deck_count == 3:
            three_ship += 1
        elif deck_count == 4:
            four_ship += 1

    if total_ship != 10:
        print("The total number of ships does not correspond 10")
    if single_ship != 4:
        print("The number of single-deck ships is incorrect")
    if double_ship != 3:
        print("The number of double-deck ships is incorrect")
    if three_ship != 2:
        print("The number of three-deck ships is incorrect")
    if four_ship != 1:
        print("The number of four-deck ships is incorrect")

    for ship in self.ships:
        for deck in ship.decks:
            for i in range(max(0, deck[0] - 1), min(deck[0] + 2, len(self.field))):
                for j in range(max(0, deck[1] - 1), min(deck[1] + 2, len(self.field[0]))):
                    if (i != deck[0] or j != deck[1]) and self.field[i][j] is not None:
                        print("The ships are located nearby!")

    print("Ships are placed correctly!")
