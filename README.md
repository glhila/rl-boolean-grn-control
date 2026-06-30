# Reinforcement Learning-Based Control Strategy for Boolean Gene Regulatory Networks

Reference implementation accompanying our CIBB 2026 paper on steering Boolean gene
regulatory networks (GRNs) toward desirable attractor states with reinforcement
learning. The codebase implements a temporal-difference (TD) agent with
value-function approximation, experience replay, and state aggregation.

This repository is published **separately** from the original course project at
[`michal-shoob/final-project`](https://github.com/michal-shoob/final-project).
It is intended for reproducibility and extension of the published work.

## Publication

> **Title:** Reinforcement Learning-Based Control Strategy for Boolean Gene Regulatory Networks  
> **Venue:** International Conference on Computational Intelligence Methods for Bioinformatics and Biostatistics (CIBB), 2026  
> **Authors:** Hillel Kugler, Avraham Raviv, Hila Glazz, Michal Shoob  
> **Paper:** _Link and DOI to be added upon publication_  
> **Preprint:** _Optional link_

If you use this code, please cite the paper and this repository (see
[`CITATION.cff`](CITATION.cff)).

## Abstract

The control problem in Boolean Gene Regulatory Networks (GRNs) is a central
challenge in computational biology, focusing on guiding biological systems
toward desired target states by determining suitable assignments for unknown
node states. The objective is not only to reach the target state, but to do so
in the most efficient manner, while minimizing changes in node states
throughout the network dynamics. However, as the size and complexity of the
network increases, the state space grows exponentially, making exhaustive
search approaches computationally infeasible. To address this challenge, this
work presents a scalable Reinforcement Learning (RL) framework based on
Temporal Difference (TD) learning. By integrating a Hybrid Decision Strategy,
Importance-Based State Aggregation, and a persistent external memory
architecture alongside cache optimization, our framework identifies optimal
control policies for networks with up to 50 nodes within 21 seconds. We
demonstrate that the use of a state-value V(s) representation, combined with
domain-specific heuristics, effectively navigates a large search space of
assignments while maintaining a bounded memory footprint.

## Requirements

- Python 3.10+
- Git
- A C compiler (recommended; `pyboolnet` may build from source)

## Installation

```bash
git clone https://github.com/glhila/rl-boolean-grn-control.git
cd rl-boolean-grn-control
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux / macOS
pip install -r requirements.txt
```

## Reproducing experiments

Train the TD agent on the default 20-node benchmark:

```bash
python experiments/run_experiment.py
```

Select a network size and training settings:

```bash
python experiments/run_experiment.py --network 50 --episodes 1000 --epsilon 0.1
python experiments/run_experiment.py --network 100 --episodes 1000
```

Supported `--network` values: `7`, `20`, `50`, `100`.

A thin wrapper is also available at the repository root:

```bash
python main.py --network 20 --epsilon 0.1
```

### Outputs

Experiment artifacts are written under `results/`:

| File | Description |
|------|-------------|
| `results/app.log` | Training and evaluation log |
| `results/td_agent_value_table.db` | Persisted value table (SQLite) |

Figures and tables from the paper can be regenerated from these logs and the
agent summary printed at the end of each run.

## Repository layout

```
.
├── grn_td/                     # Core library
│   ├── boolean_network.py      # Benchmark GRN definitions (BNET → primes)
│   ├── td_agent.py             # TD learning agent
│   ├── helper.py               # Target-state utilities
│   ├── logger_setup.py         # Shared logging configuration
│   └── paths.py                # Output directory paths
├── experiments/
│   └── run_experiment.py       # Main experiment entry point
├── archive/                    # Legacy exploratory scripts (not used in paper)
├── results/                    # Generated logs and databases (git-ignored)
├── CITATION.cff                # Citation metadata for software and paper
├── requirements.txt
└── main.py                     # Convenience wrapper around the experiment script
```

## Method overview

1. **Network model.** Each benchmark is defined in BNET format and converted to
   PyBoolNet `primes` using [`pyboolnet`](https://github.com/hklarner/pyboolnet).
   Some nodes are fixed, others are controllable (`None` in the initial state).
2. **Target selection.** For smaller networks, feasible target states are derived
   by forward simulation from the valid intervention set
   (`compute_possible_targets` in `grn_td/helper.py`).
3. **RL control.** `TDAgent` learns state values under synchronous updates,
   epsilon-greedy exploration, optional state aggregation, and experience replay.
   Training statistics and comparison metrics are reported via
   `print_comparison_summary()`.

See `grn_td/td_agent.py` and the paper for full algorithmic details.

## License

MIT (update if a different license applies to the published work).

## Contact

Hillel Kugler, Avraham Raviv, Hila Glazz, Michal Shoob — open an issue in
this repository or refer to the paper for correspondence details.
