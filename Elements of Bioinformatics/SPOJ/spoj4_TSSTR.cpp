#include <bits/stdc++.h>
using namespace std;

// Calculate overlap: how many chars at end of a match start of b
int calcOverlap(const string& a, const string& b) 
{
    int maxOv = min(a.size(), b.size());
    for (int ov = maxOv; ov >= 1; ov--) 
    {
        bool match = true;
        for (int i = 0; i < ov && match; i++) 
        {
            if (a[a.size() - ov + i] != b[i]) { match = false; } 
        }
        if (match) { return ov; }
    }
    return 0;
}

int main() 
{
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int t;
    cin >> t;
    
    for (int tc = 1; tc <= t; tc++) 
    {
        int n;
        cin >> n;
        
        vector<string> words(n);
        for (int i = 0; i < n; i++) 
        {
            cin >> words[i];
        }
        
        // Store original words for position finding
        vector<string> origWords = words;
        
        // Map: original index -> index in reduced set (-1 if substring of another)
        vector<int> origToReduced(n, -1);
        
        // Remove words that are substrings of other words
        vector<bool> isSubstr(n, false);
        for (int i = 0; i < n; i++) 
        {
            for (int j = 0; j < n; j++) 
            {
                if (i != j && !isSubstr[j] && words[j].find(words[i]) != string::npos) 
                {
                    isSubstr[i] = true;
                    break;
                }
            }
        }
        
        vector<string> reduced;
        vector<int> reducedToOrig; // which original indices map to each reduced word
        for (int i = 0; i < n; i++) 
        {
            if (!isSubstr[i]) 
            {
                origToReduced[i] = reduced.size();
                reducedToOrig.push_back(i);
                reduced.push_back(words[i]);
            }
        }
        
        int m = reduced.size();
        
        if (m == 0) 
        {
            // All words are substrings of each other - find the longest one
            int longest = 0;
            for (int i = 1; i < n; i++) 
            {
                if (words[i].size() > words[longest].size()) { longest = i; }
            }
            cout << "case " << tc << " Y\n";
            cout << words[longest] << "\n";
            for (int i = 0; i < n; i++) 
            {
                size_t pos = words[longest].find(origWords[i]);
                cout << pos + 1 << "\n";
            }
            continue;
        }
        
        // Greedy: repeatedly merge two strings with maximum overlap
        // Track which reduced indices are still active
        vector<bool> active(m, true);
        vector<string> current = reduced;
        
        while (true) 
        {
            int bestI = -1, bestJ = -1, bestOv = -1;
            
            // Find pair with maximum overlap
            for (int i = 0; i < m; i++) 
            {
                if (!active[i]) { continue; }
                for (int j = 0; j < m; j++) 
                {
                    if (!active[j] || i == j) { continue; }
                    int ov = calcOverlap(current[i], current[j]);
                    if (ov > bestOv) 
                    {
                        bestOv = ov;
                        bestI = i;
                        bestJ = j;
                    }
                }
            }
            
            if (bestOv <= 0) { break; } // No more beneficial merges
            
            // Merge: current[bestI] + current[bestJ] (with overlap)
            string merged = current[bestI] + current[bestJ].substr(bestOv);
            current[bestI] = merged;
            active[bestJ] = false;
        }
        
        // Concatenate remaining active strings
        string superstr;
        for (int i = 0; i < m; i++) 
        {
            if (active[i]) 
            {
                superstr += current[i];
            }
        }
        
        // Find positions of all original words
        vector<int> positions(n);
        for (int i = 0; i < n; i++) 
        {
            size_t pos = superstr.find(origWords[i]);
            positions[i] = pos + 1; // 1-indexed
        }
        
        cout << "case " << tc << " Y\n";
        cout << superstr << "\n";
        for (int i = 0; i < n; i++) 
        {
            cout << positions[i] << "\n";
        }
    }
    
    return 0;
}
