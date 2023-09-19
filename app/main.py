from app.ship import Ship


class Battleship:
    def __init__(self, ships: list) -> None:
        self.field = self.organize_input(ships)

    def fire(self, location: tuple) -> str:
        ship = self.field.get(location)
        if ship and not ship.is_drowned:
            row, column = location
            ship.fire(row, column)
            if ship.is_drowned:
                print("Sunk!")
                return "Sunk!"
            else:
                print("Hit!")
                return "Hit!"
        print("Miss!")
        return "Miss!"

    def organize_input(self, input_data: list[tuple[tuple]]) -> dict:
        result = {}
        for ship_coords in input_data:
            all_coords = self.fill_the_gap(ship_coords[0], ship_coords[1])
            ship = Ship(ship_coords[0], ship_coords[1])
            temp = dict.fromkeys(all_coords, ship)
            result.update(temp)
        return result

    @staticmethod
    def fill_the_gap(start: tuple, end: tuple) -> list:
        if start[0] == end[0]:
            return [(start[0], i) for i in range(start[1], end[1] + 1)]
        elif start[1] == end[1]:
            return [(i, start[1]) for i in range(start[0], end[0] + 1)]
        else:
            return []
