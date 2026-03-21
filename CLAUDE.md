# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Research codebase for an article on an extended dialog model. It simulates two-party dialogs (Alice and Bob) where each actor has **resistance** (tendency to maintain their position) and **persuasion** (ability to change the other's position) parameters. The model tracks how preferences over three options (vA, vB, valt) evolve over dialog iterations using transition matrices.

## Setup & Running

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook simulations.ipynb
```

## Architecture

The code has a three-layer pipeline: **persuasion.py → dialog_logic.py → helpers.py**

- **`persuasion.py`** — Top-level module (import this). Creates `Actor` objects, builds 9×9 transition matrices from resistance/persuasion parameters via `choice_probabilities()`, and runs simulations via `engage_in_dialog()`.
- **`dialog_logic.py`** — Core dialog engine. `communicate()` iteratively applies the transition matrix to a joint preference matrix (outer product of actor preferences), then marginalizes to extract updated individual preferences.
- **`helpers.py`** — Plotting (`plot_one`, `plot_side_by_side`) and display utilities. Saves figures to `.output/`. Uses matplotlib with grayscale stacked area charts.
- **`simulations.ipynb`** — Jupyter notebook with scenarios (e.g., "both persuasive and resistant", "strong leader vs follower"). Uses `importlib.reload()` for iterative development.

## Key Concepts

- **Actor**: has `resistance` (0–1), `persuasion` (0–1), and preference vector `[va, vb, valt]`
- **Transition matrix**: 9×9 matrix (3×3 joint states flattened). Identity for agreement states; disagreement states filled by `choice_probabilities(resistance, persuasion)`
- **`choice_probabilities(ra, cb)`**: returns tuple `(1-cb, (1-ra)*cb, ra*cb)` — probabilities of staying, adopting other's view, or choosing alternative
- Plot outputs go to `.output/` directory (gitignored)
