# Sample CMakeLists.txt to test Bluloco Dark
cmake_minimum_required(VERSION 3.10)
project(BlulocoTheme VERSION 1.0)

set(CMAKE_CXX_STANDARD 17)

add_executable(ThemeApp main.cpp utils.cpp)
target_link_libraries(ThemeApp PUBLIC Qt5::Widgets)

install(TARGETS ThemeApp DESTINATION bin)
