"""
Sample Python code to test Bluloco Dark.
Includes decorators, f-strings, and type hints.
"""
from typing import List, Optional

def debug(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args}")
        return func(*args, **kwargs)
    return wrapper

@debug
def calculate_sum(numbers: List[int], multiplier: Optional[int] = None) -> int:
    res = sum(numbers)
    return res * multiplier if multiplier else res

if __name__ == "__main__":
    print(f"Result: {calculate_sum([1, 2, 3], 2)}")
