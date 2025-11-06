# Quick Reference Guide

## Running the Simulation

```bash
python Simulation.py
```

## Keyboard Controls

| Key | Symbol | Action | Description |
|-----|--------|--------|-------------|
| `s` | Spot | Wander → Chase | Ghost spots Pac-Man |
| `l` | Lose | Chase → Wander | Ghost loses sight of Pac-Man |
| `p` | Power | Wander/Chase → Flee | Pac-Man eats power pellet |
| `x` | Expire | Flee → Wander | Power pellet effect expires |
| `e` | Eaten | Flee → Return | Ghost eaten by Pac-Man |
| `b` | Base | Return → Wander | Ghost reaches central base |
| `g` | GameOver | Any → GameOver | Game ends |

## State Colors

- 🟢 **Green** = Wander (Initial State)
- 🟠 **Orange** = Chase
- 🟣 **Purple** = Flee (Accepting State - Double Circle)
- 🟡 **Yellow** = Return
- 🔴 **Red** = Invalid (Error State)
- 🔵 **Blue** = GameOver (Accepting State - Double Circle)

## Common Sequences

### Normal Ghost Behavior
1. Start in **Wander** (green)
2. Press `s` → **Chase** (orange) - Ghost spots Pac-Man
3. Press `l` → **Wander** (green) - Ghost loses Pac-Man

### Power Pellet Sequence
1. From **Wander** or **Chase**
2. Press `p` → **Flee** (purple) - Pac-Man eats power pellet
3. Press `x` → **Wander** (green) - Power pellet expires

### Ghost Eaten Sequence
1. From **Flee** (purple)
2. Press `e` → **Return** (yellow) - Ghost eaten by Pac-Man
3. Press `b` → **Wander** (green) - Ghost reaches base

### Game Over
- Press `g` from any state → **GameOver** (blue)
- All inputs keep you in GameOver

### Invalid Transitions
- Any invalid key press → **Invalid** (red)
- Once in Invalid, all inputs keep you there

## Example Gameplay

```
Start → Wander
  ↓ (press 's')
Chase
  ↓ (press 'p')
Flee
  ↓ (press 'e')
Return
  ↓ (press 'b')
Wander
  ↓ (press 'g')
GameOver
```

## Tips

1. **Watch the Animation**: The ghost marker moves along the arrows
2. **Check the Log**: Bottom panel shows all transitions
3. **Double Circles**: Flee and GameOver are accepting states
4. **Invalid State**: Avoid invalid transitions to prevent getting stuck
5. **Experiment**: Try different key sequences to explore the DFA

## Visual Elements

- **Start Arrow**: Points to Wander (initial state)
- **Curved Arrows**: Show valid transitions with labels
- **Self-Loops**: Invalid and GameOver loop back to themselves
- **Ghost Marker**: Red circle or ghost.png image
- **State Labels**: Bold text in center of each circle
- **Transition Labels**: Show input symbol and description

## Troubleshooting

**Q: Nothing happens when I press keys**
- Make sure the simulation window has focus (click on it)
- Only use lowercase letters: s, l, p, x, e, b, g

**Q: Ghost is stuck in Invalid state**
- This is expected behavior for invalid transitions
- Close and restart the simulation to reset

**Q: Animation is too fast/slow**
- Edit `time.sleep(0.02)` in Simulation.py
- Increase value to slow down, decrease to speed up

**Q: Can't see the ghost**
- Make sure ghost.png is in the same folder
- Or the simulation will use a red circle as fallback

