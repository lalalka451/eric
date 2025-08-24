cmake_minimum_required(VERSION 3.10)

project(HelloWorld)

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Add executable
add_executable(HelloWorld main.cpp)