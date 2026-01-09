# Cybersecurity Risk Assessment in Banking Systems

This project provides a command-line tool for conducting cybersecurity risk assessments of complex systems using Bayesian Attack Graphs (BAGs) and A* search for optimal countermeasure selection.

The original analysis was performed in a Jupyter Notebook and has since been refactored into a configurable Python script for improved modularity, testability, and ease of use.

## Project Overview

The tool models potential attack paths in a system, calculates the risk of critical asset compromise, and determines the most cost-effective set of countermeasures for a given budget.

-   **Bayesian Attack Graphs (BAGs):** The system is modeled as a BAG, where nodes represent system states or vulnerabilities, and edges represent the dependencies between them.
-   **Risk Calculation:** An iterative algorithm calculates the steady-state probability of reaching critical nodes, representing the overall risk.
-   **A* Search Algorithm:** An A* search algorithm is used to find the optimal set of countermeasures that minimizes risk for a specified budget.

---

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/adityasengar/Cybersecurity-risk-assessment.git
    cd Cybersecurity-risk-assessment
    ```

2.  It is recommended to use a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

---

## Usage

The main entry point for the tool is `risk_analyzer.py`. It can be run in two modes: `risk` and `budget`.

### `risk` mode

This mode runs a single risk calculation with no countermeasures applied and outputs the final risk of accessing the primary target (the database server).

```bash
python risk_analyzer.py --mode risk
```
This will also generate a plot of the probability evolution in `plots/probability_evolution.png`.

### `budget` mode

This mode runs the A* search algorithm to find the optimal countermeasure plan for a range of budgets.

```bash
python risk_analyzer.py --mode budget --bstart 300 --bend 1500 --bstep 200
```

**Arguments:**

-   `--mode`: The analysis mode to run (`risk` or `budget`). Default is `risk`.
-   `--config`: Path to the attack graph JSON file. Default is `config/attack_graph.json`.
-   `--bstart`: The starting budget for the analysis. Default is `300`.
-   `--bend`: The ending budget for the analysis. Default is `1500`.
-   `--bstep`: The step increment for the budget analysis. Default is `200`.
-   `--plot_dir`: The directory where output plots will be saved. Default is `plots`.

This mode will generate a plot of the risk vs. budget in `plots/risk_vs_budget.png`.

---
*The original Jupyter notebook and its instructions can be found in the project's commit history prior to May 2023.*
# Updated on 2026-01-09
