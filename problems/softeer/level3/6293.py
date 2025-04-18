import sys
from functools import reduce

#5
#3 2 1 4 5

def read_line(*args, sep=" "):
    input_values = input().split(sep)

    if not args:
        return input_values

    return list(reduce(lambda acc, func: map(func, acc), args, input_values))


def longest_increasing_sequence(arr):
    n = len(arr)
    dp = [1 for i in range(n)]

    for i in range(n):
        for j in range(i):
            if (arr[i] > arr[j] and dp[j] + 1 > dp[i]):
                dp[i] = dp[j] + 1
        
    print(max(dp))
    
    
N = read_line(int)
arr = read_line(int)

longest_increasing_sequence(arr)

#3
