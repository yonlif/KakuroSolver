from board import KakoroBoard, Cell, ConstraintCell, BlackCell
import requests


def request_board(dimensions=(13, 13)):
    link = f"https://www.kakuros.com/?s={dimensions[0]}x{dimensions[1]}"
    # TODO (Eilon): Do regex magic
    r = requests.get(link)

    string_to_find = 'var board = '
    text = r.text
    var_board_pos = text.find(string_to_find)
    end = text[var_board_pos:].find('] ]')
    final_str = text[var_board_pos + len(string_to_find) + 3:var_board_pos + end + 1] + '  '
    l = []
    for _line in final_str.split('\n'):
        line = _line[1:-3].split(',')
        l.append(line)
    return l


def convert_int_tuple_to_cell(o):
    match o:
        case int():
            match o:
                case -1:
                    return BlackCell()
                case 0:
                    return Cell()
                case _:
                    return Cell(o)
        case tuple():
            return ConstraintCell(*o)


def parse_num(_num):
    if _num == '-1' or _num == '0':
        return int(_num)
    num = '0' * (5 - len(_num)) + _num
    return int(num[:2]), int(num[2:4])


def convert_str_to_board(l):
    lines = []
    for line in l:
        lines.append(list(map(parse_num, line)))
    return KakoroBoard([list(map(convert_int_tuple_to_cell, a)) for a in lines])


l = request_board((9, 8))
l = convert_str_to_board(l)

print(l)
