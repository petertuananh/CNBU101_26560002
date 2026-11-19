from dataclasses import dataclass

class NotInvertibleError(Exception):
    pass

def gcd(a: int, b: int) -> int:
    """
    Tính ước chung lớn nhất của a và b.
    Quy ước: gcd(0, 0) trả về 0. 
    Lý do: Trong đại số, ước chung lớn nhất d của a và b thỏa mãn d|a và d|b. 
    Mọi số nguyên đều chia hết 0, do đó ước lớn nhất chia hết cả 0 và 0 chính là 0.
    """
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a

def egcd(a: int, b: int) -> tuple[int, int, int]:
    """Trả về (g, x, y) sao cho a*x + b*y = g."""
    if a == 0 and b == 0:
        return (0, 0, 0)
    
    sign_a = 1 if a >= 0 else -1
    sign_b = 1 if b >= 0 else -1
    a_abs, b_abs = abs(a), abs(b)
    
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b_abs:
        q, a_abs, b_abs = a_abs // b_abs, b_abs, a_abs % b_abs
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
        
    return a_abs, x0 * sign_a, y0 * sign_b

@dataclass
class Step:
    q: int
    r: int
    x: int
    y: int

def egcd_trace(a: int, b: int, check: bool = True) -> list[Step]:
    """Theo dõi từng bước của Extended Euclid."""
    a_orig, b_orig = a, b
    x0, y0, x1, y1 = 1, 0, 0, 1
    trace = []
    
    while b:
        q, r = divmod(a, b)
        a, b = b, r
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
        
        step = Step(q=q, r=r, x=x1, y=y1)
        trace.append(step)
        
        if check:
            assert r == a_orig * x1 + b_orig * y1, f"Check failed: {r} != {a_orig}*{x1} + {b_orig}*{y1}"
            
    return trace

def inverse(a: int, n: int) -> int:
    """Tính nghịch đảo của a modulo n."""
    g, x, _ = egcd(a, n)
    if g != 1:
        raise NotInvertibleError(f"[{a}] is not invertible mod {n} (gcd = {g}).")
    return x % n

def steps(a: int, b: int) -> int:
    """Đếm số bước phép chia."""
    a, b = abs(a), abs(b)
    count = 0
    while b:
        a, b = b, a % b
        count += 1
    return count

if __name__ == "__main__":
    print("--- CHECKPOINT TASK B.2 ---")
    print(f"egcd(252, 198) = {egcd(252, 198)}")
    print(f"egcd(101, 23) = {egcd(101, 23)}")
    print(f"inverse(23, 101) = {inverse(23, 101)}")
    
    try:
        inverse(2, 8)
    except NotInvertibleError as e:
        print(f"inverse(2, 8) raises NotInvertibleError: {e}")
        
    print(f"steps(34, 21) = {steps(34, 21)}")