class BattleShipError(Exception):
    pass


class NumberOfShipsError(BattleShipError):
    pass


class NumberOfTypesError(BattleShipError):
    pass


class LocationError(BattleShipError):
    pass
