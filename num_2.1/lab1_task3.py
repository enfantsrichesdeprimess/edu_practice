import random

def doubls():
    nums = []
    for i in range(random.randint(5,10)):
        nums.append(random.randint(1,20))
    print(nums)
    print(len(nums) != len(set(nums)))

doubls()