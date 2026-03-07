import sys
import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt

array_index = int(sys.argv[1])

amplitude = 1.0
frequency = float(array_index)
phase = 0.0
offset = 0.0

x = np.linspace(0, 2 * np.pi, 1000)
y = amplitude * np.sin(2 * np.pi * frequency * x + phase) + offset

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(x, y, lw=2)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title(f"Sine function for array index {array_index}")

png_name = f"output/array_sine_{array_index}.png"
txt_name = f"output/array_sine_{array_index}.txt"

fig.savefig(png_name, dpi=300, bbox_inches="tight")
plt.close(fig)

with open(txt_name, "w") as f:
    f.write(f"{amplitude}  # amplitude\n")
    f.write(f"{frequency}  # frequency\n")
    f.write(f"{phase}  # phase\n")
    f.write(f"{offset}  # offset\n")

print(f"Created {png_name}")
print(f"Created {txt_name}")
