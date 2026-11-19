def wrap_add(x: int, y: int, w: int) -> int:
    """Mathematical addition in Z_{2^w}."""
    return (x + y) % (2**w)

def checked_add(x: int, y: int, w: int) -> int:
    """Addition that raises an error on overflow."""
    ans = x + y
    if ans >= (2**w):
        raise OverflowError("Integer overflow detected!")
    return ans

def vulnerable_check(h: int, p: int) -> bool:
    """Vulnerable check evaluating length in Z_256."""
    L = wrap_add(h, p, 8)
    return L <= 64

def safe_check(h: int, p: int) -> bool:
    """Safe check evaluated in Z avoiding overflow."""
    # Assuming valid sizes h >= 0, p >= 0 and maximum buffer 64
    if h > 64:
        return False
    return p <= 64 - h

if __name__ == "__main__":
    print("--- I.1 CHECKPOINT ---")
    h, p = 40, 230
    L = wrap_add(h, p, 8)
    accepted = vulnerable_check(h, p)
    print(f"(a) L = {L}, accepted = {accepted}, so the buffer overflows.")
    
    dangerous_pairs = 0
    for h_test in range(65): # h in [0, 64]
        for p_test in range(256): # p in [0, 255]
            if (h_test + p_test > 64) and vulnerable_check(h_test, p_test):
                dangerous_pairs += 1
                
    print(f"(b) Number of dangerous pairs: {dangerous_pairs}")