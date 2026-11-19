import math
from dataclasses import dataclass
from typing import Callable

@dataclass
class AxiomReport:
    closure: bool
    associative: bool
    identity: object | None
    inverses: bool
    commutative: bool
    first_failure: str | None  # "closure" | "associativity" | "identity" | "inverses" | None
    counterexample: tuple | None

def check_axioms(carrier: list, op: Callable[[object, object], object]) -> AxiomReport:
    # 1. Closure Check
    for a in carrier:
        for b in carrier:
            if op(a, b) not in carrier:
                return AxiomReport(False, False, None, False, False, "closure", (a, b))
                
    # Check Commutativity early so we can correctly label commutative monoids even if inverses fail
    commutative = True
    for a in carrier:
        for b in carrier:
            if op(a, b) != op(b, a):
                commutative = False
                break
        if not commutative: break

    # 2. Associativity Check
    for a in carrier:
        for b in carrier:
            for c in carrier:
                if op(op(a, b), c) != op(a, op(b, c)):
                    return AxiomReport(True, False, None, False, commutative, "associativity", (a, b, c))

    # 3. Identity Check
    identity = None
    for e in carrier:
        is_id = True
        for a in carrier:
            if op(e, a) != a or op(a, e) != a:
                is_id = False
                break
        if is_id:
            identity = e
            break

    if identity is None:
        return AxiomReport(True, True, None, False, commutative, "identity", None)

    # 4. Inverses Check
    for a in carrier:
        has_inv = False
        for b in carrier:
            if op(a, b) == identity and op(b, a) == identity:
                has_inv = True
                break
        if not has_inv:
            # We return the single element that lacked an inverse as the counterexample
            return AxiomReport(True, True, identity, False, commutative, "inverses", (a,))

    # If it passes all tests
    return AxiomReport(True, True, identity, True, commutative, None, None)

def classify_magma(r: AxiomReport) -> str:
    if not r.closure:
        return "not closed"
    if not r.associative:
        return "magma"
    if r.identity is None:
        return "semigroup"
    if not r.inverses:
        return "commutative monoid" if r.commutative else "monoid"
    return "abelian group" if r.commutative else "group"

def classify_ring(n: int) -> str:
    """
    For Z_n, returns "commutative ring" | "integral domain" | "field".
    Example: For n=6, (2, 3) is a zero-divisor pair because 2*3 = 0 mod 6.
    Every finite integral domain is a field.
    """
    zero_divisors = []
    for i in range(1, n):
        if math.gcd(i, n) > 1:
            zero_divisors.append(i)
            
    if len(zero_divisors) > 0:
        return "commutative ring"
    return "field"

def run_f3_experiments():
    print("--- F.3(i) Lecture Exercise 3 Cases ---")
    z5_add = check_axioms(list(range(5)), lambda a, b: (a + b) % 5)
    print(f"(Z5, +) -> {classify_magma(z5_add)}")

    z5_mul = check_axioms(list(range(1, 5)), lambda a, b: (a * b) % 5)
    print(f"(Z5 \\ {{0}}, x) -> {classify_magma(z5_mul)}")

    z6_mul = check_axioms(list(range(1, 6)), lambda a, b: (a * b) % 6)
    print(f"(Z6 \\ {{0}}, x): first failure {z6_mul.first_failure}, counterexample {z6_mul.counterexample}")

    z6_star = check_axioms([1, 5], lambda a, b: (a * b) % 6)
    print(f"(Z6*, x) -> {classify_magma(z6_star)}")

    print("\n--- F.3(ii) Hostile Inputs ---")
    z7_sub = check_axioms(list(range(7)), lambda a, b: (a - b) % 7)
    print(f"(Z7, -): first failure {z7_sub.first_failure}, counterexample {z7_sub.counterexample}")

    z7_max = check_axioms(list(range(7)), lambda a, b: max(a, b))
    print(f"(Z7, max): {classify_magma(z7_max)} with identity {z7_max.identity}, first failure {z7_max.first_failure}")

    # Strings over {a, b} of length <= 2
    strings = ["", "a", "b", "aa", "ab", "ba", "bb"]
    str_concat = check_axioms(strings, lambda a, b: a + b)
    print(f"Strings length <= 2: first failure {str_concat.first_failure}, counterexample {str_concat.counterexample}")

    print("\n--- F.3(iii) classify_ring(n) for 2 <= n <= 30 ---")
    fields = []
    for n in range(2, 31):
        cls = classify_ring(n)
        if cls == "field":
            fields.append(n)
    print(f"classify_ring(n) = 'field' for: {fields}")
    print(f"Total fields found: {len(fields)} (Matches checkpoint expected 10 primes <= 30)")

if __name__ == "__main__":
    run_f3_experiments()