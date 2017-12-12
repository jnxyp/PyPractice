def deep_copy(l: list):
    l2 = []
    for e in l:
        l2.append(e)
    return l2


num_components = [0, 1, 2, 3, 4, 5, 6, 7, 8]
nums = []


def find_numbers(components: list, output_target: list, constructed: str = ''):
    if len(components) == 1:
        nums.append(constructed + str(components[0]))
        return
    for component in components:
        copy = deep_copy(components)
        copy.remove(component)
        find_numbers(copy, output_target, constructed + str(component))


find_numbers(num_components, nums)

print(*nums, file=open('all_nums.txt', 'w'))