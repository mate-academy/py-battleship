class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return "□" if self.is_alive else "x"


class Ship:
    def __init__(self, start, end, is_drowned: bool = False) -> None:
        #start: tuple[int, int], end: tuple[int, int],is_drowned: bool = Fal
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []
        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))

        # Створіть колоди та збережіть їх у списку `self.decks`

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        # Знайдіть у списку відповідну колоду

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck is not None:
            deck.is_alive = False
        if deck in self.decks:
            if not any(deck.is_alive for deck in self.decks):
                self.is_drowned = True

        # Змінити статус «is_alive» колоди
        # І оновіть значення `is_drown`, якщо це необхідно


class Battleship:
    def __init__(self, ships: list[tuple[tuple[int, int], tuple[int, int]]]) -> None:
        self.ships = ships
        self.field = {}
        self._validate_field()
        for ship in self.ships:
            r1, c1 = ship[0]
            r2, c2 = ship[1]
        # Create a dict `self.field`.
        # Його ключами є кортежі - координати непорожніх комірок,
        # Значення для кожної комірки є посиланням на корабель
        # який знаходиться в ньому

    def fire(self, ceil: tuple) -> str:
        if self.field[(ceil[0], ceil[1])] == "~":
            return "Miss!"
        elif self.field[(ceil[0], ceil[1])] == "□":
            self.field[(ceil[0], ceil[1])] = "x"
            for ship in self.ships:
                if ceil in ship:
                    self.field[(ceil[0], ceil[1])] = "x"
                    return "Sunk!"
                else:
                    return "Hit!"
        else:
            return "Already fired at this ceil!"

        # Ця функція повинна перевіряти, чи місцезнаходження
        # є ключем у `self.field`
        # Якщо це так, то він повинен перевірити, чи ця клітина є останньою живою
        # на кораблі чи ні.
    def print_field(self) -> None:
        for row in self.field:
            for ceil in row:
                if ceil == "~":
                    print("~", end="\t")
                elif ceil == "□":
                    print(u"\u25A1", end="\t")
                elif ceil == "*":
                    print("*", end="\t")
                else:
                    print('x', end='\t')
            print()

    def _validate_field(self) -> None:
        num_ships = len(self.ships)
        num_single = sum(1 for s in self.ships if s[0] == s[1])
