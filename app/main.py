def find_coords(start: tuple, end: tuple) -> None:
    coords = []

    x1, y1 = start
    x2, y2 = end

    if y1 == y2:
        step_x = 1 if x1 < x2 else -1

        for x in range(x1, x2 + step_x, step_x):
            coords.append((x, y1))

    elif x1 == x2:
        step_y = 1 if y1 < y2 else -1

        for y in range(y1, y2 + step_y, step_y):
            coords.append((x1, y))

    return coords


class Deck:
    def __init__(
            self,
            coords: tuple,
            is_alive: bool = True
    ) -> None:

        self.is_alive = is_alive
        self.coords = coords


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:

        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.fire_decks = 0

        self.decks = [Deck(coords) for coords in find_coords(self.start, self.end)]

    def fire(self, deck: Deck, is_drowned: bool = None) -> None:
        deck.is_alive = False
        self.fire_decks += 1
        if is_drowned:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.count = 0
        self.deadline = []
        self.ship_check = {4: 0, 3: 0, 2: 0, 1: 0}
        self.ship_limit = {4: 1, 3: 2, 2: 3, 1: 4}
        self.ships = [
            Ship(start, end)
            for start, end in ships
            if self._validation_field(start, end)
        ]

    def _validation_field(self, start: tuple, end: tuple) -> bool:
        if self.count <= 10:
            ship_lenght = abs(end[0] - start[0]) + 1 \
                if end[1] == start[1] else abs(end[1] - start[1]) + 1

            if ship_lenght in self.ship_limit:
                if self.ship_check[ship_lenght] < self.ship_limit[ship_lenght]:
                    if start[0] == end[0]:
                        if start[0] != 0:
                            self.deadline.extend(find_coords([start[0] + 1, start[1]], [end[0] + 1, end[1]]))
                            if start[1] != end[1]:
                                if start[1] != 0:
                                    self.deadline.extend(find_coords((start[0] - 1, start[1] - 1), (start[0] + 1, start[1] - 1)))
                        if start[0] != 9:
                            self.deadline.extend(find_coords([start[0] - 1, start[1]], [end[0] - 1, end[1]]))
                    else:
                        self.deadline.append([end[0] + 1, end[1]])

                    if start not in self.deadline and end not in self.deadline:
                        self.count += 1
                        self.ship_check[ship_lenght] += 1
                        return True
            # Validator deadline

        return False

    def fire(self, location: tuple) -> str:
        for ship in self.ships:
            if not ship.is_drowned:

                for deck in ship.decks:
                    if location == deck.coords and deck.is_alive:

                        if ship.fire_decks == len(ship.decks) - 1:
                            ship.fire(deck, is_drowned=True)
                            return "Sunk!"

                        ship.fire(deck)
                        return "Hit!"
        return "Miss!"
