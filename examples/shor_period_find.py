# Shor period finding example

# Find period of **f(x) = 13^x mod 15**

# load packages and enable backend

from mqss.qiskit_adapter import MQSSQiskitAdapter
from qiskit import QuantumCircuit, transpile, QuantumRegister, ClassicalRegister

import math
import matplotlib.pyplot as plt

token = "<token>"
adapter = MQSSQiskitAdapter(token=token)
[backend] = adapter.backends(name="<backend")


# Set the parameters

n = 4  # x is an n-bit number; feel free to change it, n>=2 must hold
shots = 200  # number of shots per run

# Define function


def f(x):
    return pow(13, x, 15)


# Generate circuit

qr_x = QuantumRegister(n, "x")
qr_fx = QuantumRegister(4, "f(x)")
cr_x = ClassicalRegister(n, "c_x")
qc = QuantumCircuit(qr_x, qr_fx, cr_x)
# equal superposition
for q in range(n):
    qc.h(qr_x[q])
qc.barrier()
# f(x) = 13^x mod 15
qc.x(qr_fx[0])
qc.x(qr_fx[2])
qc.x(qr_x[0])
qc.ccx(qr_x[0], qr_x[1], qr_fx[0])
qc.x(qr_x[0])
qc.ccx(qr_x[0], qr_x[1], qr_fx[1])
qc.x(qr_x[0])
qc.x(qr_x[1])
qc.ccx(qr_x[0], qr_x[1], qr_fx[2])
qc.x(qr_x[0])
qc.ccx(qr_x[0], qr_x[1], qr_fx[3])
qc.x(qr_x[1])
qc.barrier()
# QFT
for q in range(n - 1, -1, -1):
    qc.h(q)
    for k in range(1, q + 1):
        qc.cp(math.pi / 2**k, q - k, q)
    qc.barrier()
for q in range(n // 2):
    qc.swap(q, (n - 1) - q)
qc.barrier()

# This should ALWAYS give k*2^n/4, where k>=0 is a random integer.
# It's because the period of f(x) is 4, which is a power of 2.
qc.measure(qr_x, cr_x)

# Draw circuit

qc.draw(scale=0.5, output="mpl")

# Run circuit on hardware

result = backend.run(qc, shots=shots, optimization_level=3).result()

counts = result.get_counts()

print(f"Result counts: {counts}")  # e.g. for n=4 1100 is 12, which is 3*2^4/4

# Plotting the results

# plotting:
x = list(counts.keys())
x_values = []
for item in x:
    x_values.append(int(item, 2))
y = list(counts.values())
y = [i / sum(y) for i in y]

x_values_sorted, y_sorted = zip(*sorted(zip(x_values, y)))

fig = plt.figure()
plt.grid(zorder=0, axis="y", linestyle="--")
plt.bar(x=x, height=y_sorted, zorder=3)
locs, labels = plt.xticks()
plt.xticks(locs, x_values_sorted, rotation=65)
plt.ylabel("Probabilities")
plt.xlabel("x")

plt.show()
