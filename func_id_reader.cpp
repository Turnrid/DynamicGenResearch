#include <iostream>
#include <fstream>
#include <string>
#include <set>
#include <unordered_map>
#include <chrono>
#include <thread>
#include "Common/Shmqueue/include/Queue.h"
#include "Common/DynTrace/include/Event.h"

// ANSI escape code for clearing the console screen
void clearScreen() {
    std::cout << "\033[2J\033[1;1H";
}

// Load function IDs from "function_list.txt" into a map
std::unordered_map<unsigned, std::string> loadFunctionList(const std::string& filename) {
    std::unordered_map<unsigned, std::string> functionMap;
    std::ifstream infile(filename);
    if (!infile.is_open()) {
        std::cerr << "Error: Could not open " << filename << std::endl;
        return functionMap;
    }

    std::string line;
    while (std::getline(infile, line)) {
        size_t separator = line.find(':');
        if (separator != std::string::npos) {
            std::string funcName = line.substr(0, separator);
            unsigned funcID = std::stoi(line.substr(separator + 1));
            functionMap[funcID] = funcName;
        }
    }

    infile.close();
    return functionMap;
}

// Write uncovered functions to "uncovered_functions.txt"
void writeUncoveredFunctions(const std::unordered_map<unsigned, std::string>& functionMap, const std::set<unsigned>& coveredFunctions) {
    std::ofstream outfile("uncovered_functions.txt");
    if (!outfile.is_open()) {
        std::cerr << "Error: Could not open uncovered_functions.txt for writing." << std::endl;
        return;
    }

    for (const auto& entry : functionMap) {
        unsigned funcID = entry.first;
        const std::string& funcName = entry.second;
        if (coveredFunctions.find(funcID) == coveredFunctions.end()) {
            outfile << funcName << ":" << funcID << "\n";
        }
    }

    outfile.close();
}

// Display real-time function coverage stats
void displayCoverageStats(size_t totalFunctions, size_t coveredFunctions, const std::string& heartbeat) {
    clearScreen();
    std::cout << "---------------- Function Coverage ----------------\n";
    std::cout << "Total Functions:   " << totalFunctions << "\n";
    std::cout << "Covered Functions: " << coveredFunctions << "\n";
    float coveragePercent = (coveredFunctions / static_cast<float>(totalFunctions)) * 100;
    std::cout << "Coverage:          " << coveragePercent << "%\n";
    std::cout << "---------------------------------------------------\n";
    std::cout << "Status: Running " << heartbeat << "\n";
}

// Generate heartbeat animation
std::string getHeartbeat(int step) {
    const std::string states[] = {".   ", "..  ", "... ", "...."};
    return states[step % 4];
}

int main() {
    auto functionMap = loadFunctionList("/home/security/DynamicGenResearch/function_list.txt");
    if (functionMap.empty()) {
        std::cerr << "No functions loaded. Exiting..." << std::endl;
        return 1;
    }

    size_t totalFunctions = functionMap.size();
    std::set<unsigned> coveredFunctions;  // Set to track covered function IDs

    InitQueue(MEMMOD_SHARE);  // Initialize the shared memory queue

    int heartbeatStep = 0;

    while (true) {
        QNode* node = FrontQueue();
        if (node == nullptr || node->IsReady == 0) {
            // Display coverage stats with heartbeat if no new function is covered
            displayCoverageStats(totalFunctions, coveredFunctions.size(), getHeartbeat(heartbeatStep));
            heartbeatStep++;
            std::this_thread::sleep_for(std::chrono::milliseconds(250));
            continue;
        }

        // Get the function ID from the queue
        ObjValue *OV = (ObjValue *) node->Buf;
        unsigned FuncID = OV->Value;

        // Update coverage if this is a new function hit
        if (coveredFunctions.insert(FuncID).second) {  // insert returns true if the item was new
            writeUncoveredFunctions(functionMap, coveredFunctions);  // Update uncovered functions list
            displayCoverageStats(totalFunctions, coveredFunctions.size(), getHeartbeat(heartbeatStep));  // Display updated coverage stats
        }

        // Mark the node as processed
        OutQueue(node);
    }

    return 0;
}
