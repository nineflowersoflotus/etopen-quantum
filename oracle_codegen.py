def generate_minimal_oracle(filename="oracle.py", N=34, BITS=3):
    """
    Generates a Qiskit file with a meld/pair oracle for a 14-tile hand.
    Includes triplets and sequences for suits, minimal ancilla usage.
    """
    ANCILLA = 8  # Pair+meld flags

    with open(filename, "w") as f:
        f.write("from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister\n")
        f.write(f"hand = QuantumRegister({N*BITS}, 'hand')\n")
        f.write("flag = QuantumRegister(1, 'flag')\n")
        f.write(f"anc = QuantumRegister({ANCILLA}, 'anc')\n")
        f.write("qc = QuantumCircuit(hand, flag, anc)\n\n")
        f.write("# -- Pair check (if any tile has 2, set anc[0])\n")
        f.write("for i in range(34):\n")
        f.write("    bits = [hand[i*3+0], hand[i*3+1], hand[i*3+2]]\n")
        f.write("    qc.ccx(bits[1], bits[0].__invert__(), anc[0])  # 2 = 010\n")
        f.write("# -- Triplets (counts==3, set anc[1]~anc[4])\n")
        f.write("for j,i in enumerate(range(34)):\n")
        f.write("    if j<4:\n")
        f.write("        bits = [hand[i*3+0], hand[i*3+1], hand[i*3+2]]\n")
        f.write("        qc.ccx(bits[0], bits[1], anc[1+j])\n")
        f.write("# -- Sequences (for suits only, sets anc[5]~anc[7])\n")
        f.write("for j,suit_start in enumerate([0,9,18]):\n")
        f.write("    for i in range(suit_start,suit_start+7):\n")
        f.write("        t0 = hand[i*3+0]\n")
        f.write("        t1 = hand[(i+1)*3+0]\n")
        f.write("        t2 = hand[(i+2)*3+0]\n")
        f.write("        if j<3:\n")
        f.write("            qc.ccx(t0, t1, anc[5+j])\n")
        f.write("            qc.ccx(anc[5+j], t2, anc[5+j])\n")
        f.write("# -- Win if: pair and any 4 melds (triplets/sequences), here just check triplets+pair (simple version)\n")
        f.write("qc.mct([anc[0], anc[1], anc[2], anc[3], anc[4]], flag[0])\n")
        f.write("\n")
        f.write("oracle = qc\n")

if __name__ == "__main__":
    generate_minimal_oracle()
