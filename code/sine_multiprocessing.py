import sys
from multiprocessing import Pool
import numpy as np

def evaluate_task(task):
    task_id, amplitude, frequency, phase = task
    x = np.linspace(0.0, 2.0 * np.pi, 200000)
    y = amplitude * np.sin(2.0 * np.pi * frequency * x + phase)
    summary = np.trapz(np.abs(y), x)
    return task_id, amplitude, frequency, phase, summary

if __name__ == "__main__":
    ncpu = int(sys.argv[1])

    tasks = []
    task_id = 1
    for amplitude in [0.5, 1.0, 1.5]:
        for frequency in [0.5, 1.0, 2.0]:
            for phase in [0.0, np.pi / 4.0]:
                tasks.append((task_id, amplitude, frequency, phase))
                task_id += 1

    print(f"Running {len(tasks)} tasks with {ncpu} worker processes")

    with Pool(processes=ncpu) as pool:
        results = pool.map(evaluate_task, tasks)

    with open("output/sine_evaluations_multiprocessing.txt", "w") as f:
        f.write("# task_id amplitude frequency phase integral_abs_y\n")
        for row in results:
            f.write(
                f"{row[0]:2d} {row[1]:6.2f} {row[2]:6.2f} {row[3]:10.5f} {row[4]:.8f}\n"
            )

    print("Created output/threaded_sine_scan_results.txt")
