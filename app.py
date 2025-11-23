# app.py
import streamlit as st
from puzzle import GRID, ROWS, COLS, Cell

st.set_page_config(page_title="One to Nine Puzzle", page_icon="🧩")

st.title("One to Nine")

st.write(
    "Using the numbers **1 to 9**, complete these six equations "
    "(three reading across and three reading downwards). "
    "Every number is used once only, and **7** is already in place."
)

LIGHT = "#f5f5d5"   # light cell background
DARK = "#1b7a40"    # dark green blocks
CELL_SIZE = 50      # pixels for the boxes


def render_block():
    st.markdown(
        f"""
        <div style="
            width:{CELL_SIZE}px;
            height:{CELL_SIZE}px;
            background-color:{DARK};
        "></div>
        """,
        unsafe_allow_html=True,
    )


def render_static(text: str, bold: bool = True):
    st.markdown(
        f"""
        <div style="
            display:flex;
            align-items:center;
            justify-content:center;
            width:{CELL_SIZE}px;
            height:{CELL_SIZE}px;
            background-color:{LIGHT};
            font-size:22px;
            {'font-weight:bold;' if bold else ''}
            color:#000;
        ">
            {text}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------- Draw grid ----------
for r in range(ROWS):
    cols = st.columns(COLS, gap="small")
    for c in range(COLS):
        cell: Cell = GRID[r][c]
        with cols[c]:
            key = f"cell-{r}-{c}"

            if cell.kind == "block":
                render_block()

            elif cell.kind in ("op", "result", "given"):
                render_static(cell.value)

            elif cell.kind == "blank":
                st.text_input(
                    label="",
                    key=key,
                    max_chars=1,
                    help="Enter a digit 1–9",
                )

st.write("---")

# ---------- Helper functions for checking ----------

def read_numbers():
    """
    Read all number cells (blank + given) into a 2D list of ints or None.
    Returns (grid_numbers, errors:list[str]).
    """
    numbers = [[None for _ in range(COLS)] for _ in range(ROWS)]
    errors = []
    used_digits = []

    for r in range(ROWS):
        for c in range(COLS):
            cell = GRID[r][c]

            if cell.kind == "given":
                val = int(cell.value)
                numbers[r][c] = val
                used_digits.append(val)

            elif cell.kind == "blank":
                key = f"cell-{r}-{c}"
                raw = st.session_state.get(key, "").strip()

                if raw == "":
                    errors.append(f"Cell at row {r+1}, col {c+1} is empty.")
                    continue

                if not raw.isdigit():
                    errors.append(
                        f"Cell at row {r+1}, col {c+1} must be a digit 1–9."
                    )
                    continue

                val = int(raw)
                if not (1 <= val <= 9):
                    errors.append(
                        f"Cell at row {r+1}, col {c+1} must be between 1 and 9."
                    )
                    continue

                numbers[r][c] = val
                used_digits.append(val)

    # Uniqueness: digits 1..9 exactly once (7 is pre-filled)
    if len([d for row in numbers for d in row if d is not None]) == 9:
        if set(used_digits) != set(range(1, 10)):
            errors.append(
                f"Digits used are {sorted(used_digits)} "
                f"but they must be exactly 1–9 with no repeats."
            )
        elif len(set(used_digits)) != len(used_digits):
            errors.append("You have repeated at least one digit.")
    else:
        # don't add an error here; missing cells already reported
        pass

    return numbers, errors


def apply_op(a: int, b: int, op: str) -> int:
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "x":
        return a * b
    raise ValueError(f"Unknown op {op}")


def eval_three(n1: int, op1: str, n2: int, op2: str, n3: int) -> int:
    """
    Evaluate n1 op1 n2 op2 n3 with normal precedence: x before + and -.
    """
    # multiplication first
    if op1 == "x" and op2 != "x":
        return apply_op(apply_op(n1, n2, "x"), n3, op2)
    elif op2 == "x" and op1 != "x":
        return apply_op(n1, apply_op(n2, n3, "x"), op1)
    else:
        # neither or both are x -> left to right
        return apply_op(apply_op(n1, n2, op1), n3, op2)


def check_equations(numbers):
    """
    Check the 3 horizontal and 3 vertical equations.
    Returns a list of (name, ok, lhs, rhs).
    """
    n = numbers  # alias

    results = []

    # Across rows
    # Row 0: [n00 + n02 x 7] = 35
    results.append(
        ("Row 1", eval_three(n[0][0], "+", n[0][2], "x", n[0][4]), 35)
    )
    # Row 2: [n20 + n22 - n24] = 12
    results.append(
        ("Row 3", eval_three(n[2][0], "+", n[2][2], "-", n[2][4]), 12)
    )
    # Row 4: [n40 x n42 + n44] = 24
    results.append(
        ("Row 5", eval_three(n[4][0], "x", n[4][2], "+", n[4][4]), 24)
    )

    # Down columns
    # Col 0: [n00 x n20 - n40] = 21
    results.append(
        ("Col 1", eval_three(n[0][0], "x", n[2][0], "-", n[4][0]), 21)
    )
    # Col 2: [n02 + n22 x n42] = 45
    results.append(
        ("Col 3", eval_three(n[0][2], "+", n[2][2], "x", n[4][2]), 45)
    )
    # Col 4: [7 - n24 + n44] = 14
    results.append(
        ("Col 5", eval_three(n[0][4], "-", n[2][4], "+", n[4][4]), 14)
    )

    # Convert to (name, ok, lhs, rhs)
    return [(name, lhs == rhs, lhs, rhs) for name, lhs, rhs in results]


# ---------- Button + logic ----------

if st.button("Check solution"):
    nums, errors = read_numbers()

    if errors:
        st.error("There are issues with your inputs:")
        for e in errors:
            st.write(f"- {e}")
    else:
        checks = check_equations(nums)
        all_ok = all(ok for _, ok, _, _ in checks)

        if all_ok:
            st.success("✅ Correct! You solved the puzzle.")
        else:
            st.error("Some equations are incorrect:")
            for name, ok, lhs, rhs in checks:
                if not ok:
                    st.write(f"- **{name}**: left side = {lhs}, should be {rhs}")