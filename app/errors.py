class NumberOfShipsError(Exception):
    """number of ships should be 10."""
    pass


class CountShipsDecks(Exception):
    """number of ships with corresponding number of decks
     should be 4 for 1 deck, 3 for 2 decks, 2 for 3 decks,
     1 for 4 decks """
    pass


class SpaceBetweenShips(Exception):
    """there must be space between the ships."""
    pass


class FleetError(Exception):
    """all errors in Battleship"""
    pass
