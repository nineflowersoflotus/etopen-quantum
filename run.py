from qiskit import IBMQ, transpile
from qiskit.providers.ibmq import least_busy
from qiskit import Aer, execute
from trajectory import qc

# ---- SET YOUR HAND ----
# Example for a ready hand: 1m1m1m2m3m4m5m6m7m8m9mEEN
# Use X gates on the hand register as in the generated file, or insert like:
# for i in [0,3,6]: qc.x(hand[i])  # (Set as needed for your test)

# ---- Run on IBM Quantum (change backend if needed) ----
# (Comment this section out if only using simulator)

# IBMQ.save_account('YOUR_API_TOKEN', overwrite=True) # Do this only once
IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q')
backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= 127 and
                                       not x.configuration().simulator and x.status().operational==True))
print("Using backend:", backend.name())

transpiled = transpile(qc, backend, optimization_level=1)
job = backend.run(transpiled, shots=4096)
print("Job ID:", job.job_id())
result = job.result()
counts = result.get_counts()
print("Result counts:", counts)
if '1' in counts:
    print("Empirical tenpai 1-step win rate:", counts['1'] / sum(counts.values()))
else:
    print("No wins in sampled runs.")

# ---- Alternatively, run on simulator ----
# backend = Aer.get_backend('qasm_simulator')
# job = execute(qc, backend, shots=4096)
# result = job.result()
# counts = result.get_counts()
# print(counts)
# if '1' in counts:
#     print("Empirical win rate:", counts['1'] / sum(counts.values()))
