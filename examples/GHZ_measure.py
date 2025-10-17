# GHZ State generation and measurement

# Load packages + connect to device

from mqss.qiskit_adapter import MQSSQiskitAdapter
from qiskit import QuantumCircuit, transpile

token = "<token>"
adapter = MQSSQiskitAdapter(token=token)
[backend] = adapter.backends(name="<backend>")

# Set Parameters

# Pay attention `shots <= 200` for AQT20

# set number of qubits and measurement shots for the quantum circuit
qubits = 8
shots = 200
# Repetitions
rep = 2
meas = [0]

# Generate circuit

qc = QuantumCircuit(qubits, qubits)
qc.h(0)
for i in range(1, qubits):
    qc.cx(0, i)
qc.measure_all(add_bits=False)

# Transpile using Qiskit 'transpile'
# Comment out the these two lines if you are running on QLM
trans_qc = transpile(qc, backend, optimization_level=3)
job = backend.run(trans_qc, shots=shots, qasm3=True, queued=True)
# print(trans_qc)

# Run circuit on hardware

# ------- Use this if running on QLM backend ---------
# job = backend.run(qc, shots=shots, qasm3=False, queued=True)

counts = job.result().get_counts()
print("Result: ", counts)

# Visualize Results

from qiskit.visualization import plot_histogram

plot_histogram(counts, figsize=(12, 6))
