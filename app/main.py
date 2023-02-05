class Battleship:
    def __init__(self, ships: list) -> None:
        self.ships = ships
        self.field = [["~"] * 10 for _ in range(10)]
        for ship in ships:
            start_r, start_c = ship[0]
            end_r, end_c = ship[1]
            for i in range(start_r, end_r + 1):
                for j in range(start_c, end_c + 1):
                    self.field[i][j] = "□"
        self.shots = []

    def fire(self, location: tuple) -> str:
        row, column = location
        if self.field[row][column] == "~":
            return "Miss!"
        else:
            self.shots.append(location)
            for ship in self.ships:
                start_row, start_column = ship[0]
                end_row, end_column = ship[1]
                if (
                        start_row <= row <= end_row
                        and start_column <= column <= end_column
                ):
                    self.field[row][column] = "X"
                    if self.is_sunk(ship):
                        return "Sunk!"
                    else:
                        return "Hit!"

    def is_sunk(self, ship) -> bool:
        start_row, start_column = ship[0]
        end_row, end_column = ship[1]
        for i in range(start_row, end_row + 1):
            for j in range(start_column, end_column + 1):
                if self.field[i][j] == "□":
                    return False
        return True
