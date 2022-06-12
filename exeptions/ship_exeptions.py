class FieldLocations(Exception):
    pass


class ShipLocations(FieldLocations):
    def __str__(self):
        return "The deck of a ship shouldn't touch the deck of another ship."


class ShipsCounts(FieldLocations):
    def __str__(self):
        return "You should have 10 ships."


class ShipsByDecks(FieldLocations):
    def __str__(self):
        return "You should have 4 single-deck ships, 3 double-deck " \
               "ships, 2 three-deck ships, 1 four-deck ship."
