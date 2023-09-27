from board import KakoroBoard, BlackCell, ConstraintCell, Cell
from solver import solve_loop

test_boards = [
    KakoroBoard([[BlackCell(), BlackCell(), ConstraintCell(down_result=3), BlackCell()],
                 [ConstraintCell(right_result=3), Cell(idx=1), Cell(idx=2), BlackCell()],
                 [BlackCell(), ConstraintCell(right_result=5), Cell(idx=3), Cell(3, idx=4)],
                 [BlackCell(), BlackCell(), BlackCell(), BlackCell()],
                 ]),
    KakoroBoard([[BlackCell(), ConstraintCell(down_result=11), ConstraintCell(down_result=3)],
                 [ConstraintCell(right_result=3), Cell(), Cell()],
                 [ConstraintCell(right_result=11), Cell(), Cell()]]),
    KakoroBoard([[BlackCell(), ConstraintCell(down_result=14), ConstraintCell(down_result=7)],
                 [ConstraintCell(right_result=15), Cell(), Cell()],
                 [ConstraintCell(right_result=6), Cell(), Cell()]]),
    KakoroBoard(
        [[BlackCell(), BlackCell(), ConstraintCell(down_result=10), ConstraintCell(down_result=29), BlackCell()],
         [BlackCell(), ConstraintCell(right_result=9, down_result=16), Cell(), Cell(), ConstraintCell(down_result=4)],
         [ConstraintCell(right_result=15), Cell(), Cell(), Cell(), Cell()],
         [ConstraintCell(right_result=23), Cell(), Cell(), Cell(), Cell()],
         [BlackCell(), ConstraintCell(right_result=12), Cell(), Cell(), BlackCell()]]),
    #  #  14\  5\  #   #
    # \13  9   4  11\  #
    # \12  0   1  0    #
    #  #   #  \6  0    0
    KakoroBoard(
        [[BlackCell(), ConstraintCell(down_result=14), ConstraintCell(down_result=5), BlackCell(), BlackCell()],
         [ConstraintCell(right_result=13), Cell(9), Cell(4), ConstraintCell(down_result=10), BlackCell()],
         [ConstraintCell(right_result=12), Cell(), Cell(1), Cell(), BlackCell()],
         [BlackCell(), BlackCell(), ConstraintCell(right_result=10), Cell(), Cell()]]),

    #  #   3\   16\  29\  #   #   #   #   #
    # \15  0    9    0   11\  #   #   #   #
    # \26  0    7    0    0   9   4   #   #
    # #    #    \7   0    0   #   #   #   #
    # #    #   \14   8    5   1   #   #   #
    # #    #  28\28  0    0   2   5   8   9
    # #   \11   0    0    #   #   #   #   #
    # #    \9   0    0    #   #   #   #   #
    # #    #    5    #    #   #   #   #   #
    # #    #    4    #    #   #   #   #   #
    # #    #    1    #    #   #   #   #   #
    # #    #    3    #    #   #   #   #   #
    # #    #    2    #    #   #   #   #   #
    KakoroBoard(
        [[BlackCell(), ConstraintCell(down_result=3), ConstraintCell(down_result=16),
          ConstraintCell(down_result=29)] + [BlackCell()] * 5,
         [ConstraintCell(right_result=15), Cell(), Cell(9), Cell(), ConstraintCell(down_result=11)] + [BlackCell()] * 4,
         [ConstraintCell(right_result=26), Cell(), Cell(7), Cell(), Cell(), Cell(9), Cell(4)] + [BlackCell()] * 2,
         [BlackCell()] * 2 + [ConstraintCell(right_result=7), Cell(), Cell()] + [BlackCell()] * 4,
         [BlackCell()] * 2 + [ConstraintCell(right_result=14), Cell(8), Cell(5), Cell(1)] + [BlackCell()] * 3,
         [BlackCell()] * 2 + [ConstraintCell(down_result=28, right_result=28), Cell(), Cell(), Cell(2), Cell(5),
                              Cell(8),
                              Cell(9)],
         [BlackCell(), ConstraintCell(right_result=11), Cell(), Cell()] + [BlackCell()] * 5,
         [BlackCell(), ConstraintCell(right_result=9), Cell(), Cell()] + [BlackCell()] * 5,
         [BlackCell()] * 2 + [Cell(1)] + [BlackCell()] * 6,
         [BlackCell()] * 2 + [Cell(2)] + [BlackCell()] * 6,
         [BlackCell()] * 2 + [Cell(3)] + [BlackCell()] * 6,
         [BlackCell()] * 2 + [Cell(4)] + [BlackCell()] * 6,
         [BlackCell()] * 2 + [Cell(5)] + [BlackCell()] * 6,
         ])
]


def test_all_boards():
    for b in test_boards:
        res = solve_loop(b)
        assert res[1]
        print(res[0])


if __name__ == '__main__':
    test_all_boards()
