# Inverse Unitary Test
# We put our initial state to |011> and then apply unitaries.
# Then we apply the unitaries again in reverse and should get the state |001> again.
# This example highlights the difference between running a problem on a noiseless simulator vs an actual hardware

from mqss.qiskit_adapter import MQSSQiskitAdapter
from qiskit import QuantumCircuit
import numpy as np

# Connect to MQSS
adapter = MQSSQiskitAdapter("<token>")
backend = adapter.get_backend("<backend>")

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
from qiskit.visualization import plot_histogram

plot_histogram(counts)
