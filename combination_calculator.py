from typing import List


def combination_calculator(result: int, length: int, cannot_exist: List[int] = None, existing: List[int] = None):
    if existing:
        return combination_calculator(result - sum(existing), length - len(existing), cannot_exist)

    cannot_exist = cannot_exist if cannot_exist else []
    option_numbers = [i for i in range(1, 10) if i not in cannot_exist]
    return _combinations_using_numbers_to_sum(result, length, option_numbers)


def _combinations_using_numbers_to_sum(result: int, length: int, option_numbers: List[int]):
    if length == 1:
        if result in option_numbers:
            return [[result]]
        return []
    results = []
    for option in option_numbers:
        if option < result:
            new_option_numbers = option_numbers.copy()
            for i in range(1, option + 1):
                if i in new_option_numbers:
                    new_option_numbers.remove(i)

            for sub_comb in _combinations_using_numbers_to_sum(result - option, length - 1, new_option_numbers):
                results.append([option] + sub_comb)
    return results


def test_combination_calculator():
    assert combination_calculator(24, 3, cannot_exist=[1, 7]) == []
    assert combination_calculator(24, 3, cannot_exist=[1, 6]) == [[7, 8, 9]]
    print(combination_calculator(10, 3))
    print(combination_calculator(24, 3, cannot_exist=[1, 6], existing=[8]))
    print(combination_calculator(3, 1))
    print(combination_calculator(3, 2))
    print(combination_calculator(3, 3))
    print(combination_calculator(3, 1, existing=[8]))


def combinations_with_option_numbers_to_sum(result: int, length: int, option_numbers: List[List[int]]):
    if length == 1:
        if result in option_numbers[-length]:
            return [[result]]
        return []
    results = []
    for option in option_numbers[-length]:
        if option < result:
            for sub_comb in combinations_with_option_numbers_to_sum(result - option, length - 1, option_numbers):
                tmp_res = [option] + sub_comb
                if len(tmp_res) == len(set(tmp_res)):
                    results.append(tmp_res)

    return results


def test_combinations_with_option_numbers_to_sum():
    print(combinations_with_option_numbers_to_sum(3, length=2, option_numbers=[list(range(1, 10)), list(range(2, 10))]))
    print(combinations_with_option_numbers_to_sum(4, length=2, option_numbers=[list(range(1, 10)), list(range(2, 10))]))


if __name__ == '__main__':
    test_combinations_with_option_numbers_to_sum()
