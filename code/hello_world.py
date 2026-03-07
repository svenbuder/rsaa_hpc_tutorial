import time

print("Hello from the HPC cluster!")

for i in range(5):
    print(f"Step {i}")
    time.sleep(2)

print("Done")
