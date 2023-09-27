from board import KakoroBoard, Cell, BlackCell, ConstraintCell
from combination_calculator import combinations_with_option_numbers_to_sum


def reduce_all_options(board: KakoroBoard) -> None:
    """
    If a number was added to the board - use this function to eliminate the options to use this
    number from other cells
    """
    for y, row in enumerate(board.board):
        for x, item in enumerate(row):
            if type(item) == Cell:
                if item.value:
                    for connected_cell in item.visible_cells:
                        if item.value in connected_cell.option_numbers:
                            connected_cell.option_numbers.remove(item.value)


def _brute_force_constraint_cell(constraint_cell: ConstraintCell) -> None:
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
                set_cell.value = set_value
        else:
            for idx, set_cell in enumerate(constraint_cell.visible_cells):
                option_numbers_set = set()
                for res in results:
                    option_numbers_set.add(res[idx])
                set_cell.option_numbers = list(set(set_cell.option_numbers) & option_numbers_set)


def brute_force_iteration(board):
    for y, row in enumerate(board.board):
        for x, item in enumerate(row):
            if type(item) == ConstraintCell:
                _brute_force_constraint_cell(item)


def test():
    b = KakoroBoard([[BlackCell(), BlackCell(), ConstraintCell(down_result=3), BlackCell()],
                     [ConstraintCell(right_result=3), Cell(idx=1), Cell(idx=2), BlackCell()],
                     [BlackCell(), ConstraintCell(right_result=5), Cell(idx=3), Cell(3, idx=4)],
                     [BlackCell(), BlackCell(), BlackCell(), BlackCell()],
                     ])
    reduce_all_options(b)
    print(b)
    brute_force_iteration(b)
    print(b)
    brute_force_iteration(b)
    print(b)
    brute_force_iteration(b)
    print(b)


def test2():
    b = KakoroBoard([[BlackCell(), ConstraintCell(down_result=11), ConstraintCell(down_result=3)],
                     [ConstraintCell(right_result=3), Cell(), Cell()],
                     [ConstraintCell(right_result=11), Cell(), Cell()]])
    reduce_all_options(b)
    print(b)
    brute_force_iteration(b)
    print(b)


def test3():
    b = KakoroBoard([[BlackCell(), ConstraintCell(down_result=14), ConstraintCell(down_result=7)],
                     [ConstraintCell(right_result=15), Cell(), Cell()],
                     [ConstraintCell(right_result=6), Cell(), Cell()]])
    reduce_all_options(b)
    print(b)
    brute_force_iteration(b)
    print(b)


def test4():
    b = KakoroBoard(
        [[BlackCell(), BlackCell(), ConstraintCell(down_result=10), ConstraintCell(down_result=29), BlackCell()],
         [BlackCell(), ConstraintCell(right_result=9, down_result=16), Cell(), Cell(), ConstraintCell(down_result=4)],
         [ConstraintCell(right_result=15), Cell(), Cell(), Cell(), Cell()],
         [ConstraintCell(right_result=23), Cell(), Cell(), Cell(), Cell()],
         [BlackCell(), ConstraintCell(right_result=12), Cell(), Cell(), BlackCell()]])
    reduce_all_options(b)
    print(b)
    brute_force_iteration(b)
    print(b)
    brute_force_iteration(b)
    print(b)
    brute_force_iteration(b)
    print(b)


def test5():
    """
    #  14\  5\  #   #
   \13  9   4  11\  #
   \12  0   1  0    #
    #   #  \6  0    0
    """
    b = KakoroBoard(
        [[BlackCell(), ConstraintCell(down_result=14), ConstraintCell(down_result=5), BlackCell(), BlackCell()],
         [ConstraintCell(right_result=13), Cell(9), Cell(4), ConstraintCell(down_result=10), BlackCell()],
         [ConstraintCell(right_result=12), Cell(), Cell(1), Cell(), BlackCell()],
         [BlackCell(), BlackCell(), ConstraintCell(right_result=10), Cell(), Cell()]])
    reduce_all_options(b)
    print(b)
    brute_force_iteration(b)
    print(b)
    brute_force_iteration(b)
    print(b)
    brute_force_iteration(b)
    print(b)


def test6():
    """
      #   3\   16\  29\  #   #   #   #   #
     \15  0    9    0   11\  #   #   #   #
     \26  0    7    0    0   9   4   #   #
     #    #    \7   0    0   #   #   #   #
     #    #   \14   8    5   1   #   #   #
     #    #  28\28  0    0   2   5   8   9
     #   \11   0    0    #   #   #   #   #
     #    \9   0    0    #   #   #   #   #
     #    #    5    #    #   #   #   #   #
     #    #    4    #    #   #   #   #   #
     #    #    1    #    #   #   #   #   #
     #    #    3    #    #   #   #   #   #
     #    #    2    #    #   #   #   #   #
    """
    b = KakoroBoard(
        [[BlackCell(), ConstraintCell(down_result=3), ConstraintCell(down_result=16),
          ConstraintCell(down_result=29)] + [BlackCell()] * 5,
         [ConstraintCell(right_result=15), Cell(), Cell(9), Cell(), ConstraintCell(down_result=11)] + [BlackCell()] * 4,
         [ConstraintCell(right_result=26), Cell(), Cell(7), Cell(), Cell(), Cell(9), Cell(4)] + [BlackCell()] * 2,
         [BlackCell()] * 2 + [ConstraintCell(right_result=7), Cell(), Cell()] + [BlackCell()] * 4,
         [BlackCell()] * 2 + [ConstraintCell(right_result=14), Cell(8), Cell(5), Cell(1)] + [BlackCell()] * 3,
         [BlackCell()] * 2 + [ConstraintCell(down_result=28, right_result=28), Cell(), Cell(), Cell(2), Cell(5), Cell(8), Cell(9)],
         [BlackCell(), ConstraintCell(right_result=11), Cell(), Cell()] + [BlackCell()] * 5,
         [BlackCell(), ConstraintCell(right_result=9), Cell(), Cell()] + [BlackCell()] * 5,
         [BlackCell()] * 2 + [Cell(1)] + [BlackCell()] * 6,
         [BlackCell()] * 2 + [Cell(2)] + [BlackCell()] * 6,
         [BlackCell()] * 2 + [Cell(3)] + [BlackCell()] * 6,
         [BlackCell()] * 2 + [Cell(4)] + [BlackCell()] * 6,
         [BlackCell()] * 2 + [Cell(5)] + [BlackCell()] * 6,
         ])
    reduce_all_options(b)
    for _ in range(8):
        brute_force_iteration(b)
        print(b)


if __name__ == '__main__':
    test6()
