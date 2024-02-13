from app.ship import Ship


def check_number_of_ships(fleet: list[Ship]) -> None:
    number_of_ships = {"4-decks": 0, "3-decks": 0, "2-decks": 0, "1-deck": 0}
    for ship in fleet:
        if len(ship.decks) == 4:
            number_of_ships["4-decks"] += 1
        elif len(ship.decks) == 3:
            number_of_ships["3-decks"] += 1
        elif len(ship.decks) == 2:
            number_of_ships["2-decks"] += 1
        elif len(ship.decks) == 1:
            number_of_ships["1-deck"] += 1
    if number_of_ships["1-deck"] != 4:
        raise ValueError("There should be 4 single-deck ships")
    elif number_of_ships["2-decks"] != 3:
        raise ValueError("There should be 3 double-deck ships")
    elif number_of_ships["3-decks"] != 2:
        raise ValueError("There should be 2 three-deck ships")
    elif number_of_ships["4-decks"] != 1:
        raise ValueError("There should be 1 four-deck ship")
