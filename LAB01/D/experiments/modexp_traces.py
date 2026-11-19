import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modexp import OpCounter, modpow_lr, modpow_ladder

def recover_exponent(trace: list[str]) -> int:
    """Recover the left-to-right exponent by parsing the trace string."""
    e = 0
    for op in trace:
        if op == 'S':
            e <<= 1
        elif op == 'M':
            e += 1
    return e

def run_trace_experiment():
    print("\n--- D.3 EXPERIMENT ---")
    lr_traces = set()
    ladder_traces = set()
    
    # 11-bit exponents e in [2^10, 2^11)
    for e in range(1024, 2048): 
        ops_lr = OpCounter()
        modpow_lr(2, e, 99, ops_lr)
        lr_traces.add("".join(ops_lr.trace))
        
        ops_ladder = OpCounter()
        modpow_ladder(2, e, 99, ops_ladder)
        ladder_traces.add("".join(ops_ladder.trace))
        
    print(f"(a) Distinct LR traces: {len(lr_traces)}") 
    # Bit đầu tiên luôn là '1' (sinh ra 'SM'). 
    # 10 bit còn lại có thể là '0' hoặc '1' độc lập, sinh ra 2^10 = 1024 chuỗi S và SM khác nhau.
    
    print(f"(a) Distinct Ladder traces: {len(ladder_traces)}") 
    # Thuật toán Ladder luôn thực hiện chính xác một phép nhân (M) 
    # và một phép bình phương (S) cho mỗi bit mà không phụ thuộc vào giá trị bit đó.
    
    # Test (b) recovery
    test_trace = OpCounter()
    test_e = 1337
    modpow_lr(2, test_e, 99, test_trace)
    recovered = recover_exponent(test_trace.trace)
    print(f"(b) Khôi phục số mũ LR (test_e = 1337): Thành công? {recovered == test_e} (Giá trị khôi phục được: {recovered})")

if __name__ == "__main__":
    run_trace_experiment()