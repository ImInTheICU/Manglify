# Import Testing
import random
from datetime import timedelta

# Basic Math
x = 356
y = 356

print(x + y)
print(x / y)
print(x * y)

print('Hello World!')

# Function Testing
def test() -> int:
    return random.randint(1,100)

print("The return", test())
print(f"The F return {test()}")
