from typing import List, Tuple, Optional

Location = Tuple[int, int]


class Cell:
    def __init__(self, value=None, idx=None):
        self.idx = idx
        self.option_numbers: List[int] = list(range(1, 10))
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


class KakoroBoard:
    def __init__(self, board: List[List[Cell]]):
        self.size: int = len(board)
        self.board: List[List[Cell]] = board
        self._set_all_visible_cells_relations()

    def __eq__(self, other):
        if other.size != self.size:
            return False

        for other_row, self_row in zip(self.board, other.board):
            for other_cell, self_cell in zip(other_row, self_row):
                if other_cell != self_cell:
                    return False
        return True

    def is_solved(self):
        return all([c.value > 0 if type(c) == Cell else True for row in self.board for c in row])

    def _set_all_visible_cells_relations(self) -> None:
        recent_constraint_cell: Optional[ConstraintCell] = None
        row_connected: List[Cell] = []
        col_connected: List[Cell] = []
        for y, row in enumerate(self.board):
            for x, item in enumerate(row):
                if type(item) != Cell:  # TODO (Eilon): Use isintance? - NOOOOO isinstance checks if the object is also a child of another object, and so if item is `BlackCell` the expression will be True!!
                    for connected_cell in row_connected:
                        tmp_row_connected = row_connected.copy()
                        tmp_row_connected.remove(connected_cell)
                        connected_cell.visible_cells += tmp_row_connected
                    if recent_constraint_cell:
                        recent_constraint_cell.right.size = len(row_connected)
                        recent_constraint_cell.right.visible_cells = row_connected.copy()
                        recent_constraint_cell = None
                    row_connected = []
                    if type(item) == ConstraintCell and item.right.result is not None:
                        recent_constraint_cell = item
                else:
                    row_connected.append(item)
            for connected_cell in row_connected:
                tmp_row_connected = row_connected.copy()
                tmp_row_connected.remove(connected_cell)
                connected_cell.visible_cells += tmp_row_connected
            if recent_constraint_cell and recent_constraint_cell.right.visible_cells == []:
                recent_constraint_cell.right.size = len(row_connected)
                recent_constraint_cell.right.visible_cells = row_connected
            row_connected = []
            recent_constraint_cell = None

        for x in range(len(self.board[0])):
            for y in range(len(self.board)):
                item = self.board[y][x]
                if type(item) != Cell:
                    for connected_cell in col_connected:
                        tmp_col_connected = col_connected.copy()
                        tmp_col_connected.remove(connected_cell)
                        connected_cell.visible_cells += tmp_col_connected
                    if recent_constraint_cell:
                        recent_constraint_cell.down.size = len(col_connected)
                        recent_constraint_cell.down.visible_cells = col_connected.copy()
                        recent_constraint_cell = None
                    col_connected = []

                    if type(item) == ConstraintCell and item.down.result is not None:
                        recent_constraint_cell = item
                else:
                    col_connected.append(item)
            for connected_cell in col_connected:
                tmp_col_connected = col_connected.copy()
                tmp_col_connected.remove(connected_cell)
                connected_cell.visible_cells += tmp_col_connected
            if recent_constraint_cell and recent_constraint_cell.down.visible_cells == []:
                recent_constraint_cell.down.size = len(col_connected)
                recent_constraint_cell.down.visible_cells = col_connected
            col_connected = []
            recent_constraint_cell = None

    def __str__(self):
        def get_val(p, i):
            if type(p) == BlackCell:
                return '#####'
            if type(p) == ConstraintCell:
                return (f" \\ {p.right.result if p.right.result is not None else '': <2}", "  \\  ",
                        f"{p.down.result if p.down.result is not None else '': <2} \\ ")[i]
            return (' ' * 5, f'{f"  {p.value if p.value is not None else 0}": <5}', ' ' * 5)[i]

        x_len, y_len = len(self.board[0]), len(self.board)
        res = (x_len * 6 + 1) * "-" + '\n'
        for i in range(y_len):
            for k in range(3):
                for j in range(x_len):
                    res += f"|{get_val(self.board[i][j], k)}"
                res += '|\n'
            res += (x_len * 6 + 1) * "-" + '\n'
        return res
