# Sample C++ code to test Bluloco Dark
#include <iostream>
#include <vector>
#include <memory>

/**
 * Template class to test complex types and operators
 */
template <typename T>
class Buffer {
    std::vector<T> data;
public:
    void push(T val) { data.push_back(val); }
    T& operator[](size_t idx) { return data[idx]; }
};

int main() {
    auto buf = std::make_unique<Buffer<int>>();
    buf->push(42);
    std::cout << "Value: " << (*buf)[0] << std::endl;
    return 0;
}
