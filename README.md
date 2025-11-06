# Pac-Man Ghost DFA Simulation

An interactive visualization of Pac-Man ghost behavior using a Deterministic Finite Automaton (DFA).

## Overview

This simulation models the behavior of ghosts in Pac-Man as a state machine with 6 states and 7 input symbols. The ghost transitions between different behavioral states based on game events.

## States

1. **Wander** (Green) - Initial state: Ghost roams randomly
2. **Chase** (Orange) - Ghost actively pursues Pac-Man
3. **Flee** (Purple) - Ghost runs away (Pac-Man ate power pellet) - **Accepting State**
4. **Return** (Yellow) - Ghost returns to base after being eaten
5. **Invalid** (Red) - Error state for undefined transitions
6. **GameOver** (Blue) - Final game over state - **Accepting State**

## Input Symbols

- `s` - Spot Pac-Man
- `l` - Lose Pac-Man
- `p` - Power Pellet eaten
- `x` - Power pellet expires
- `e` - Ghost eaten by Pac-Man
- `b` - Reach central base
- `g` - Game Over

## Transitions

### Valid Transitions
- **Wander → Chase**: Press `s` (Spot Pac-Man)
- **Chase → Wander**: Press `l` (Lose Pac-Man)
- **Wander → Flee**: Press `p` (Power Pellet)
- **Chase → Flee**: Press `p` (Power Pellet)
- **Flee → Wander**: Press `x` (Expire)
- **Flee → Return**: Press `e` (Eaten)
- **Return → Wander**: Press `b` (Base)
- **Any State → GameOver**: Press `g` (Game Over)

### Invalid Transitions
Any undefined transition leads to the **Invalid** state, which loops back to itself.

## How to Run

```bash
python Simulation.py
```

## Controls

Press the corresponding keys to trigger state transitions:
- `s` = Spot Pac-Man
- `l` = Lose Pac-Man
- `p` = Power Pellet
- `x` = Expire
- `e` = Eaten by Pac-Man
- `b` = Reach Base
- `g` = Game Over

## Features

- **Animated Ghost**: Watch the ghost marker move along curved arrows between states
- **Visual Feedback**: Color-coded states with clear labels
- **Transition Log**: Real-time log showing all state transitions
- **Double Circles**: Accepting states (Flee and GameOver) are marked with double circles
- **Self-Loops**: Invalid and GameOver states loop back to themselves

## Requirements

- Python 3.x
- tkinter (usually included with Python)

## DFA Properties

- **Alphabet (Σ)**: {s, l, p, x, e, b, g}
- **States (Q)**: {Wander, Chase, Flee, Return, Invalid, GameOver}
- **Initial State (q₀)**: Wander
- **Accepting States (F)**: {Flee, GameOver}
- **Transition Function (δ)**: Defined in the transitions dictionary