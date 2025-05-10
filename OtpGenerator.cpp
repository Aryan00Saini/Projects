#include <iostream>
#include <cstdlib>
#include <ctime>
#include <string>
#include <chrono>
#include <thread>

using namespace std;
using namespace chrono;

string generateOTP(int length = 6) {
    string otp = "";
    for (int i = 0; i < length; ++i) {
        otp += to_string(rand() % 10);
    }
    return otp;
}

int main() {
    srand(time(0)); 

    string otp = generateOTP();
    cout << "Your OTP is: " << otp << endl;
    cout << "Note: OTP is valid for 30 seconds." << endl;

    // Record the start time
    auto startTime = steady_clock::now();

    int maxAttempts = 3;
    int attempt = 0;
    bool success = false;

    while (attempt < maxAttempts) {
        string userInput;
        cout << "Attempt " << (attempt + 1) << "/" << maxAttempts << ". Enter OTP: ";
        cin >> userInput;

        auto currentTime = steady_clock::now();
        auto elapsed = duration_cast<seconds>(currentTime - startTime).count();

        if (elapsed > 30) {
            cout << " OTP expired! Please request a new OTP." << endl;
            break;
        }

        if (userInput == otp) {
            cout << " OTP confirmed successfully!" << endl;
            success = true;
            break;
        } else {
            cout << " Incorrect OTP." << endl;
        }

        attempt++;
        if (attempt < maxAttempts) {
            cout << "Please try again." << endl;
        }
    }

    if (!success && attempt >= maxAttempts) {
        cout << " Maximum attempts reached. Access denied." << endl;
    }

    return 0;
}
