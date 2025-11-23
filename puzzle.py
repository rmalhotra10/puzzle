# puzzle.py
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Cell:
    # kind: "blank" (user enters number), "op", "result", "block", "given"
    kind: str
    value: Optional[str] = None


ROWS = 7
COLS = 7

# Grid layout taken from the book image (7x7)
# Row/col indices are 0-based.
GRID: List[List[Cell]] = [
    # row 0:  _  +  _  x  7  =  35
    [
        Cell("blank"),
        Cell("op", "+"),
        Cell("blank"),
        Cell("op", "x"),
        Cell("given", "7"),
        Cell("op", "="),
        Cell("result", "35"),
    ],
    # row 1:  x  ■  +  ■  -  ■  ■
    [
        Cell("op", "x"),
        Cell("block"),
        Cell("op", "+"),
        Cell("block"),
        Cell("op", "-"),
        Cell("block"),
        Cell("block"),
    ],
    # row 2:  _  +  _  -  _  =  12
    [
        Cell("blank"),
        Cell("op", "+"),
        Cell("blank"),
        Cell("op", "-"),
        Cell("blank"),
        Cell("op", "="),
        Cell("result", "12"),
    ],
    # row 3:  -  ■  x  ■  +  _  ■
    [
        Cell("op", "-"),
        Cell("block"),
        Cell("op", "x"),
        Cell("block"),
        Cell("op", "+"),
        Cell("blank"),
        Cell("block"),
    ],
    # row 4:  _  x  _  +  _  =  24
    [
        Cell("blank"),
        Cell("op", "x"),
        Cell("blank"),
        Cell("op", "+"),
        Cell("blank"),
        Cell("op", "="),
        Cell("result", "24"),
    ],
    # row 5:  =  ■  =  ■  =  ■  ■
    [
        Cell("op", "="),
        Cell("block"),
        Cell("op", "="),
        Cell("block"),
        Cell("op", "="),
        Cell("block"),
        Cell("block"),
    ],
    # row 6: 21 ■ 45 ■ 14 ■  ■
    [
        Cell("result", "21"),
        Cell("block"),
        Cell("result", "45"),
        Cell("block"),
        Cell("result", "14"),
        Cell("block"),
        Cell("block"),
    ],
]

# Convenience: list of all editable number cells (excluding the fixed 7)
VARIABLE_CELLS = [
    (r, c)
    for r in range(ROWS)
    for c in range(COLS)
    if GRID[r][c].kind == "blank"
]
