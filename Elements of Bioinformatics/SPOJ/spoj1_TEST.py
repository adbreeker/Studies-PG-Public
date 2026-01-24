#TEST - Life, the Universe, and Everything
import sys
 
results = []
x = input()
while x != "42":
    results.append(x)
    x = input()
 
for result in results:
    print(result) 