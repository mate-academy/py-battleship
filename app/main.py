
class Deck:
    def __init__(self, row, column, is_alive=True):
        pass


class Ship:
    def __init__(self, start, end, is_drowned=False):
        # Create decks and save them to a list `self.decks`
        pass

    def get_deck(self, row, column):
        # Find the corresponding deck in the list
        pass

    def fire(self, row, column):
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        pass


class Battleship:
    def __init__(self, ships):
        self.field = {}

        for ship in ships:
            len_x, len_y = [abs(x - y) for x, y in zip(ship[0], ship[1])]
            for step in range(len_x):
                self.field[(ship[0][0] + step, ship[0][1])] = ship
            for step in range(len_y):
                self.field[(ship[0][0], ship[0][1] + step)] = ship
            self.field[ship[1]] = ship

    def fire(self, location: tuple):
        if location in self.field:
            the = self.field[location]
            self.field[location] = f"{self.field[location]} Hit!"
            if the not in self.field.values():
                return "Sunk!"
            return "Hit!"
        return "Miss!"


if __name__ == "__main__":
    battle_ship = Battleship(
        ships=[
                    ((2, 0), (2, 3)),
                    ((4, 5), (4, 6)),
                    ((3, 8), (3, 9)),
                    ((6, 0), (8, 0)),
                    ((6, 4), (6, 6)),
                    ((6, 8), (6, 9)),
                    ((9, 9), (9, 9)),
                    ((9, 5), (9, 5)),
                    ((9, 3), (9, 3)),
                    ((9, 7), (9, 7)),
                ]
    )
    print(battle_ship.field)