"""Run TD learning experiments on Boolean gene regulatory networks."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from grn_td.boolean_network import (
    edge_functions,
    edge_functions_20,
    edge_functions_50,
    edge_functions_100,
    initial_values,
    initial_values_20,
    initial_values_50,
    initial_values_100,
    primes,
    primes_20,
    primes_50,
    primes_100,
    valid_action,
    valid_action_20,
    valid_action_50,
)
from grn_td.helper import compute_possible_targets
from grn_td.td_agent import TDAgent


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train a TD agent to steer a Boolean GRN toward target states."
    )
    parser.add_argument(
        "--network",
        choices=("7", "20", "50", "100"),
        default="20",
        help="Benchmark network size (default: 20).",
    )
    parser.add_argument(
        "--epsilon",
        type=float,
        default=0.1,
        help="Exploration rate for epsilon-greedy action selection.",
    )
    parser.add_argument(
        "--episodes",
        type=int,
        default=1000,
        help="Number of training episodes.",
    )
    return parser.parse_args()


NETWORK_CONFIG = {
    "7": (primes, edge_functions, valid_action, initial_values),
    "20": (primes_20, edge_functions_20, valid_action_20, initial_values_20),
    "50": (primes_50, edge_functions_50, valid_action_50, initial_values_50),
    "100": (primes_100, edge_functions_100, None, initial_values_100),
}


def main() -> None:
    args = parse_arguments()

    if args.network not in NETWORK_CONFIG:
        raise ValueError(f"Unsupported network size: {args.network}")

    primes, edge_functions, valid_action, initial_values = NETWORK_CONFIG[args.network]

    if args.network == "100":
        from grn_td.boolean_network import target_values_100

        target_values = target_values_100
    else:
        target_values = compute_possible_targets(valid_action, primes, edge_functions)

    agent = TDAgent(
        primes,
        edge_functions,
        target_values,
        initial_values,
        epsilon=args.epsilon,
    )
    agent.train(episodes=args.episodes)
    agent.print_comparison_summary()


if __name__ == "__main__":
    main()
