#PCP2SUBS - Sums of two subsequences
import sys
 
n = input()
numbers = list(map(int, input().split()))
 
subsequence_positive_sum = 0
subsequence_negative_sum = 0
for number in numbers:
    if number > 0:
        subsequence_positive_sum += number
    else:
        subsequence_negative_sum += number
 
print(str(subsequence_positive_sum) + " " + str(subsequence_negative_sum)) 