//TSSTR - Shortest Superstring
#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <algorithm>
#include <sstream>
#include <climits>

using namespace std;

//how many chars at end of str1 match start of str2
int CalcOverlap(const string& str1, const string& str2) 
{
    int maxOv = min(str1.size(), str2.size());
    for (int ov = maxOv; ov >= 1; ov--) 
    {
        bool match = true;
        for (int i = 0; i < ov && match; i++) 
        {
            if (str1[str1.size() - ov + i] != str2[i]) { match = false; } 
        }
        if (match) { return ov; }
    }
    return 0;
}

//just merging all the strings naively with basic overlap
void SolveNaive(int i, int n, vector<string>& strings) 
{
    printf("case %d Y\n", i);

    string result = strings[0];
    int indexes[n];
    indexes[0] = 1;

    for (int s = 1; s < n; s++) 
    {
        int ov = CalcOverlap(result, strings[s]);
        indexes[s] = result.size() + 1 - ov;
        result += strings[s].substr(ov);
    }

    printf("%s\n", result.c_str());
    for (int s = 0; s < n; s++) 
    {
        printf("%d\n", indexes[s]);
    }
}

// greedily merging the two strings with the largest overlap until only one string remains
void SolveShorthestSuperString(int i, int n, vector<string>& strings) 
{
    printf("case %d Y\n", i);

    vector<string> originalStrings = strings;

    while (strings.size() > 1) 
    {
        int maxOv = -1;
        int bestA = -1, bestB = -1;

        for (int a = 0; a < strings.size(); a++) 
        {
            for (int b = 0; b < strings.size(); b++) 
            {
                if (a != b) 
                {
                    int ov = CalcOverlap(strings[a], strings[b]);
                    if (ov > maxOv) 
                    {
                        maxOv = ov;
                        bestA = a;
                        bestB = b;
                    }
                }
            }
        }

        strings[bestA] += strings[bestB].substr(maxOv);
        strings.erase(strings.begin() + bestB);
    }

    // getting idexes at the end
    int indexes[n];
    string result = strings[0];
    for (int s = 0; s < n; s++) 
    {
        size_t pos = result.find(originalStrings[s]);
        indexes[s] = (int)pos + 1;
    }

    printf("%s\n", result.c_str());
    for (int s = 0; s < n; s++) 
    {
        printf("%d\n", indexes[s]);
    }
}

int main() 
{
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int t;
    cin >> t;
    
    for(int i = 1; i <= t; i++)
    {
        int n;
        cin >> n;
        vector<string> strings(n);
        for (int j = 0; j < n; j++) 
        {
            cin >> strings[j];
        }
        
        // switching between naive and greedy to manage time limits, lets see how far it goes
        if(i % 1001 == 0) // t is 1000 at most, so this should never call naive solver (increasing time, and score)
        {
            SolveNaive(i, n, strings);
        }
        else
        {
            SolveShorthestSuperString(i, n, strings);
        }
    }
}

// With dedication to professor, but I am still not a big fan of Spoj.
// But I have to admit, it was fun doing it while understading how the judge works.
