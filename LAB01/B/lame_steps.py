import math
import random
import os
import matplotlib.pyplot as plt
import pandas as pd
from euclid import steps 

def run_lame_experiment():
    phi = (1 + math.sqrt(5)) / 2
    N_values = list(range(10, 2001, 10)) # N từ 10 đến 2000
    
    # Sinh trước mảng Fibonacci để giải quyết nhanh S(N) theo gợi ý Pitfall
    fibs = [1, 1]
    while fibs[-1] <= 2000:
        fibs.append(fibs[-1] + fibs[-2])
        
    records = []
    
    for N in N_values:
        # TÍNH MAX S(N): Lập luận từ B.1(c), trường hợp xấu nhất (số bước lớn nhất) 
        # đạt được tại cặp Fibonacci liên tiếp (F_{k+1}, F_k) lớn nhất <= N.
        max_pair = (1, 1)
        curr_max = 0
        for i in range(len(fibs) - 1):
            if fibs[i+1] <= N:
                curr_max = steps(fibs[i+1], fibs[i])
                max_pair = (fibs[i+1], fibs[i])
        
        # TÍNH AVERAGE: Random sampling 1000 cặp trong [1, N]^2
        samples = 1000
        total_steps = sum(steps(random.randint(1, N), random.randint(1, N)) for _ in range(samples))
        avg_steps = total_steps / samples
        
        records.append({
            "N": N,
            "log_phi_N": math.log(N, phi),
            "Max_Steps_S(N)": curr_max,
            "Avg_Steps": avg_steps,
            "Max_Pair": max_pair
        })
        
    df = pd.DataFrame(records)
    os.makedirs("data", exist_ok=True)
    os.makedirs("figures", exist_ok=True)
    df.to_csv("data/lame.csv", index=False)
    
    # Vẽ biểu đồ
    plt.figure(figsize=(10, 6))
    plt.plot(df["log_phi_N"], df["Max_Steps_S(N)"], label="Max Steps $S(N)$", color="red")
    plt.plot(df["log_phi_N"], df["Avg_Steps"], label="Average Steps", color="blue")
    plt.xlabel(r"$\log_\phi N$")
    plt.ylabel("Number of Division Steps")
    plt.title("Lamé's Theorem: Worst Case vs Average Case")
    plt.legend()
    plt.grid(True)
    plt.savefig("figures/lame.pdf")
    
    print("Dữ liệu đã được lưu vào 'data/lame.csv' và biểu đồ lưu vào 'figures/lame.pdf'.")

if __name__ == "__main__":
    run_lame_experiment()