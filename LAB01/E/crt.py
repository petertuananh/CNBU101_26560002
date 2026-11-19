import math
import time

class InconsistentSystemError(Exception):
    pass

def egcd(a: int, b: int) -> tuple[int, int, int]:
    """Extended Euclidean Algorithm."""
    a_abs, b_abs = abs(a), abs(b)
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b_abs:
        q, a_abs, b_abs = a_abs // b_abs, b_abs, a_abs % b_abs
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a_abs, x0 * (1 if a >= 0 else -1), y0 * (1 if b >= 0 else -1)

def crt_coprime(residues: list[int], moduli: list[int]) -> int:
    """Solves CRT when all moduli are pairwise coprime."""
    N = math.prod(moduli)
    
    # Check pairwise coprime
    for i in range(len(moduli)):
        for j in range(i + 1, len(moduli)):
            if math.gcd(moduli[i], moduli[j]) != 1:
                raise ValueError("Moduli are not pairwise coprime.")
                
    result = 0
    for a, n in zip(residues, moduli):
        M = N // n
        _, u, _ = egcd(M, n)
        result = (result + a * M * u) % N
    return result

def crt_general(residues: list[int], moduli: list[int]) -> tuple[int, int]:
    """Solves general CRT with potentially non-coprime moduli."""
    x = 0
    m = 1
    for a, n in zip(residues, moduli):
        # We need to solve: x + k*m = a (mod n) => k*m = (a - x) (mod n)
        d, u, _ = egcd(m, n)
        if (a - x) % d != 0:
            raise InconsistentSystemError(f"Inconsistent congruences at mod {n}")
        
        # Divide congruence by d
        m_prime = m // d
        n_prime = n // d
        target = (a - x) // d
        
        # k = (target * inverse(m')) mod n'
        k = (target * u) % n_prime
        
        x = x + k * m
        m = (m * n) // d # Update modulo to lcm(m, n)
        x = x % m
        
    return x, m

def crt_map(x: int, moduli: list[int]) -> tuple[int, ...]:
    """Maps an integer x to its residues."""
    return tuple(x % n for n in moduli)

def is_ring_iso(N: int, moduli: list[int]) -> bool:
    """Checks if the mapping Z_N -> Z_n1 x Z_n2 is a ring isomorphism."""
    if N != math.prod(moduli):
        return False
        
    # 1. Check Bijective (Injective + Surjective on finite sets)
    mapped = set(crt_map(x, moduli) for x in range(N))
    if len(mapped) != N:
        return False
        
    # 2. Check Homomorphism (Preserves Addition and Multiplication)
    for x in range(N):
        for y in range(N):
            m_x = crt_map(x, moduli)
            m_y = crt_map(y, moduli)
            m_xy_add = crt_map((x + y) % N, moduli)
            m_xy_mul = crt_map((x * y) % N, moduli)
            
            for i in range(len(moduli)):
                if m_xy_add[i] != (m_x[i] + m_y[i]) % moduli[i]:
                    return False
                if m_xy_mul[i] != (m_x[i] * m_y[i]) % moduli[i]:
                    return False
    return True

def run_rsa_crt_experiment():
    """Task E.3 (c): Timing modpow vs RSA-CRT"""
    # Import locally to avoid dependency failure if sympy isn't installed
    try:
        from sympy import randprime
    except ImportError:
        print("sympy not installed, skipping RSA-CRT timing experiment.")
        return

    # Generate 512-bit primes for a 1024-bit modulus
    p = randprime(2**511, 2**512)
    q = randprime(2**511, 2**512)
    N = p * q
    
    # Dummy e and compute valid d
    e = 65537
    phi = (p - 1) * (q - 1)
    _, d, _ = egcd(e, phi)
    d = d % phi
    
    c = 12345678901234567890 # Arbitrary ciphertext
    
    # 1. Direct Evaluation
    start_dir = time.perf_counter()
    for _ in range(100): # run multiple times to average out noise
        m_dir = pow(c, d, N)
    time_dir = time.perf_counter() - start_dir
    
    # 2. RSA-CRT Evaluation
    start_crt = time.perf_counter()
    for _ in range(100):
        dp = d % (p - 1)
        dq = d % (q - 1)
        mp = pow(c, dp, p)
        mq = pow(c, dq, q)
        m_crt = crt_coprime([mp, mq], [p, q])
    time_crt = time.perf_counter() - start_crt
    
    assert m_dir == m_crt, "RSA-CRT produced wrong decryption!"
    print(f"Direct time (100 ops): {time_dir:.4f}s")
    print(f"CRT time (100 ops):    {time_crt:.4f}s")
    print(f"Speed-up factor:       {time_dir / time_crt:.2f}x (Expected ~4x)")

if __name__ == "__main__":
    print("--- E.2 CHECKPOINT ---")
    print(f"crt_coprime([1,2,3], [4,5,7]) = {crt_coprime([1, 2, 3], [4, 5, 7])}")
    print(f"crt_general([3,5], [4,6]) = {crt_general([3, 5], [4, 6])}")
    
    try:
        crt_general([1, 2], [4, 6])
    except InconsistentSystemError as e:
        print(f"crt_general([1,2], [4,6]) Error: {e}")
        
    print(f"is_ring_iso(6, [2,3]) = {is_ring_iso(6, [2, 3])}")
    print(f"is_ring_iso(4, [2,2]) = {is_ring_iso(4, [2, 2])}")

    print("\n--- E.3 TOY RSA & EXPERIMENT ---")
    # Toy RSA check
    p, q, d, c = 5, 11, 27, 8
    mp = pow(c, d % (p-1), p)
    mq = pow(c, d % (q-1), q)
    m = crt_coprime([mp, mq], [p, q])
    print(f"Toy RSA: mp = {mp}, mq = {mq}, combined m = {m}")
    
    run_rsa_crt_experiment()