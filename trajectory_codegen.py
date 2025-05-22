import math

def generate_1step_trajectory(filename="trajectory.py", N=34, BITS=3):
    draw_bits = math.ceil(math.log2(N))
    discard_bits = math.ceil(math.log2(14))
    ANCILLA = 8

    with open(filename, "w") as f:
        f.write("from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister\n")
        f.write("from oracle_codegen import oracle\n")
        f.write(f"hand = QuantumRegister({N*BITS}, 'hand')\n")
        f.write("flag = QuantumRegister(1, 'flag')\n")
        f.write(f"draw = QuantumRegister({draw_bits}, 'draw')\n")
        f.write(f"discard = QuantumRegister({discard_bits}, 'discard')\n")
        f.write(f"anc = QuantumRegister({ANCILLA}, 'anc')\n")
        f.write("creg = ClassicalRegister(1, 'cflag')\n")
        f.write(f"qc = QuantumCircuit(hand, flag, draw, discard, anc, creg)\n\n")
        f.write("# -- Set your initial 13-tile hand below with X gates, e.g.: qc.x(hand[0])\n\n")
        f.write("qc.h(draw)\n")
        f.write("qc.h(discard)\n\n")
        # Controlled increment for draw
        f.write("# -- Controlled increment: for each tile t, if draw==t, increment hand[t] (only LSB)\n")
        for t in range(N):
            ctrl = ''.join([f"qc.x(draw[{i}])\n" if ((t>>i)&1)==0 else '' for i in range(draw_bits)])
            bits = [f"hand[{t*BITS+k}]" for k in range(BITS)]
            ctrlq = ','.join([f"draw[{i}]" for i in range(draw_bits)])
            f.write(ctrl)
            f.write(f"qc.mcx([{ctrlq}], {bits[0]})  # +1 to LSB if draw=={t}\n")
            for i in range(draw_bits):
                if ((t>>i)&1)==0:
                    f.write(f"qc.x(draw[{i}])\n")
        f.write("\n")
        # Controlled decrement for discard
        f.write("# -- Controlled decrement: for each tile t, if discard==t, decrement hand[t] (only LSB)\n")
        for t in range(N):
            ctrl = ''.join([f"qc.x(discard[{i}])\n" if ((t>>i)&1)==0 else '' for i in range(discard_bits)])
            bits = [f"hand[{t*BITS+k}]" for k in range(BITS)]
            ctrlq = ','.join([f"discard[{i}]" for i in range(discard_bits)])
            f.write(ctrl)
            f.write(f"qc.mcx([{ctrlq}], {bits[0]})  # -1 to LSB if discard=={t}\n")
            for i in range(discard_bits):
                if ((t>>i)&1)==0:
                    f.write(f"qc.x(discard[{i}])\n")
        f.write("\n")
        f.write("# -- Call meld/pair oracle --\n")
        f.write("qc.compose(oracle, qubits=qc.qubits[:oracle.num_qubits], inplace=True)\n")
        f.write("qc.measure(flag, creg[0])\n")
        f.write("print(qc)\n")

if __name__ == "__main__":
    generate_1step_trajectory()
