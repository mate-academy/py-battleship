from app.ship import Ship


def create_field(fleet: list[Ship]) -> dict:
    battle_ships_dict = dict()
    for battle_ship in fleet:
        for deck in battle_ship.decks:
            battle_ships_dict[(deck.row, deck.column)] = battle_ship
    return battle_ships_dict
