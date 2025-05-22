# Quantum Riichi Mahjong: Qiskit Simulation & Oracle

## Project Overview

This project implements a **quantum-enhanced simulation of Riichi Mahjong hand evaluation** and decision-making using [Qiskit](https://qiskit.org/) and classical/quantum hybrid algorithms. It features:

* **Quantum circuits for checking meld/pair completeness (tenpai).**
* **Trajectory simulation for quantum draw/discard operations.**
* **Win probability estimation using actual quantum hardware or simulators.**
* **Score and EV calculation using classical Python.**
* **Flexible code generation for quantum oracles and stepwise trajectory logic.**

The framework is **modular**, allowing you to build and test quantum strategies for Riichi Mahjong with hands of 13 or 14 tiles, analyze expected value, and even run jobs on IBM Quantum computers with 127+ qubits.

---

## Table of Contents

* [Project Overview](#project-overview)
* [Directory & File Structure](#directory--file-structure)
* [How it Works](#how-it-works)

  * [1. Quantum Oracle Generation](#1-quantum-oracle-generation)
  * [2. Trajectory Code Generation](#2-trajectory-code-generation)
  * [3. Utility Functions](#3-utility-functions)
  * [4. Score Calculation](#4-score-calculation)
  * [5. Running Quantum Jobs](#5-running-quantum-jobs)
* [Usage Instructions](#usage-instructions)

  * [A. Environment Setup](#a-environment-setup)
  * [B. Generating Oracles & Trajectories](#b-generating-oracles--trajectories)
  * [C. Running Quantum Experiments](#c-running-quantum-experiments)
  * [D. Classical EV/Score Calculation](#d-classical-evscore-calculation)
* [Extending the Project](#extending-the-project)
* [Technical Notes](#technical-notes)
* [References](#references)
* [License](#license)

---

## Directory & File Structure

```
.
├── utils.py                # Tile operations, hand parsing, shanten, ukeire, pretty output
├── oracle_codegen.py       # Code generator for meld/pair quantum oracle (Qiskit code output)
├── score_calculator.py     # Full hand scoring, yaku, fu, han, point calculation
├── trajectory_codegen.py   # Code generator for quantum trajectory circuits (draw/discard)
├── run.py                  # Sample Qiskit runner: sends circuit to IBMQ or simulator
```

---

## How it Works

### 1. Quantum Oracle Generation (`oracle_codegen.py`)

* **Purpose:** Generates a Qiskit Python file defining a *meld/pair quantum oracle* that can check if a hand is tenpai (complete) using only quantum gates and minimal ancilla.
* **How:**

  * Each tile is encoded with 3 qubits (up to 4 copies per tile, so 0-3).
  * The oracle checks for pairs, triplets (koutsu), and sequences (shuntsu) by manipulating ancilla qubits.
  * If the hand matches the win condition, a `flag` qubit is flipped for measurement.
* **Extensibility:** You can generate custom oracles by changing parameters like hand size, tile count, etc.

### 2. Trajectory Code Generation (`trajectory_codegen.py`)

* **Purpose:** Generates Qiskit code to simulate *one step of quantum draw and discard*, fully in superposition.
* **How:**

  * Uses registers for the hand (as above), draw (which tile is drawn), and discard (which tile is removed).
  * Applies Hadamard gates to put the draw/discard registers in superposition.
  * For each possible draw/discard, conditionally increments/decrements the tile counts in the hand.
  * Calls the meld/pair oracle, and measures if the resulting hand is tenpai.
* **Extension:** The approach can be extended to multi-step lookahead by nesting the logic (though this quickly becomes exponential in complexity).

### 3. Utility Functions (`utils.py`)

* **Purpose:** Provides helper functions for:

  * Tile encoding/decoding, pretty-printing
  * Shanten calculation (how far from complete)
  * Ukeire (effective tiles to progress)
  * Hand parsing from human-readable notation (like `123m456p789s11z`)
  * Data preparation for quantum/classical models
* **Performance:** Uses `@lru_cache` for memoized recursive functions (like shanten, meld detection) for speed.

### 4. Score Calculation (`score_calculator.py`)

* **Purpose:** Fully classical calculation of Mahjong hand score, including:

  * Yaku (hand value)
  * Han (doubles)
  * Fu (minipoints)
  * Final point value
* **Extra:** Detects all major yakus (including yakuman), handles melds, win tiles, dora, and special rules.
* **Extensibility:** Can be used standalone for any hand, or as a post-processing step after quantum circuit simulation.

### 5. Running Quantum Jobs (`run.py`)

* **Purpose:** Submits generated Qiskit circuits (from trajectory/oracle code) to IBMQ or local simulators.
* **How:**

  * Loads IBMQ credentials and selects a backend with enough qubits (e.g., 127-qubit Eagle processors).
  * Runs the quantum circuit, fetches measurement results, and prints empirical tenpai/win rates.
  * Can switch to the local `qasm_simulator` backend for fast, free testing.
* **User Customization:** You must set up your hand's initial state in the quantum circuit (see comments in code).

---

## Usage Instructions

### A. Environment Setup

1. **Install Qiskit and requirements:**

   ```bash
   pip install qiskit numpy tqdm
   ```
2. **Set up IBM Quantum account** *(optional, for real hardware)*:

   * Create an account at [https://quantum-computing.ibm.com/](https://quantum-computing.ibm.com/)
   * Save your token with:

     ```python
     from qiskit import IBMQ
     IBMQ.save_account('YOUR_API_TOKEN', overwrite=True)
     ```

### B. Generating Oracles & Trajectories

1. **Generate a meld/pair oracle:**

   ```bash
   python oracle_codegen.py
   ```

   * This creates `oracle.py` for your hand size/tile config.

2. **Generate a 1-step trajectory circuit:**

   ```bash
   python trajectory_codegen.py
   ```

   * This outputs `trajectory.py`, importing the oracle and building the full quantum circuit for 1 draw/discard step.

### C. Running Quantum Experiments

1. **Customize your hand in `trajectory.py` or similar:**

   * Add X gates to set your initial hand state as comments show, e.g.:

     ```python
     qc.x(hand[0])  # Set tile 0 present in hand
     ```
2. **Run the job using `run.py`:**

   * For IBMQ hardware (if you have access and enough credits):

     ```bash
     python run.py
     ```
   * For the simulator, uncomment the relevant lines and comment out the IBMQ section in `run.py`:

     ```python
     backend = Aer.get_backend('qasm_simulator')
     job = execute(qc, backend, shots=4096)
     ```
   * View win rates in the printed output!

### D. Classical EV/Score Calculation

* Use `ScoreCalculator` from `score_calculator.py` to evaluate hand value, yakus, han, fu, and final points after quantum simulation.
* Combine quantum win probability with classical score to compute **expected value (EV)** for different discards or strategies.

---

## Extending the Project

* **Multi-step Trajectories:** Extend `trajectory_codegen.py` to more steps (more registers for multiple draws/discards).
* **Custom Oracles:** Edit or extend `oracle_codegen.py` for other win conditions, hand types, or partial hand checking (e.g., specific yakus).
* **Integration:** Use `utils.py` functions for AI agents, classical Monte Carlo simulations, or hybrid quantum-classical evaluations.
* **Visualization:** Add pretty printing or graphical outputs for hand histories, win paths, or EV curves.

---

## Technical Notes

* **Qubit Count:** Each tile uses 3 qubits for its count (0-3), total 34 tile types → 102 qubits for hand representation, plus ancilla/flag.
* **Quantum Circuit Complexity:** Multi-step lookahead is exponential, but can be efficient for single or few-step trajectories.
* **Quantum-Classic Boundary:** Only the oracle and trajectory logic are quantum; score calculation and EV aggregation are classical.

---

## References

* [Qiskit Documentation](https://qiskit.org/documentation/)
* Riichi Mahjong rules and scoring resources (see [Japanese Mahjong Wiki](https://riichi.wiki/Main_Page))
* [IBM Quantum](https://quantum-computing.ibm.com/)

---

## License

This project is provided for academic, research, and personal use. Please cite if used in publications or further projects!
Contributions welcome. Hug hug\~
