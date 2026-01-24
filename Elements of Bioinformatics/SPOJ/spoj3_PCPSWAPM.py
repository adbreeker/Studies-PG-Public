#PCPSWAPM - Swapping min and max
import sys
 
n = input()
numbers = list(map(int, input().split()))
 
max_num = max(numbers)
min_num = min(numbers)
 
for i in range(len(numbers)):
    if numbers[i] == max_num:
        numbers[i] = min_num
    elif numbers[i] == min_num:
        numbers[i] = max_num
 
print(" ".join(map(str, numbers))) 