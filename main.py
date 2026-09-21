def twoSum(nums, target):
    """Return indices of two numbers such that they add up to target."""
    lookup = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in lookup:
            return [lookup[complement], i]
        lookup[num] = i
    return []

if __name__ == "__main__":
    print(twoSum([2,7,11,15], 9))  # Expected: [0,1]