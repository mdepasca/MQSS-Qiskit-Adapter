# Inverse Unitary Test
# We put our initial state to |011> and then apply unitaries.
# Then we apply the unitaries again in reverse and should get the state |011> in a noiseless system but on a real hardware we would likely get some hits in the other states too.
# This example highlights the difference between running a problem on a noiseless simulator (QLM) vs an actual hardware (e.g., QExa20)

from mqss.qiskit_adapter import MQSSQiskitAdapter
import os
from dotenv import load_dotenv
from qiskit import QuantumCircuit
import numpy as np
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram

# Loading variables from the .env file

load_dotenv()  # reads .env if present
token = os.getenv("MQP_TOKEN")
backend_name = os.getenv("MQP_BACKEND")

# Initialize MQSS adapter and get backend

adapter = MQSSQiskitAdapter(token=token)
backend = adapter.get_backend(backend_name)

n = 3  # number of qubits
x = 3  # input state |011>

qc = QuantumCircuit(n)

# Prepare basis state |x⟩
for i in range(n):
    if (x >> i) & 1:
        qc.x(i)

# --- Unitaries ---
for qubit in range(n):
    qc.h(qubit)
    for target in range(qubit + 1, n):
        qc.crz(np.pi / 2 ** (target - qubit), qubit, target)

# --- Inverse Unitaries ---
for qubit in reversed(range(n)):
    for target in reversed(range(qubit + 1, n)):
        qc.crz(-np.pi / 2 ** (target - qubit), qubit, target)
    qc.h(qubit)

qc.measure_all()

# Run the job
job = backend.run(qc, shots=200, qasm3=False, queued=True)
counts = job.result().get_counts()
print("results:", counts)

# Visualization 
plot_histogram(counts)
plt.show()