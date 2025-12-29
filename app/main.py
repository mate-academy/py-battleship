class Deck:
    def __init__(self, row, column, is_alive=True):
        self.row = row
        self.column = column
        self.is_alive = is_alive

class Ship:
    def __init__(self, start, end, is_drowned=False):
        self.decks = []
        for row in range(start[0], end[0] + 1):
            for col in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, col))
        self.is_drowned = is_drowned

    def get_deck(self, row, column):
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row, column):
        deck = self.get_deck(row, column)
        if deck:
            deck.is_alive = False
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True


class Battleship:
    def __init__(self, ships):
        self.ships = []
        self.field = {}
        
        for ship_coords in ships:
            start = ship_coords[0]
            end = ship_coords[1]
            ship = Ship(start, end)
            self.ships.append(ship)
            
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def fire(self, location: tuple):
        if location in self.field:
            ship = self.field[location]
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self):
        for row in range(10):
            line = ""
            for col in range(10):
                if (row, col) in self.field:
                    ship = self.field[(row, col)]
                    deck = ship.get_deck(row, col)
                    
                    if ship.is_drowned:
                        line += "x\t"
                    elif not deck.is_alive:
                        line += "*\t"
                    else:
                        line += "□\t"
                else:
                    line += "~\t"
            print(line)

    def _validate_field(self):
        if len(self.ships) != 10:
            raise ValueError(f"Should be 10 ships, but got {len(self.ships)}")
        
        ship_counts = {1: 0, 2: 0, 3: 0, 4: 0}
        
        for ship in self.ships:
            size = len(ship.decks)
            if size not in ship_counts:
                raise ValueError(f"Invalid ship size: {size}")
            ship_counts[size] += 1
        
        if ship_counts[1] != 4:
            raise ValueError(f"Should be 4 single-deck ships, but got {ship_counts[1]}")
        if ship_counts[2] != 3:
            raise ValueError(f"Should be 3 double-deck ships, but got {ship_counts[2]}")
        if ship_counts[3] != 2:
            raise ValueError(f"Should be 2 three-deck ships, but got {ship_counts[3]}")
        if ship_counts[4] != 1:
            raise ValueError(f"Should be 1 four-deck ship, but got {ship_counts[4]}")
        
        for (row, col), ship in self.field.items():
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    
                    neighbor_row = row + dr
                    neighbor_col = col + dc
                    
                    if 0 <= neighbor_row < 10 and 0 <= neighbor_col < 10:
                        if (neighbor_row, neighbor_col) in self.field:
                            neighbor_ship = self.field[(neighbor_row, neighbor_col)]
                            if neighbor_ship != ship:
                                raise ValueError(
                                    f"Ships at ({row}, {col}) and "
                                    f"({neighbor_row}, {neighbor_col}) are neighbors"
                                )
