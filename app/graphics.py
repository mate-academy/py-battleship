class Surface:
    def __init__(
            self,
            width: int,
            height: int,
            fill_symbol: str = " "
    ) -> None:
        self.height = height
        self.width = width
        self.data: dict[int, dict[int, str]] = dict()
        self.fill(fill_symbol)

    def draw_point(self, row: int, column: int, symbol: str) -> None:
        if len(symbol) != 1:
            raise ValueError("Function accepts only one symbol")
        self.data[row][column] = symbol

    def fill(self, symbol: str) -> None:
        if len(symbol) != 1:
            raise ValueError("Function accepts only one symbol")
        self.data = {
            y: {x: symbol for x in range(self.width)}
            for y in range(self.height)
        }

    def __str__(self) -> str:
        return "\n".join(
            "".join([self.data[y][x] for x in self.data[y]])
            for y in self.data
        )
