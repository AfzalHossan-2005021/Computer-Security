import sys
import random
from BitVector import *
sys.path.append("./BitVector-3.5.0/BitVector")

# Generate a prime number of specified bit width.
def generate_prime(width: int) -> int:
    while True:
        p = BitVector(intVal = 0).gen_random_bits(width)
        if p.test_for_primality():
            return p.intValue()
        
# Function to generate curve parameters
def generate_curve_params(p: int, width: int) -> tuple:
    while True:
        # Generate random a and b less than p
        a = random.getrandbits( width ) % p
        b = random.getrandbits( width ) % p
        
        # Check if the curve is valid
        if (4 * a**3 + 27 * b**2) % p != 0:
            break
    return (a, b)

def main():
    # Set seed and generate a random prime number
    random.seed(2005021)
    p = generate_prime(128)
    a, b = generate_curve_params(p, 128)
    print(p)
    print(a)
    print(b)

if __name__ == "__main__":
    main()