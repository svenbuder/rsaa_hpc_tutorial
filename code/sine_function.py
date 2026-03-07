import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt

# Sine-function parameters
amplitude = 1.0
frequency = 1.0
phase = 0.0
offset = 0.0

# x and y values
x = np.linspace(0, 2*np.pi, 1000)
y = amplitude * np.sin(2*np.pi*frequency*x + phase) + offset

# Make figure
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(x, y, lw=2)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Sine function")

# Save figure
fig.savefig("output/sine_function.pdf", bbox_inches="tight")
fig.savefig("output/sine_function.png", dpi=300, bbox_inches="tight")

# Save parameters
with open("output/sine_parameters.txt", "w") as f:
    f.write(f"{amplitude}  # amplitude\n")
    f.write(f"{frequency}  # frequency\n")
    f.write(f"{phase}  # phase\n")
    f.write(f"{offset}  # offset\n")

print("Created output/sine_function.pdf")
print("Created output/sine_function.png")
print("Created output/sine_parameters.txt")

# Reading in what we just saved:
amplitude, frequency, phase, offset = np.loadtxt(
    "output/sine_parameters.txt",
    comments="#"
)
print("Loading output back in to show it works:")
print("amplitude, frequency, phase, offset")
print(amplitude, frequency, phase, offset)
