from app.classes.deck import Deck
from app.classes.ship import Ship


def check_neighbours_free(
        deck: Deck,
        current_ship: Ship,
        matrix: list[list]
) -> bool:
    row, col = deck.row, deck.col
    return not any(
        [
            matrix[i][j]
            for j in range(col - 1, col + 2)
            for i in range(row - 1, row + 2)
            if all(
                [
                    i >= 0,
                    i < 10,
                    j >= 0,
                    j < 10,
                    (i != row or j != col),
                    not current_ship.get_deck(i, j)
                ]
            )
        ]
    )
