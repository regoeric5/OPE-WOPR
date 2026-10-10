# OPE-WOPR: Opportunity, Pace, and Efficiency Metric

## 1. WOPR

$$\text{WOPR} = 1.5 \cdot (\text{Target Share}) + 0.7 \cdot (\text{Air Yard Share})$$

**Weighted Opportunity Rating (WOPR)** is an analytics metric that combines target share and air yard share to estimate a player's personal volume within a team's passing environment. 

## 2. OPE-WOPR

$$\text{\textbf{OPE-WOPR}} = 0.65(O) + 0.25(E) + 0.10(P)$$

OPE-WOPR expands traditional WOPR to provide deeper context of the workload and better align with the needs of PPR fantasy managers.

1. **Opportunity Score ($O$) — 65% Weight**
Traditional WOPR with heavier target weighting to reflect PPR scoring dynamics:

$$O = 2.0 \cdot (\text{Target Share}) + 0.5 \cdot (\text{Air Yard Share})$$


2. **Efficiency Score ($E$) — 25% Weight**
Measures target quality and distance covered per target attempt:

$$E = (\text{Catch Percentage}) \cdot (0.10 \cdot \text{Yards per Target})$$


3. **Pace Score ($P$) — 10% Weight**
Scales player volume against the team passing environment to account for overall attempt volume:

$$P = \frac{\text{Team Pass Attempts per Game}}{\text{League Avg Pass Attempts per Game}}$$

## 3. Main Script Workflow (`main.py`)

1. Uses the [nflreadpy](https://github.com/nflverse/nflreadpy) library to collect player and team statistics, filtering for positions (WR & TE) and a minimum number of targets ($\ge 20$ targets).
2. Calculates each sub-score: Opportunity ($O$), Efficiency ($E$), and Pace ($P$).
3. Combines sub-scores using their respective weights ($0.65$, $0.25$, $0.10$) into a single OPE-WOPR rating.
4. Sorts players by their OPE-WOPR score in descending order.
5. Exports a structured CSV file containing OPE-WOPR scores, sub-scores, and other metrics directly to the working directory.

## 4. Getting Started

### Prerequisites

* Python 3.11+

### Installation and Setup

Execute the following commands in your terminal to set up the environment and run the pipeline:

```bash
git clone https://github.com/regoeric5/OPE-WOPR.git
cd OPE-WOPR

# Create the virtual environment
python3.11 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the engine
python main.py

```
