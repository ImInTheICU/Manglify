# Import Testing
import random
from datetime import timedelta

# Basic Math Testing
x = 356
y = 356

print(x + y)
print(x / y)
print(x * y)

# Function Testing
def test() -> int:
    return random.randint(1,100)

print("The return", test())
print(f"The F return {test()}")

# Wrap Testing
wrapper = lambda inter: inter() if callable(inter) == inter else inter

print(
    wrapper(wrapper(wrapper(wrapper(wrapper(test)))))()
)
