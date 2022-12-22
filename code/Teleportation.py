from qiskit import QuantumRegister,ClassicalRegister,QuantumCircuit
from qiskit import Aer,IBMQ
from qiskit.visualization import plot_bloch_multivector
from qiskit.extensions import Initialize
from qiskit_textbook.tools import random_state

def create_bell_pair(qc ,q1 ,q2):
  qc.h(q1)
  qc.cx(q1,q2)

def alise_gate(qc ,q1 ,q2):
  qc.cx(q1,q2)
  qc.h(q1)

def measure_and_send(qc, q1, q2):
  qc.measure(q1,0)
  qc.measure(q2,1)
  
def bob_gate(qc,qubit,crx,crz):
  qc.x(qubit).c_if(crx,1)
  qc.z(qubit).c_if(crz,1)
  
provider = IBMQ.load_account()
psi = random_state(1)
init_gate = Initialize(psi)
init_gate.lebel = "init"
qr = QuantumRegister(3,name="q")
crx = ClassicalRegister(1, name= "crx")
crz = ClassicalRegister(1, name= "crz")
qc = QuantumCircuit(qr,crx,crz)

plot_bloch_multivector(psi, filename='images/psi.png')

qc.append(init_gate, [0])
qc.barrier()

create_bell_pair(qc,1,2)
qc.barrier()

alise_gate(qc, 0, 1)
qc.barrier()

measure_and_send(qc, 0, 1)

bob_gate(qc,2,crx,crz)

qc.draw(output='mpl', filename='images/Teleportation.png')

sim = Aer.get_backend("aer_simulator")
qc.save_statevector()
out_vector = sim.run(qc).result().get_statevector()
plot_bloch_multivector(out_vector, filename='images/out_vector.png')








