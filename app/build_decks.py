from app.deck import Deck


def build_decks(start: tuple, end: tuple) -> list:
    decks = []
    for row in range(start[0], end[0] + 1):
        for column in range(start[1], end[1] + 1):
            deck = Deck(row, column)
            decks.append(deck)
    return decks
