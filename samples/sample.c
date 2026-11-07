# Sample C code to test Bluloco Dark
# Includes macros, pointers, and doc comments
/**
 * @brief Calculates the factorial of a number.
 * @param n The number to calculate.
 * @return The factorial of n.
 */
#define MAX_VAL 100
#define SQUARE(x) ((x) * (x))

#include <stdio.h>

int main() {
    int arr[5] = {1, 2, 3, 4, 5};
    int *ptr = arr;
    printf("Square of 5 is %d\n", SQUARE(5));
    
    // User keyword test: custom_func
    custom_func(ptr);
    
    return 0;
}
