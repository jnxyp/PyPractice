def binary_search(nums: list, target: int):
    return binary_search_recursive(nums, 0, len(nums) - 1, target)


def binary_search_recursive(nums: list, start: int, end: int, target: int):
    if end - start <= 1:
        if nums[start] == target:
            return start
        elif nums[end] == target:
            return end
        else:
            return -1
    mid = start + (end - start) // 2
    if target == nums[mid]:
        return mid
    elif target < nums[mid]:
        return binary_search_recursive(nums, start, mid, target)
    else:
        return binary_search_recursive(nums, mid, end, target)


def quick_sort(nums):
    if len(nums) <= 1:
        return nums
    else:
        mid = nums[0]
        nums1, nums2 = [], []
        for n in nums[1:]:
            if n <= mid:
                nums1.append(n)
            else:
                nums2.append(n)
        return combine(append_to_end(quick_sort(nums1), mid), quick_sort(nums2))


def combine(list1, list2):
    if list1 is None:
        return list2
    elif list2 is None:
        return list1
    for i in list2:
        append_to_end(list1, i)
    return list1


def append_to_end(list, obj):
    if obj is None:
        return list
    list.append(obj)
    return list


def twoSum(nums: list, target: int):
    """
    :type nums: List[int]
    :type target: int
    :rtype: List[int]
    """
    sorted_nums = quick_sort(nums)
    i1 = 0
    while i1 < len(sorted_nums) - 1:
        temp = sorted_nums[i1+1:]
        diff = target - sorted_nums[i1]
        i2 = binary_search(sorted_nums, diff) + i1
        if i2 != -1:
            index1 = nums.index(sorted_nums[i1])
            index2 = nums.index(diff)
            while index1 == index2:
                index2 = nums.index(diff, index1 + 1)
            return [index1, index2]
        i1 += 1
print(twoSum([3,3], 6))
