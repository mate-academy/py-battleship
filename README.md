# Battleship

**Please note:** read [the guideline](https://github.com/mate-academy/py-task-guideline/blob/main/README.md)
before starting.

Let's implement a class that provides an interface to create and modify the field for Battleship game.
It should have the following public methods:
- `__init__(self, ships)`, to create a field with given ships;
- `fire(self, ceil)`, to simulate a shot to cell.

Consider a field as a matrix 10x10.
```
x	x	x	x	~	□	□	~	□	□	
~	~	~	~	~	~	~	~	~	~	
□	~	~	~	□	□	□	~	□	□	
□	~	~	~	~	~	~	~	~	~	
□	~	~	~	~	~	~	~	~	~	
~	~	~	~	~	~	~	~	~	~	
~	~	~	~	~	~	~	~	~	~	
~	~	~	~	~	~	~	□	~	□	
~	~	~	~	~	~	~	~	~	~	
~	~	~	~	~	~	~	□	~	□
```
The first coordinate of each cell is the number of the row.

The second is the number of the column.

The upper-left corner has coordinates `(0, 0)`.

The lower-right has coordinates `(9, 9)`.

We will define a ship by the coordinates of its ends.

For example, a ship marked with crosses has ends with coordinates
`(0, 0)` and `(0, 3)`, so a tuple `((0, 0), (0, 3))` corresponds to it.

Implement the class `Battleship` that takes a list of ships. Each ship is represented by a such tuple.

Example:
```python 
battle_ship = Battleship(
    ships=[
        ((0, 0), (0, 3)),
        ((0, 5), (0, 6)),
        ((0, 8), (0, 9)),
        ((2, 0), (4, 0)),
        ((2, 4), (2, 6)),
        ((2, 8), (2, 9)),
        ((9, 9), (9, 9)),
        ((7, 7), (7, 7)),
        ((7, 9), (7, 9)),
        ((9, 7), (9, 7)),
    ]
)
```
This field can be represented as follows:
```
□	□	□	□	~	□	□	~	□	□	
~	~	~	~	~	~	~	~	~	~	
□	~	~	~	□	□	□	~	□	□	
□	~	~	~	~	~	~	~	~	~	
□	~	~	~	~	~	~	~	~	~	
~	~	~	~	~	~	~	~	~	~	
~	~	~	~	~	~	~	~	~	~	
~	~	~	~	~	~	~	□	~	□	
~	~	~	~	~	~	~	~	~	~	
~	~	~	~	~	~	~	□	~	□
```
Here `~` is an empty cell and `□` is a deck.

If the `fire` method is called it should return one 
of the following strings:
- `"Miss!"` - when there is no ship in the given ceil;
- `"Hit!"` - when there is a deck in the ceil, but 
the corresponding ship still have another
alive deck;
- `"Sunk!"` - when there is the last alive deck.

Example:
```python
print(
    battle_ship.fire((0, 4)),  # Miss!
    battle_ship.fire((0, 3)),  # Hit!
    battle_ship.fire((0, 2)),  # Hit!
    battle_ship.fire((0, 1)),  # Hit!
    battle_ship.fire((0, 0)),  # Sunk!
)
```

**Note:** follow the created template and implement 
already declared methods. Feel free to add your own
methods to extend the functionality.

### Extra tasks:
#### 1. Print field 
_It is recommended to implement this method, it will greatly simplify the debugging process!_

Create method `print_field` which prints all
cells of the field line by line.
- Use `~` symbol for empty cells
- Use `□` symbol for alive decks.
You can print it using the unicode symbol:
```python
print(u"\u25A1")
```
- Use `*` for hit decks of the alive ship
- Use `x` for decks of the drowned ship

Feel free to use other symbols instead of these if you think it'd be better.


#### 2. Validate input
Write protected method `_validate_field` that
should check the following conditions after creating
a field in the `__init__` method:
- the total number of the ships should be 10;
- there should be 4 single-deck ships;
- there should be 3 double-deck ships; 
- there should be 2 three-deck ships; 
- there should be 1 four-deck ship;
- ships shouldn't be located in the neighboring cells
  (even if cells are neighbors by diagonal).

### Note: Check your code using this [checklist](checklist.md) before pushing your solution.
