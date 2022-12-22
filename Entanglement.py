from qiskit import IBMQ, Aer, execute, QuantumCircuit
from qiskit.visualization import plot_histogram 
provider = IBMQ.load_account()
qc = QuantumCircuit(2,2)
qc.h(0)
qc.cx(0,1)
qc.measure(range(2),range(2))
qc.draw(output='mpl', filename='my_circuit.png')
backend = Aer.get_backend('qasm_simulator')
job_simulator = execute(qc,backend,shots=1000)
result_simulator = job_simulator.result()
count = result_simulator.get_counts(qc)
print(count)
plot_histogram(count, filename='my_plot.png')
