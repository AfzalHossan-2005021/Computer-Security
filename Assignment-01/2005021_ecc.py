import sys
import time
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
        a = random.randint(0, p-1)
        b = random.randint(0, p-1)
        
        # Check if the curve is valid
        if (4 * a**3 + 27 * b**2) % p != 0:
            break
    return (a, b)

# Legendre symbol calculation
def legendre(a: int, p: int) -> int:
    return pow(a, (p - 1) // 2, p)

# Check if a number is a quadratic residue modulo p using Euler's criterion
def is_quadratic_residue(n: int, p: int) -> bool:
    return legendre(n, p) == 1

# Implement Tonelli-Shanks algorithm to compute square roots modulo P efficiently
def tonelli_shanks(a: int, p: int) -> int:
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1

    if s == 1 :
        return pow(a, (p + 1)//4, p)

    for z in range(2, p):
        if p - 1 == legendre(z, p):
            break

    c = pow(z, q, p)
    r = pow(a, (q+1) // 2, p)
    t = pow(a, q, p)

    m = s

    t2 = 0

    while (t - 1) % p != 0:
        t2 = (t * t) % p
        for i in range(1, m):
            if (t2 -1) % p == 0:
                break
            t2 = (t2 * t2) % p
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r

# Find a point on the curve
def find_generator_point(a: int, b: int, p: int) -> tuple:
    # Find a point on the curve
    while True:
        x = random.randint(0, p-1)
        y_squared = (x**3 + a * x + b) % p
        if is_quadratic_residue(y_squared, p):
            y = tonelli_shanks(y_squared, p)
            return (x, y)
        
# Function add two points on the curve
def add_points(p1: tuple, p2: tuple, a: int, p: int) -> tuple:
    x1, y1 = p1
    x2, y2 = p2
    if p1 == p2:
        try:
            m = (3 * x1**2 + a) * pow(2 * y1, -1, p) % p
        except ValueError:
            return None
    else:
        try:
            m = (y2 - y1) * pow(x2 - x1, -1, p) % p
        except ValueError:
            return None
    x3 = (m**2 - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p
    return (x3, y3)

# scelar multiplication of generator point
def double_and_add(d: int, point: tuple, a: int, p: int) -> tuple:
    result = None
    addend = point

    for i in range(d.bit_length() - 1, -1, -1):
        if result is not None:
            result = add_points(result, result, a, p)
        if d & (1 << i):
            if result is None:
                result = addend
            else:
                result = add_points(result, addend, a, p)

    return result

# Function to generate public and private keys
def generate_keys(point: tuple, a: int, p: int) -> tuple:
    # Generate a random private key
    private_key = random.randint(1, p-1)
    # Calculate the public key using scalar multiplication
    public_key = None
    while public_key is None:
        private_key = random.randint(1, p-1)
        public_key = double_and_add(private_key, point, a, p)

    return (private_key, public_key)

def main():
    # Set seed and generate a random prime number
    random.seed(2005021)
    time_stamp = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    trials = 10
    len_p = [128, 192, 256]
    for j in range(trials):
        for i, width in enumerate(len_p):
            p = generate_prime(width)
            a, b = generate_curve_params(p, width)
            x, y = find_generator_point(a, b, p)

            start_time = time.time()
            ka, A = generate_keys((x, y), a, p)
            end_time = time.time()
            time_stamp[i][0] += end_time - start_time

            start_time = time.time()
            kb, B = generate_keys((x, y), a, p)
            end_time = time.time()
            time_stamp[i][1] += end_time - start_time

            start_time = time.time()
            R = double_and_add(ka, B, a, p)
            end_time = time.time()
            time_stamp[i][2] += end_time - start_time

    for i in range(3):
        for j in range(3):
            time_stamp[i][j] *= 1000 / trials

    print("+-----------------+-----------------------------------------------+")
    print("|                 |           Time-related performance            |")
    print("| Key Size (bits) |---------------+---------------+---------------+")
    print("|                 |       A       |       B       |       R       |")
    print("+-----------------+---------------+---------------+---------------+")
    for i in range(len(len_p)):
        print(f"|\t{len_p[i]}\t  |\t{time_stamp[i][0]:.3f}\t  |\t{time_stamp[i][1]:.3f}\t  |\t{time_stamp[i][2]:.3f}\t  |")
        print("+-----------------+---------------+---------------+---------------+")
    
if __name__ == "__main__":
    main()