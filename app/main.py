class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.ships = {}
        self.cell_to_ship = {}

        for index, ship in enumerate(ships):
            start, end = ship
            ship_cells = set()

            if start[0] == end[0]:
                row = start[0]
                for col in range(
                    min(start[1], end[1]),
                    max(start[1], end[1]) + 1,
                ):
                    cell = (row, col)
                    ship_cells.add(cell)
                    self.cell_to_ship[cell] = index
            else:
                col = start[1]
                for row in range(
                    min(start[0], end[0]),
                    max(start[0], end[0]) + 1,
                ):
                    cell = (row, col)
                    ship_cells.add(cell)
                    self.cell_to_ship[cell] = index

            self.ships[index] = {
                "cells": ship_cells,
                "hits": set(),
            }

        self._validate_field()

    def fire(self, cell: tuple[int, int]) -> str:
        if cell not in self.cell_to_ship:
            return "Miss!"

        ship_id = self.cell_to_ship[cell]
        ship = self.ships[ship_id]

        ship["hits"].add(cell)

        if ship["hits"] == ship["cells"]:
            return "Sunk!"

        return "Hit!"

    def print_field(self) -> None:
        field = [["~" for _ in range(10)] for _ in range(10)]

        for ship in self.ships.values():
            cells = ship["cells"]
            hits = ship["hits"]

            sunk = cells == hits

            for row, col in cells:
                if sunk:
                    field[row][col] = "x"
                elif (row, col) in hits:
                    field[row][col] = "*"
                else:
                    field[row][col] = u"\u25A1"

        for row in field:
            print(" ".join(row))

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValueError(
                "There must be exactly 10 ships"
            )

        lengths = []

        all_cells = set()

        for ship in self.ships.values():
            cells = ship["cells"]
            lengths.append(len(cells))

            for cell in cells:
                all_cells.add(cell)

        if lengths.count(1) != 4:
            raise ValueError(
                "There must be 4 single-deck ships"
            )

        if lengths.count(2) != 3:
            raise ValueError(
                "There must be 3 double-deck ships"
            )

        if lengths.count(3) != 2:
            raise ValueError(
                "There must be 2 three-deck ships"
            )

        if lengths.count(4) != 1:
            raise ValueError(
                "There must be 1 four-deck ship"
            )

        for row, col in all_cells:
            for d_row in (-1, 0, 1):
                for d_col in (-1, 0, 1):
                    if d_row == 0 and d_col == 0:
                        continue

                    neighbour = (
                        row + d_row,
                        col + d_col,
                    )

                    if neighbour not in all_cells:
                        continue

                    ship_a = self.cell_to_ship[(row, col)]
                    ship_b = self.cell_to_ship[neighbour]

                    if ship_a != ship_b:
                        raise ValueError(
                            "Ships cannot touch"
                        )
