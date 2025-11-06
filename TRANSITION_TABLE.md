# DFA Transition Table

## Complete State Transition Table

| Current State | Input | Next State | Description |
|--------------|-------|------------|-------------|
| **Wander** | s | Chase | Ghost spots Pac-Man |
| **Wander** | l | Invalid | Cannot lose what you don't have |
| **Wander** | p | Flee | Pac-Man eats power pellet |
| **Wander** | x | Invalid | No power pellet to expire |
| **Wander** | e | Invalid | Cannot be eaten while wandering |
| **Wander** | b | Invalid | Not returning to base |
| **Wander** | g | GameOver | Game ends |
| **Chase** | s | Invalid | Already chasing |
| **Chase** | l | Wander | Lost sight of Pac-Man |
| **Chase** | p | Flee | Pac-Man eats power pellet |
| **Chase** | x | Invalid | No power pellet to expire |
| **Chase** | e | Invalid | Cannot be eaten while chasing |
| **Chase** | b | Invalid | Not returning to base |
| **Chase** | g | GameOver | Game ends |
| **Flee** | s | Invalid | Cannot spot while fleeing |
| **Flee** | l | Invalid | Not chasing to lose |
| **Flee** | p | Invalid | Already fleeing |
| **Flee** | x | Wander | Power pellet expires |
| **Flee** | e | Return | Eaten by Pac-Man |
| **Flee** | b | Invalid | Not at base yet |
| **Flee** | g | GameOver | Game ends |
| **Return** | s | Invalid | Cannot spot while returning |
| **Return** | l | Invalid | Not chasing to lose |
| **Return** | p | Invalid | Cannot flee while returning |
| **Return** | x | Invalid | No power pellet to expire |
| **Return** | e | Invalid | Already eaten |
| **Return** | b | Wander | Reached central base |
| **Return** | g | GameOver | Game ends |
| **Invalid** | s | Invalid | Error state - all inputs loop |
| **Invalid** | l | Invalid | Error state - all inputs loop |
| **Invalid** | p | Invalid | Error state - all inputs loop |
| **Invalid** | x | Invalid | Error state - all inputs loop |
| **Invalid** | e | Invalid | Error state - all inputs loop |
| **Invalid** | b | Invalid | Error state - all inputs loop |
| **Invalid** | g | Invalid | Error state - all inputs loop |
| **GameOver** | s | GameOver | Final state - all inputs loop |
| **GameOver** | l | GameOver | Final state - all inputs loop |
| **GameOver** | p | GameOver | Final state - all inputs loop |
| **GameOver** | x | GameOver | Final state - all inputs loop |
| **GameOver** | e | GameOver | Final state - all inputs loop |
| **GameOver** | b | GameOver | Final state - all inputs loop |
| **GameOver** | g | GameOver | Final state - all inputs loop |

## State Descriptions

### Wander (Initial State)
- **Color**: Green
- **Behavior**: Ghost roams randomly around the maze
- **Valid Transitions**: Can spot Pac-Man (→Chase), or Pac-Man eats power pellet (→Flee)

### Chase
- **Color**: Orange  
- **Behavior**: Ghost actively pursues Pac-Man
- **Valid Transitions**: Can lose Pac-Man (→Wander), or Pac-Man eats power pellet (→Flee)

### Flee (Accepting State)
- **Color**: Purple
- **Behavior**: Ghost runs away from Pac-Man (vulnerable state)
- **Valid Transitions**: Power pellet expires (→Wander), or eaten by Pac-Man (→Return)
- **Note**: Marked with double circle as accepting state

### Return
- **Color**: Yellow
- **Behavior**: Ghost returns to central base after being eaten
- **Valid Transitions**: Reaches base (→Wander)

### Invalid (Error State)
- **Color**: Red
- **Behavior**: Error state for undefined transitions
- **Valid Transitions**: All inputs loop back to Invalid
- **Note**: Once in Invalid state, cannot escape (except game over in some implementations)

### GameOver (Accepting State)
- **Color**: Blue
- **Behavior**: Final game over state
- **Valid Transitions**: All inputs loop back to GameOver
- **Note**: Marked with double circle as accepting state

## Input Symbol Meanings

- **s** = Spot Pac-Man (ghost sees Pac-Man)
- **l** = Lose Pac-Man (ghost loses sight of Pac-Man)
- **p** = Power Pellet (Pac-Man eats a power pellet)
- **x** = Expire (power pellet effect expires)
- **e** = Eaten (ghost is eaten by Pac-Man)
- **b** = Base (ghost reaches central base)
- **g** = Game Over (game ends)

## DFA Formal Definition

**M = (Q, Σ, δ, q₀, F)**

Where:
- **Q** = {Wander, Chase, Flee, Return, Invalid, GameOver}
- **Σ** = {s, l, p, x, e, b, g}
- **δ** = Transition function (see table above)
- **q₀** = Wander (initial state)
- **F** = {Flee, GameOver} (accepting states)

