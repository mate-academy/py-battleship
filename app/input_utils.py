from app.constants import (
    DEBUG_COORDS,
    MAX_COORD,
    MIN_COORD,
    UI_MAX,
    UI_MIN,
)
from app.types_aliases import Cell


def get_coordinate() -> Cell | None:
    prompt = (
        f"\nEnter two numbers from {UI_MIN} to {UI_MAX} (e.g. 5 7)\n"
        f"or 'q' to quit: "
    )
    user_input = input(prompt).strip().lower()

    if user_input == "q":
        return None

    parts = validate_input_numbers(user_input)
    return parse_to_coordinate(parts)


def validate_input_numbers(user_input: str) -> list[str]:
    if not user_input:
        raise ValueError("No input received")

    parts = user_input.split()

    if len(parts) != 2:
        raise ValueError("Please enter exactly two numbers")

    if not all(part.isdigit() for part in parts):
        raise ValueError("Please enter valid numbers")

    return parts


def parse_to_coordinate(parts: list[str]) -> Cell:
    row = int(parts[0])
    col = int(parts[1])

    if not DEBUG_COORDS:
        row -= 1
        col -= 1

    if not is_within_bounds(row, col):
        raise ValueError(f"Numbers must be between {UI_MIN} and {UI_MAX}")

    return row, col


def is_within_bounds(row: int, col: int) -> bool:
    return (
        MIN_COORD <= row <= MAX_COORD
        and MIN_COORD <= col <= MAX_COORD
    )
