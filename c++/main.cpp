#include <iostream>
#include <string>
#include <limits>

// Function prototypes
void displayMenu();
double getNumber();
char getOperation();
double calculate(double num1, double num2, char operation);

int main() {
    bool continueCalculation = true;
    
    std::cout << "Welcome to C++ Calculator!" << std::endl;
    
    while (continueCalculation) {
        displayMenu();
        
        // Get first number
        std::cout << "Enter first number: ";
        double num1 = getNumber();
        
        // Get operation
        char operation = getOperation();
        
        // Get second number
        std::cout << "Enter second number: ";
        double num2 = getNumber();
        
        // Perform calculation and display result
        try {
            double result = calculate(num1, num2, operation);
            std::cout << "Result: " << num1 << " " << operation << " " << num2 << " = " << result << std::endl;
        } catch (const std::exception& e) {
            std::cout << "Error: " << e.what() << std::endl;
        }
        
        // Ask if user wants to continue
        char choice;
        std::cout << "\nDo you want to perform another calculation? (y/n): ";
        std::cin >> choice;
        
        // Clear input buffer
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        
        if (choice != 'y' && choice != 'Y') {
            continueCalculation = false;
        }
    }
    
    std::cout << "Thank you for using C++ Calculator!" << std::endl;
    return 0;
}

// Function to display calculator menu
void displayMenu() {
    std::cout << "\n===== C++ Calculator =====" << std::endl;
    std::cout << "Operations:" << std::endl;
    std::cout << "  + : Addition" << std::endl;
    std::cout << "  - : Subtraction" << std::endl;
    std::cout << "  * : Multiplication" << std::endl;
    std::cout << "  / : Division" << std::endl;
    std::cout << "========================\n" << std::endl;
}

// Function to get a valid number from user
double getNumber() {
    double number;
    while (!(std::cin >> number)) {
        std::cout << "Invalid input. Please enter a number: ";
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    }
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    return number;
}

// Function to get a valid operation from user
char getOperation() {
    char operation;
    bool validOperation = false;
    
    while (!validOperation) {
        std::cout << "Enter operation (+, -, *, /): ";
        std::cin >> operation;
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        
        if (operation == '+' || operation == '-' || operation == '*' || operation == '/') {
            validOperation = true;
        } else {
            std::cout << "Invalid operation. Please try again." << std::endl;
        }
    }
    
    return operation;
}

// Function to perform calculation based on the operation
double calculate(double num1, double num2, char operation) {
    switch (operation) {
        case '+':
            return num1 + num2;
        case '-':
            return num1 - num2;
        case '*':
            return num1 * num2;
        case '/':
            if (num2 == 0) {
                throw std::runtime_error("Division by zero is not allowed");
            }
            return num1 / num2;
        default:
            throw std::runtime_error("Invalid operation");
    }
}