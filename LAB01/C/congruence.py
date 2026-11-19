def egcd(a: int, b: int) -> tuple[int, int, int]:
    """Helper function: Extended Euclidean Algorithm"""
    a_abs, b_abs = abs(a), abs(b)
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b_abs:
        q, a_abs, b_abs = a_abs // b_abs, b_abs, a_abs % b_abs
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1

    sign_a = 1 if a >= 0 else -1
    sign_b = 1 if b >= 0 else -1
    return a_abs, x0 * sign_a, y0 * sign_b


def solve_linear(a: int, b: int, n: int) -> list[int]:
    """All x in [0, n) with a*x = b (mod n), sorted ascending; [] if none."""
    d, x, _ = egcd(a, n)

    # 1. Condition for solvability: d must divide b
    if b % d != 0:
        return []

    # 2. Divide by d to find the unique solution modulo (n/d)
    a_prime = a // d
    b_prime = b // d
    n_prime = n // d

    # We need the inverse of a_prime modulo n_prime.
    # We can run egcd again for a_prime and n_prime.
    _, x_inv, _ = egcd(a_prime, n_prime)

    x0 = (x_inv * b_prime) % n_prime

    # 3. Generate all d solutions modulo n
    solutions = [(x0 + k * n_prime) for k in range(d)]
    return sorted(solutions)


def solve_linear_bf(a: int, b: int, n: int) -> list[int]:
    """Brute-force reference for tests."""
    return [x for x in range(n) if (a * x) % n == b % n]


# TASK C.3 EXPERIMENT: Counting solutions


def run_c3_experiment():
    N = 12
    solvable_pairs = 0
    total_solutions = 0

    for a in range(N):
        for b in range(N):
            solutions = solve_linear(a, b, N)
            if len(solutions) > 0:
                solvable_pairs += 1
            total_solutions += len(solutions)

    print("\n--- TASK C.3 EXPERIMENT (N=12) ---")
    print(f"Solvable pairs: {solvable_pairs}")
    print(f"Total solutions: {total_solutions}")


if __name__ == "__main__":
    print("--- CHECKPOINT TASK C.2 ---")
    print(f"solve_linear(7, 5, 26)  = {solve_linear(7, 5, 26)}")
    print(f"solve_linear(6, 4, 10)  = {solve_linear(6, 4, 10)}")
    print(f"solve_linear(6, 3, 10)  = {solve_linear(6, 3, 10)}")

    # Verify with brute force
    assert solve_linear(7, 5, 26) == solve_linear_bf(7, 5, 26)
    assert solve_linear(6, 4, 10) == solve_linear_bf(6, 4, 10)
    assert solve_linear(6, 3, 10) == solve_linear_bf(6, 3, 10)
    print("All brute-force checks passed!")

    run_c3_experiment()
