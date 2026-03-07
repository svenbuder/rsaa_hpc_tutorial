import time
from multiprocessing import Pool
import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt

def monte_carlo_pi_worker(n_samples):
    rng = np.random.default_rng()
    x = rng.random(n_samples)
    y = rng.random(n_samples)
    inside = np.sum(x * x + y * y <= 1.0)
    return inside

def run_case(nproc, total_samples):
    samples_per_worker = total_samples // nproc
    worker_samples = [samples_per_worker] * nproc

    start = time.perf_counter()
    with Pool(processes=nproc) as pool:
        inside_counts = pool.map(monte_carlo_pi_worker, worker_samples)
    runtime = time.perf_counter() - start

    total_inside = sum(inside_counts)
    total_used = samples_per_worker * nproc
    pi_estimate = 4.0 * total_inside / total_used
    return runtime, pi_estimate

if __name__ == "__main__":
    cpu_counts = [1, 2, 4, 8]
    total_samples = 8000000

    runtimes = []
    pi_estimates = []

    print("Running scaling test")
    print("Total samples per test:", total_samples)

    for nproc in cpu_counts:
        runtime, pi_estimate = run_case(nproc, total_samples)
        runtimes.append(runtime)
        pi_estimates.append(pi_estimate)
        print(f"{nproc} CPU(s): runtime = {runtime:.3f} s, pi = {pi_estimate:.6f}")

    runtimes = np.array(runtimes)
    speedup = runtimes[0] / runtimes
    ideal_speedup = np.array(cpu_counts, dtype=float)

    with open("output/scaling_results.txt", "w") as f:
        f.write("# cpus runtime_seconds speedup pi_estimate\n")
        for nproc, runtime, s, pi_estimate in zip(cpu_counts, runtimes, speedup, pi_estimates):
            f.write(f"{nproc:2d} {runtime:12.6f} {s:10.4f} {pi_estimate:10.6f}\n")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(cpu_counts, runtimes, marker="o")
    ax.set_xlabel("Number of CPUs")
    ax.set_ylabel("Runtime [s]")
    ax.set_title("Scaling test: runtime")
    fig.savefig("output/scaling_runtime.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(cpu_counts, speedup, marker="o", label="Measured speed-up")
    ax.plot(cpu_counts, ideal_speedup, linestyle="--", label="Ideal speed-up")
    ax.set_xlabel("Number of CPUs")
    ax.set_ylabel("Speed-up relative to 1 CPU")
    ax.set_title("Scaling test: speed-up")
    ax.legend()
    fig.savefig("output/scaling_speedup.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    print("Created output/scaling_results.txt")
    print("Created output/scaling_runtime.png")
    print("Created output/scaling_speedup.png")
