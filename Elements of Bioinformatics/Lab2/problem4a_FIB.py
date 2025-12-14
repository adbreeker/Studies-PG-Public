#Rabbits and Recurrence Relations
import os

test_data = "5 3"

def RabbitsPairs(n, k):
    rabbits_per_month = [0] * n
    rabbits_per_month[0] = 1
    rabbits_per_month[1] = 1
    for month in range(2, n):
        rabbits_per_month[month] = rabbits_per_month[month - 1] + k * rabbits_per_month[month - 2]
    return rabbits_per_month[-1]

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_fib.txt")
    if os.path.exists(file_path):
        data = open(file_path).read().strip()
    else:
        data = test_data

    n, k = map(int, data.split())

    print(RabbitsPairs(n, k))