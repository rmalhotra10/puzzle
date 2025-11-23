# app.py
import streamlit as st
from puzzle import GRID, ROWS, COLS, Cell

st.set_page_config(page_title="One to Nine Puzzle", page_icon="🧩")

st.title("One to Nine")

st.write(
    "Using the numbers **1 to 9**, complete these six equations "
    "(three reading across and three reading downwards). "
    "Each number is used once only, and **7** is already in place."
)

LIGHT = "#f5f5d5"   # light cell background
DARK = "#1b7a40"    # dark green blocks
CELL_SIZE = 50      # px (for the HTML boxes)


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
        ">
            {text}
        </div>
        """,
        unsafe_allow_html=True,
    )


st.write("")  # small spacer

# Draw the 7x7 grid row by row
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
                # one-character input box for user digits
                st.text_input(
                    label="",
                    key=key,
                    max_chars=1,
                    help="Enter a digit 1–9",
                )

st.write("---")
st.info(
    "Right now this is just the visual puzzle. "
    "Next step: add a **Check solution** button that reads your inputs, "
    "verifies the equations, and enforces the 1–9 uniqueness rule."
)
