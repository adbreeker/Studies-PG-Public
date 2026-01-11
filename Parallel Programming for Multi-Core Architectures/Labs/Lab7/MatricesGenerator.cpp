#include <iostream>
#include <fstream>
#include <random>
#include <string>
#include <filesystem>

int main(int argc, char* argv[]) 
{
    int n = argc > 1 ? std::atoi(argv[1]) : 25;
    const int SIZE = 1024;

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 100); // Random integers from 0 to 100

    // Get the directory of the executable
    std::filesystem::path exePath(argv[0]);
    std::filesystem::path exeDir = exePath.parent_path();
    std::filesystem::create_directories(exeDir / "InputMatrices");

    for (int i = 0; i < n; i++) 
    {
        std::filesystem::path filePath = exeDir / "InputMatrices" / ("matrix" + std::to_string(i) + ".txt");
        std::ofstream file(filePath);
        if (!file) 
        {
            std::cerr << "Error opening file: " << filePath << std::endl;
            continue;
        }

        for (int row = 0; row < SIZE; row++) 
        {
            for (int col = 0; col < SIZE; col++) 
            {
                file << dis(gen);
                if (col < SIZE - 1){ file << " "; }
            }
            file << "\n";
        }
        file.close();
        std::cout << "Generated " << filePath << std::endl;
    }

    return 0;
}
