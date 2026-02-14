//ADAMATCH - Ada and Nucleobase
#include <iostream>
#include <string>
#include <vector>
#include <cmath>
#include <algorithm>

using namespace std;

const double PI = acos(-1.0);

//FFT aproach - final chance, my sanity is sitting...  
//brute force is too slow, and matrix alignment eats to much memory 
//BTW I hate Spoj again, instead of memory limit issue or something like this, I've got Runtime Error (SIGKILL) ...
void FFT(vector<double>& real, vector<double>& imag, bool inverse) 
{
    int n = real.size();

    for (int i = 1, j = 0; i < n; i++) 
    {
        //okay fine, bitwise operations beat me a little, this part is stolen xd
        int bit = n >> 1;
        for (; j & bit; bit >>= 1) { j ^= bit; }
        j ^= bit;
        if (i < j) 
        { 
            swap(real[i], real[j]); 
            swap(imag[i], imag[j]); 
        }
    }

    for (int len = 2; len <= n; len *= 2) 
    {
        double angle = 2 * PI / len * (inverse ? -1 : 1);
        double wReal = cos(angle);
        double wImag = sin(angle);

        for (int i = 0; i < n; i += len) 
        {
            double curReal = 1, curImag = 0;

            for (int j = 0; j < len / 2; j++) 
            {
                double tReal = curReal * real[i + j + len/2] - curImag * imag[i + j + len/2];
                double tImag = curReal * imag[i + j + len/2] + curImag * real[i + j + len/2];

                real[i + j + len/2] = real[i + j] - tReal;
                imag[i + j + len/2] = imag[i + j] - tImag;
                real[i + j] += tReal;
                imag[i + j] += tImag;

                double newReal = curReal * wReal - curImag * wImag;
                double newImag = curReal * wImag + curImag * wReal;
                curReal = newReal;
                curImag = newImag;
            }
        }
    }

    if (inverse) 
    {
        for (int i = 0; i < n; i++) 
        { 
            real[i] /= n; 
            imag[i] /= n; 
        }
    }
}

vector<long long> FTTConvolution(const vector<int>& a, const vector<int>& b) 
{
    int n = 1;
    while (n < (int)(a.size() + b.size())) { n *= 2; }

    vector<double> aReal(n, 0), aImag(n, 0);
    vector<double> bReal(n, 0), bImag(n, 0);

    for (int i = 0; i < (int)a.size(); i++) { aReal[i] = a[i]; }
    for (int i = 0; i < (int)b.size(); i++) { bReal[i] = b[i]; }

    FFT(aReal, aImag, false);
    FFT(bReal, bImag, false);

    for (int i = 0; i < n; i++) 
    {
        double rr = aReal[i] * bReal[i] - aImag[i] * bImag[i];
        double ri = aReal[i] * bImag[i] + aImag[i] * bReal[i];
        aReal[i] = rr;
        aImag[i] = ri;
    }

    FFT(aReal, aImag, true);

    vector<long long> result(n);
    for (int i = 0; i < n; i++) { result[i] = llround(aReal[i]); }
    return result;
}

int CalcLowestHammingDistance(const string& text, const string& pattern) 
{
    int n = text.size();
    int m = pattern.size();
    string reversed = pattern;
    reverse(reversed.begin(), reversed.end());

    vector<long long> matches(n + m - 1, 0);
    string bases = "ACGT";

    for (char c : bases) 
    {
        vector<int> t(n), p(m);
        for (int i = 0; i < n; i++) { t[i] = (text[i] == c) ? 1 : 0; }
        for (int i = 0; i < m; i++) { p[i] = (reversed[i] == c) ? 1 : 0; }

        vector<long long> conv = FTTConvolution(t, p);
        for (int i = 0; i < n + m - 1; i++) { matches[i] += conv[i]; }
    }

    int minDist = m;
    for (int i = m - 1; i < n; i++) 
    {
        int dist = m - (int)matches[i];
        if (minDist > dist) { minDist = dist; }
        if (minDist == 0) { break; }
    }

    return minDist;
}

int main() 
{
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    string text, pattern;
    cin >> text >> pattern;

    int result = CalcLowestHammingDistance(text, pattern);
    printf("%d\n", result);
}