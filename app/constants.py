# Size of square game board (rows × columns)
GRID_SIZE = 10

# Syncs UI coordinates with internal 0-based indexing (for debugging).
# Simplifies development and testing by aligning input with internal logic.
DEBUG_COORDS = False

# Bounds displayed in input prompts and user messages:
# - 0–9 when DEBUG_COORDS is True (zero-based, debug mode)
# - 1–10 when DEBUG_COORDS is False (one-based, user mode)
UI_MIN = 0 if DEBUG_COORDS else 1
UI_MAX = GRID_SIZE - 1 if DEBUG_COORDS else GRID_SIZE

# Bounds used for internal coordinate validation (always 0-based).
MIN_COORD = 0
MAX_COORD = GRID_SIZE - 1

# Expected fleet configuration: ship size → required count
EXPECTED_SHIPS = {
    1: 4,  # Single-deck ships
    2: 3,  # Double-deck ships
    3: 2,  # Triple-deck ships
    4: 1,  # Quadruple-deck ship
}

# Symbols representing cell states (Unicode)
SYMBOL_ALIVE = "□"    # Undamaged deck
SYMBOL_SUNK = "■"     # Hit or sunk deck
SYMBOL_EMPTY = "·"    # Untouched cell
SYMBOL_MISS = "•"     # Missed shot
SYMBOL_AROUND = "✖"   # Area surrounding a sunk ship

# Legend displayed at game start.
SYMBOL_LEGEND_LINES = [
    f"  {SYMBOL_ALIVE} — alive deck",
    f"  {SYMBOL_SUNK} — sunk or hit deck",
    f"  {SYMBOL_EMPTY} — untouched cell",
    f"  {SYMBOL_MISS} — missed shot",
    f"  {SYMBOL_AROUND} — area around sunk ship",
]

# Internal deck statuses
DECK_ALIVE = "alive"
DECK_HIT = "hit"

# Internal ship statuses
SHIP_AFLOAT = "afloat"
SHIP_DROWNED = "drowned"

# Messages displayed after firing a shot.
SHOT_HIT = "Hit!"
SHOT_MISS = "Miss!"
SHOT_REPEAT = "You already fired at this location."
SHOT_SUNK = "Sunk!"
