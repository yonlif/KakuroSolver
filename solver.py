from typing import Tuple

from board import KakoroBoard, Cell, BlackCell, ConstraintCell
from combination_calculator import combinations_with_option_numbers_to_sum


def reduce_all_options(board: KakoroBoard) -> None:
    """
    If a number was added to the board - use this function to eliminate the options to use this
    number from other cells
    """
    for row in board.board:
        for item in row:
            if type(item) == Cell:
                if item.value:
                    for connected_cell in item.visible_cells:
                        if item.value in connected_cell.option_numbers:
                            connected_cell.option_numbers.remove(item.value)


def _brute_force_constraint_cell(constraint_cell: ConstraintCell) -> bool:
    progress_made = False
    for constraint_cell in [constraint_cell.right, constraint_cell.down]:
        if not constraint_cell.visible_cells or constraint_cell.is_finished:
            continue
        results = combinations_with_option_numbers_to_sum(result=constraint_cell.result,
                                                          length=constraint_cell.size,
                                                          option_numbers=list(map(lambda cell: [
                                                              cell.value] if cell.value else cell.option_numbers,
                                                                                  constraint_cell.visible_cells)))
        if len(results) == 0:
            raise "Impossible"
        elif len(results) == 1:
            constraint_cell.is_finished = True
            for set_value, set_cell in zip(results[0], constraint_cell.visible_cells):
                if set_cell.value != set_value:
                    progress_made = True
                    set_cell.value = set_value
        else:
            for idx, set_cell in enumerate(constraint_cell.visible_cells):
                if set_cell.value is not None:
                    continue
                option_numbers_set = set()
                for res in results:
                    option_numbers_set.add(res[idx])
                new_option_numbers = sorted(list(set(set_cell.option_numbers) & option_numbers_set))
                if new_option_numbers != set_cell.option_numbers:
                    progress_made = True
                    set_cell.option_numbers = new_option_numbers
    return progress_made


def brute_force_iteration(board) -> bool:
    progress_made = False
    for y, row in enumerate(board.board):
        for x, item in enumerate(row):
            if type(item) == ConstraintCell:
                progress_made |= _brute_force_constraint_cell(item)
    return progress_made


def solve_loop(board: KakoroBoard) -> Tuple[int, bool]:
    counter = 0
    progress = True
    while progress:
        counter += 1
        progress = brute_force_iteration(board)
    return counter, board.is_solved()
