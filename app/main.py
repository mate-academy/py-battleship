class Battleship:
    def __init__(self, ships):
        self.field = self.create_dict_self_field(ships)

    def fire(self, location: tuple):
        miss_ind = 0
        for coord, hp in self.field.items():
            if location in coord or location == coord:
                miss_ind = 1
                self.field[coord] -= 1
                if self.field[coord] == 0:
                    return "Sunk!"
                else:
                    return "Hit!"

        if miss_ind == 0:
            return "Miss!"

    def create_dict_self_field(self, ships):
        res = {}
        for ship in ships:
            one_cell_hp_ident = 0
            non_empty_cells = ship
            if non_empty_cells[0] == non_empty_cells[1]:
                non_empty_cells = non_empty_cells[0]
                one_cell_hp_ident = 1

            non_empty_cells = list(non_empty_cells)

            if ship[0][0] - ship[1][0] != 0:
                not_change_coord = ship[1][1]
                if ship[0][0] > ship[1][0]:
                    lower_coord = ship[1][0]
                    higher_coord = ship[0][0]
                else:
                    lower_coord = ship[0][0]
                    higher_coord = ship[1][0]
                while lower_coord != higher_coord - 1:
                    lower_coord += 1
                    new_coord = (lower_coord, not_change_coord)
                    non_empty_cells.append(new_coord)

            if ship[0][1] - ship[1][1] != 0:
                not_change_coord = ship[0][0]
                if ship[0][1] > ship[1][1]:
                    lower_coord = ship[1][1]
                    higher_coord = ship[0][1]
                else:
                    lower_coord = ship[0][1]
                    higher_coord = ship[1][1]
                while lower_coord != higher_coord - 1:
                    lower_coord += 1
                    new_coord = (not_change_coord, lower_coord)
                    non_empty_cells.append(new_coord)

            non_empty_cells = tuple(non_empty_cells)
            if one_cell_hp_ident == 0:
                health_point = len(non_empty_cells)
                res.__setitem__(non_empty_cells, health_point)
            else:
                health_point = 1
                res.__setitem__(non_empty_cells, health_point)
        return res
