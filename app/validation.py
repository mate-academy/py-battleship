from app.errors import LocationError, QuantityError, DeckError


def validate_field(ships: list) -> list:
    try:
        if len(ships) != 10:
            raise QuantityError
    except QuantityError:
        print("Should be 10 ships")
    else:
        four_deck = 0
        three_deck = 0
        double_deck = 0
        single_deck = 0
        try:
            for ship in ships:
                if (ship[0][0] != ship[1][0]
                        and ship[0][1] != ship[1][1]):
                    raise LocationError
                if ship[0][0] == ship[1][0]:
                    cell_number = abs(ship[0][1] - ship[1][1])
                else:
                    cell_number = abs(ship[0][0] - ship[1][0])
                if cell_number > 3:
                    raise DeckError
                if cell_number == 3:
                    four_deck += 1
                if cell_number == 2:
                    three_deck += 1
                if cell_number == 1:
                    double_deck += 1
                if cell_number == 0:
                    single_deck += 1
                if (single_deck > 4
                        or double_deck > 3
                        or three_deck > 2
                        or four_deck > 1):
                    raise QuantityError
        except LocationError:
            print("Ships must be located in rows and columns")
        except DeckError:
            print("Ship must contain maximum 4 decks")
        except QuantityError:
            print("Too much of this type of boats")
        else:
            return ships
