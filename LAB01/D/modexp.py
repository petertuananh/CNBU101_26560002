class OpCounter:
    def __init__(self):
        self.trace = []

    def sqr(self, x: int, n: int) -> int:
        self.trace.append("S")
        return (x * x) % n

    def mul(self, x: int, y: int, n: int) -> int:
        self.trace.append("M")
        return (x * y) % n

def handle_edge_cases(a: int, e: int, n: int):
    if n == 1:
        return 0  # a^0 mod 1 = 1 mod 1 = 0
    return None

def modpow_rl(a: int, e: int, n: int, ops: OpCounter | None = None) -> int:
    edge = handle_edge_cases(a, e, n)
    if edge is not None: return edge
    
    r, b, k = 1, a % n, e
    while k > 0:
        if k % 2 == 1:
            r = ops.mul(r, b, n) if ops else (r * b) % n
        if k > 1: # Không cần bình phương ở bước cuối cùng nếu k đã bằng 0
            b = ops.sqr(b, n) if ops else (b * b) % n
        k >>= 1
    return r

def modpow_lr(a: int, e: int, n: int, ops: OpCounter | None = None) -> int:
    edge = handle_edge_cases(a, e, n)
    if edge is not None: return edge
    if e == 0: return 1
    
    bits = bin(e)[2:]
    r = 1
    for bit in bits:
        r = ops.sqr(r, n) if ops else (r * r) % n
        if bit == '1':
            r = ops.mul(r, a, n) if ops else (r * a) % n
    return r

def modpow_ladder(a: int, e: int, n: int, ops: OpCounter | None = None) -> int:
    edge = handle_edge_cases(a, e, n)
    if edge is not None: return edge
    if e == 0: return 1
    
    bits = bin(e)[2:]
    R0, R1 = 1, a % n
    for bit in bits:
        # Thực hiện phép nhân trước phép bình phương ở cả 2 nhánh
        if bit == '0':
            prod = ops.mul(R0, R1, n) if ops else (R0 * R1) % n
            sq = ops.sqr(R0, n) if ops else (R0 * R0) % n
            R0, R1 = sq, prod
        else:
            prod = ops.mul(R0, R1, n) if ops else (R0 * R1) % n
            sq = ops.sqr(R1, n) if ops else (R1 * R1) % n
            R0, R1 = prod, sq
    return R0

if __name__ == "__main__":
    import random
    
    print("--- D.2 CHECKPOINT ---")
    print(f"RL: {modpow_rl(5, 13, 17)} | LR: {modpow_lr(5, 13, 17)} | Ladder: {modpow_ladder(5, 13, 17)}")
    
    errors = 0
    for _ in range(2000):
        a, e, n = random.randint(1, 1000), random.randint(0, 1000), random.randint(1, 1000)
        expected = pow(a, e, n)
        if not (modpow_rl(a, e, n) == expected and modpow_lr(a, e, n) == expected and modpow_ladder(a, e, n) == expected):
            errors += 1
    print(f"Property tests against built-in pow() completed. Errors: {errors}")