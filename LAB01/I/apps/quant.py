def clip(val: float, q_min: int, q_max: int) -> int:
    return max(q_min, min(q_max, int(val)))

def quantize(x: float, s: float, z: int) -> int:
    """Affine quantization to INT8."""
    return clip(round(x / s) + z, -128, 127)

def dequantize(q: int, s: float, z: int) -> float:
    """Dequantize back to real domain."""
    return s * (q - z)

def sat_add(a: int, b: int) -> int:
    """Saturating addition on [-128, 127]."""
    return clip(a + b, -128, 127)

if __name__ == "__main__":
    print("--- I.5 CHECKPOINT ---")
    
    # (a) Associativity failure counter-example
    a, b, c = 100, 100, -100
    left_side = sat_add(sat_add(a, b), c)
    right_side = sat_add(a, sat_add(b, c))
    print(f"(a) (a, b, c) = ({a}, {b}, {c}): left side {left_side}, right side {right_side}.")
    
    # (b) Maximum dequantization error
    s = 1 / 127
    z = 0
    max_error = 0.0
    
    # Test densely over [-1, 1]
    import numpy as np
    for x in np.linspace(-1, 1, 10000):
        q = quantize(x, s, z)
        x_hat = dequantize(q, s, z)
        error = abs(x - x_hat)
        if error > max_error:
            max_error = error
            
    print(f"(b) Max dequantization error: {max_error:.6f} (Expected bounded by s/2 = {s/2:.6f})")