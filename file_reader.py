from board import KakoroBoard, Cell, ConstraintCell, BlackCell
import requests
# from beatifulsoup import bs4
import re


def request_board(size=13):
    link = f"https://www.kakuros.com/?s={size}x{size}"
    # TODO (Eilon): Do regex magic
    r = requests.get(link)

    string_to_find = 'var board = '
    text = r.text
    var_board_pos = text.find(string_to_find)
    end = text[var_board_pos:].find('] ]')
    final_str = text[var_board_pos + len(string_to_find) + 3:var_board_pos + end + 1] + '  '

    def parse_num(_num):
        if _num == '-1' or _num == '0':
            return int(_num)
        num = '0' * (5 - len(_num)) + _num
        return int(num[:2]), int(num[2:4])

    l = []
    for _line in final_str.split('\n'):
        line = list(map(parse_num, _line[1:-3].split(',')))
        l.append(line)
    print(l)
    return l


def read_from_file(file_name: str):
    with open(file_name, 'r') as f:
        lines = f.readlines()
    return lines


def convert_int_tuple_to_cell(o):
    match o:
        case int():
            match o:
                case -1:
                    return BlackCell()
                case _:
                    return Cell(o)
        case tuple():
            return ConstraintCell(*o)

l = request_board(13)
l = KakoroBoard([list(map(convert_int_tuple_to_cell, a)) for a in l])

print(l)
from solver import reduce_all_options, brute_force_iteration
reduce_all_options(l)

brute_force_iteration(l)
print(l)
s = ""
counter = 0
while s != str(l):
    counter += 1
    s = str(l)
    brute_force_iteration(l)

print(l)
print(l.is_solved())
print(counter)

print(l.prety_block('1'))

"""
 #   #   #    #    #   3\   16\  29\  #    17\  7\  #   # 
 #   #   #    #   \15  0     9   0  11\9   8    1   #   # 
 #   #   #    #   \26  0     7   0    0    9    4  23\  # 
 #   #   #    #   3\   16\  \7   0    0   6\11  2   9  16\ 
 #   #   3\  30\8  1   7   \14   8    5    1  11\13 6   7 
 #  \20  1    8   2    9  28\28  0    0    2    5   8   9 
 #   \8  2    6   24\  \11  0    0   \4    3    1  17\  # 
 #   4\  7\15 7   8   11\9  0    0   16\  3\11  2   9   # 
 \30  3  4    9   7    2    5    \22  9    2    3   8   # 
 \3  1   2   7\14  9   1    4    \8   7    1    #   #   # 
 #   \3  1    2   4\4  3    1    3\  16\   #    #   #   # 
 #   #  \22   4   1    5    3    2    7    #    #   #   # 
 #   #   \4   1   3   \12   2    1    9    #    #   #   # 

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