from typing import List, Tuple, Optional

Location = Tuple[int, int]


class Cell:
    """
    # TODO (Eilon): Switch `self.option_numbers` to be static?
    OPTION_NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # and every call to self.option_numbers will be switched to Cell.OPTION_NUMBERS
    """

    def __init__(self, value=None, idx=None):
        self.idx = idx
        self.option_numbers: List[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.value: int = value
        self.visible_cells = []

    def __str__(self):
        return f" {str(self.value if self.value else 0)} "

    def __eq__(self, other):
        return self.value == other.value


class SubConstraintCell(Cell):
    def __init__(self, result: int = None):
        super().__init__()
        self.result: int = result
        self.size: int = -1
        self.is_finished: bool = False
        self.option_numbers: List[int] = []


class ConstraintCell(Cell):
    def __init__(self, right_result: int = None, down_result: int = None):
        super().__init__()
        self.right = SubConstraintCell(right_result)
        self.down = SubConstraintCell(down_result)
        self.option_numbers: List[int] = []

    def __str__(self):
        def print_helper(num):
            return num if num else ''

        return f" {print_helper(self.down.result)}\\{print_helper(self.right.result)} "


class BlackCell(Cell):
    def __init__(self):
        super().__init__()
        self.option_numbers: List[int] = []

    def __str__(self):
        return " # "


class Board:
    def __init__(self, board: List[List[Cell]]):
        self.dimensions: Tuple[int, int] = (len(board), len(board[0]))
        assert all(len(row) == self.dimensions[1] for row in board)
        self.board: List[List[Cell]] = board

    def __eq__(self, other):
        if other.dimensions != self.dimensions:
            return False

        for other_row, self_row in zip(self.board, other.board):
            for other_cell, self_cell in zip(other_row, self_row):
                if other_cell != self_cell:
                    return False
        return True

    def iterate_rows(self):
        for row in self.board:
            yield row

    def iterate_cols(self):
        for x in range(self.dimensions[1]):
            yield [self.board[y][x] for y in range(self.dimensions[0])]

    def __str__(self):
        def get_val(p, i):
            if type(p) == BlackCell:
                return '#####'
            if type(p) == ConstraintCell:
                return (f" \\ {p.right.result if p.right.result is not None else '': <2}", "  \\  ",
                        f"{p.down.result if p.down.result is not None else '': <2} \\ ")[i]
            return (' ' * 5, f'{f"  {p.value if p.value is not None else 0}": <5}', ' ' * 5)[i]

        y_len, x_len = self.dimensions
        res = (x_len * 6 + 1) * "-" + '\n'
        for i in range(y_len):
            for k in range(3):
                for j in range(x_len):
                    res += f"|{get_val(self.board[i][j], k)}"
                res += '|\n'
            res += (x_len * 6 + 1) * "-" + '\n'
        return res


class KakoroBoard(Board):
    def __init__(self, board: List[List[Cell]]):
        super().__init__(board)
        self._set_all_visible_cells_relations()

    def is_solved(self):
        return all(c.value > 0 if type(c) == Cell and c.value else True for row in self.board for c in row)

    @staticmethod
    def _set_line_relations(line: List[Cell], direction: str):
        recent_constraint_cell: Optional[ConstraintCell] = None
        connected_cells: List[Cell] = []
        line = list(line) + [BlackCell()]
        for item in line:
            if type(item) != Cell:
                for connected_cell in connected_cells:
                    tmp_row_connected = connected_cells.copy()
                    tmp_row_connected.remove(connected_cell)
                    connected_cell.visible_cells += tmp_row_connected
                if recent_constraint_cell:
                    recent_constraint_cell.size = len(connected_cells)
                    recent_constraint_cell.visible_cells = connected_cells.copy()
                    recent_constraint_cell = None
                connected_cells = []

                if type(item) is ConstraintCell:
                    sub_constraint_item = item.right if direction == "right" else item.down
                    if sub_constraint_item.result is not None:
                        recent_constraint_cell = sub_constraint_item
            else:
                connected_cells.append(item)

    def _set_all_visible_cells_relations(self) -> None:
        for row in self.board:
            self._set_line_relations(row, "right")

        for col in self.iterate_cols():
            self._set_line_relations(col, "down")


class KillerBoard(Board):
    """
    TODO (Eilon): Suggestion to killer suduku board:
    Make cells within the same group have an id corresponding to the group, i.e.
    Ask Eilon for an example...

    Interesting Note:
    A suduku board is 9x9, we can create a kakuru board that is 10x10 and put the killer inside, than the constraint of 1..9 is met?
    i'm not sure, maybe we need to add that within the 3 by 3 cells there are no repeating numbers.


    """

    def __init__(self, board: List[List[Cell]]):
        super().__init__(board)
