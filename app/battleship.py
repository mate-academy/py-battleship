from app.deck import Deck
from app.ship import Ship


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.fields = {}

        for start, end in ships:
            ship = Ship(start, end)
            if start[0] == end[0]:
                for cor in range(start[1], end[1] + 1):
                    cor_of_field = (start[0], cor)
                    self.fields[cor_of_field] = ship
            else:
                for cor in range(start[0], end[0] + 1):
                    cor_of_field = (cor, start[1])
                    self.fields[cor_of_field] = ship

    def print_field(self) -> None:
        cor_of_rows = []

        for row in range(0, 10):
            cor_of_columns = []

            for column in range(0, 10):
                field = Deck.list_of_decks.get((row, column), None)

                if field:
                    if field.is_alive:
                        cor_of_columns.append(u"\u25A1")
                        continue

                    cor_of_columns.append(u"*")
                    continue

                cor_of_columns.append(u"~")

            cor_of_rows.append(cor_of_columns)
            print("\t".join(cor_of_columns))

    def fire(self, location: tuple) -> str:
        cor_of_fire = (location[0], location[1])

        for cor_of_ship, ship in self.fields.items():
            if cor_of_ship == cor_of_fire:
                ship.fire(location[0], location[1])

                if ship.is_drowned:
                    return "Sunk!"

                return "Hit!"

        return "Miss!"
