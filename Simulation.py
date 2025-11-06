import tkinter as tk
import os
import math
import time

# All states in the DFA
states = ["Wander", "Chase", "Flee", "Return", "Invalid", "GameOver"]

# All possible input symbols
symbols = ['s', 'l', 'p', 'x', 'e', 'b', 'g']

# Transitions based on the hand-drawn diagram
transitions = {
    "Wander": {
        "s": "Chase",           # Spot Pac-Man
        "p": "Flee",            # Power Pellet
        "g": "GameOver",        # Game Over
        "l": "Invalid",         # Invalid
        "x": "Invalid",         # Invalid
        "e": "Invalid",         # Invalid
        "b": "Invalid"          # Invalid
    },
    "Chase": {
        "l": "Wander",          # Lose Pac-Man
        "p": "Flee",            # Power Pellet
        "g": "GameOver",        # Game Over
        "s": "Invalid",         # Invalid
        "x": "Invalid",         # Invalid
        "e": "Invalid",         # Invalid
        "b": "Invalid"          # Invalid
    },
    "Flee": {
        "x": "Wander",          # Expire
        "e": "Return",          # Eaten by Pac-Man
        "g": "GameOver",        # Game Over
        "s": "Invalid",         # Invalid
        "l": "Invalid",         # Invalid
        "p": "Invalid",         # Invalid
        "b": "Invalid"          # Invalid
    },
    "Return": {
        "b": "Wander",          # Reach Central Base
        "g": "GameOver",        # Game Over
        "s": "Invalid",         # Invalid
        "l": "Invalid",         # Invalid
        "p": "Invalid",         # Invalid
        "x": "Invalid",         # Invalid
        "e": "Invalid"          # Invalid
    },
    "Invalid": {
        "s": "Invalid",         # All inputs stay in Invalid
        "l": "Invalid",
        "p": "Invalid",
        "x": "Invalid",
        "e": "Invalid",
        "b": "Invalid",
        "g": "Invalid"
    },
    "GameOver": {
        "s": "GameOver",        # All inputs stay in GameOver
        "l": "GameOver",
        "p": "GameOver",
        "x": "GameOver",
        "e": "GameOver",
        "b": "GameOver",
        "g": "GameOver"
    }
}

# Optimized positions for better visibility
positions = {
    "Wander": (250, 400),      # Left center
    "Chase": (550, 200),       # Top center
    "Flee": (850, 200),        # Top right
    "Return": (550, 600),      # Bottom center
    "Invalid": (1100, 600),    # Bottom right
    "GameOver": (1100, 200)    # Top far right
}

# State colors
colors = {
    "Wander": "#4CAF50",       # Green
    "Chase": "#FF9800",        # Orange
    "Flee": "#9C27B0",         # Purple
    "Return": "#FFEB3B",       # Yellow
    "Invalid": "#F44336",      # Red
    "GameOver": "#2196F3"      # Blue
}

radius = 55

root = tk.Tk()
root.title("Pac-Man Ghost DFA Simulation")
canvas = tk.Canvas(root, width=1400, height=900, bg="#F5F5F5")
canvas.pack(padx=10, pady=10)

# Draw states
for state, (x, y) in positions.items():
    # Draw double circle for accepting states (Flee and GameOver)
    if state in ["Flee", "GameOver"]:
        outer_r = radius + 8
        canvas.create_oval(x - outer_r, y - outer_r, x + outer_r, y + outer_r,
                           outline="black", width=3)
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                           fill=colors[state], outline="black", width=3)
        canvas.create_text(x, y, text=state, font=("Helvetica", 14, "bold"), fill="white")
    else:
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                           fill=colors[state], outline="black", width=3)
        # Use white text for dark backgrounds
        text_color = "white" if state in ["Chase", "Flee", "Invalid"] else "black"
        canvas.create_text(x, y, text=state, font=("Helvetica", 14, "bold"), fill=text_color)

def draw_curved_arrow(x1, y1, x2, y2, label, curve_strength=0, arrow=tk.LAST, label_offset=0):
    """Draw a curved arrow between two points with a label."""
    # Special case for self-loops
    if x1 == x2 and y1 == y2:
        # Draw a circular self-loop above the state
        loop_radius = radius * 0.9

        # Create an arc that circles back to the start point
        canvas.create_arc(
            x1 - loop_radius, y1 - radius - loop_radius,
            x1 + loop_radius, y1 - radius + loop_radius,
            start=30, extent=300,
            style="arc", width=3, outline="black"
        )

        # Add the arrow at the end
        arrow_angle = math.radians(330)
        end_x = x1 + loop_radius * math.cos(arrow_angle)
        end_y = (y1 - radius) + loop_radius * math.sin(arrow_angle)

        # Draw arrowhead
        arrow_length = 12
        canvas.create_line(
            end_x, end_y,
            end_x - arrow_length * math.cos(arrow_angle - math.pi/6),
            end_y - arrow_length * math.sin(arrow_angle - math.pi/6),
            width=3, fill="black"
        )
        canvas.create_line(
            end_x, end_y,
            end_x - arrow_length * math.cos(arrow_angle + math.pi/6),
            end_y - arrow_length * math.sin(arrow_angle + math.pi/6),
            width=3, fill="black"
        )

        # Position the label above the loop
        canvas.create_text(x1, y1 - radius - loop_radius - 15,
                          text=label, font=("Helvetica", 11, "bold"), fill="#000")
        return

    # Calculate direction vector
    dx, dy = x2 - x1, y2 - y1
    dist = math.sqrt(dx*dx + dy*dy)
    ux, uy = dx/dist, dy/dist

    # Adjust start and end points to circle perimeter
    x1 += radius * ux
    y1 += radius * uy
    x2 -= radius * ux
    y2 -= radius * uy

    # Calculate control point for curve
    cx = (x1 + x2)/2 - curve_strength * uy
    cy = (y1 + y2)/2 + curve_strength * ux

    # Draw the curved line
    canvas.create_line(x1, y1, cx, cy, x2, y2,
                       smooth=True, arrow=arrow, width=3, fill="black", arrowshape=(12, 15, 6))

    # Position label along the curve
    lx = (x1 + x2)/2 - (curve_strength/2)*uy + label_offset * uy
    ly = (y1 + y2)/2 + (curve_strength/2)*ux - label_offset * ux
    canvas.create_text(lx, ly - 15, text=label, font=("Helvetica", 11, "bold"), fill="#000")

# Draw start indicator
start_x, start_y = positions["Wander"]
canvas.create_line(start_x - 120, start_y, start_x - radius - 10, start_y,
                   arrow=tk.LAST, width=3, fill="black", arrowshape=(12, 15, 6))
canvas.create_text(start_x - 150, start_y, text="Start", font=("Helvetica", 12, "bold"), fill="black")

# Draw transitions based on the diagram
# Wander -> Chase (s: Spot Pac-Man)
draw_curved_arrow(
    positions["Wander"][0], positions["Wander"][1],
    positions["Chase"][0], positions["Chase"][1],
    "s (Spot)", curve_strength=40
)

# Chase -> Wander (l: Lose Pac-Man)
draw_curved_arrow(
    positions["Chase"][0], positions["Chase"][1],
    positions["Wander"][0], positions["Wander"][1],
    "l (Lose)", curve_strength=40
)

# Wander -> Flee (p: Power Pellet)
draw_curved_arrow(
    positions["Wander"][0], positions["Wander"][1],
    positions["Flee"][0], positions["Flee"][1],
    "p (Power)", curve_strength=-50
)

# Chase -> Flee (p: Power Pellet)
draw_curved_arrow(
    positions["Chase"][0], positions["Chase"][1],
    positions["Flee"][0], positions["Flee"][1],
    "p (Power)", curve_strength=0
)

# Flee -> Wander (x: Expire)
draw_curved_arrow(
    positions["Flee"][0], positions["Flee"][1],
    positions["Wander"][0], positions["Wander"][1],
    "x (Expire)", curve_strength=50
)

# Flee -> Return (e: Eaten)
draw_curved_arrow(
    positions["Flee"][0], positions["Flee"][1],
    positions["Return"][0], positions["Return"][1],
    "e (Eaten)", curve_strength=40
)

# Return -> Wander (b: Base)
draw_curved_arrow(
    positions["Return"][0], positions["Return"][1],
    positions["Wander"][0], positions["Wander"][1],
    "b (Base)", curve_strength=-40
)

# Draw transitions to Invalid state
invalid_curve_strengths = {
    "Wander": ("l,x,e,b", -80),
    "Chase": ("s,x,e,b", 60),
    "Flee": ("s,l,p,b", 0),
    "Return": ("s,l,p,x,e", 80)
}

for state, (symbols_str, curve) in invalid_curve_strengths.items():
    draw_curved_arrow(
        positions[state][0], positions[state][1],
        positions["Invalid"][0], positions["Invalid"][1],
        f"[{symbols_str}]", curve_strength=curve
    )

# Draw transitions to GameOver state
gameover_curve_strengths = {
    "Wander": 80,
    "Chase": 40,
    "Flee": 0,
    "Return": -40,
    "Invalid": -80
}

for state, curve in gameover_curve_strengths.items():
    draw_curved_arrow(
        positions[state][0], positions[state][1],
        positions["GameOver"][0], positions["GameOver"][1],
        "g", curve_strength=curve
    )

# Draw self-loops
draw_curved_arrow(
    positions["Invalid"][0], positions["Invalid"][1],
    positions["Invalid"][0], positions["Invalid"][1],
    "All"
)

draw_curved_arrow(
    positions["GameOver"][0], positions["GameOver"][1],
    positions["GameOver"][0], positions["GameOver"][1],
    "All"
)

# Map transitions to curve strengths for animation
transition_curve_map = {
    ("Wander", "Chase"): 40,
    ("Chase", "Wander"): 40,
    ("Wander", "Flee"): -50,
    ("Chase", "Flee"): 0,
    ("Flee", "Wander"): 50,
    ("Flee", "Return"): 40,
    ("Return", "Wander"): -40,
    # To Invalid
    ("Wander", "Invalid"): -80,
    ("Chase", "Invalid"): 60,
    ("Flee", "Invalid"): 0,
    ("Return", "Invalid"): 80,
    # To GameOver
    ("Wander", "GameOver"): 80,
    ("Chase", "GameOver"): 40,
    ("Flee", "GameOver"): 0,
    ("Return", "GameOver"): -40,
    ("Invalid", "GameOver"): -80,
    # Self-loops
    ("Invalid", "Invalid"): 0,
    ("GameOver", "GameOver"): 0
}

# Ghost marker: try to load `ghost.png` from the same folder. Fall back to an oval.
ghost_img = None
ghost = None
ghost_is_image = False

img_path = os.path.join(os.path.dirname(__file__), "ghost.png")
if os.path.exists(img_path):
    try:
        ghost_img = tk.PhotoImage(file=img_path)
        # If image is large, subsample by an integer factor so it fits roughly 30px
        try:
            iw = ghost_img.width()
            ih = ghost_img.height()
            max_dim = 30
            if max(iw, ih) > max_dim:
                sub = max(1, int(max(iw, ih) / max_dim))
                ghost_img = ghost_img.subsample(sub, sub)
        except Exception:
            # If width()/height() not available or subsample fails, ignore and use as-is
            pass

        ghost = canvas.create_image(0, 0, image=ghost_img)
        ghost_is_image = True
    except Exception:
        ghost = canvas.create_oval(0, 0, 0, 0, fill="red", outline="orange", width=3)
else:
    ghost = canvas.create_oval(0, 0, 0, 0, fill="red", outline="orange", width=3)

current_state = "Wander"

def move_ghost_to(state_name, prev_state):
    try:
        if not prev_state:
            x, y = positions[state_name]
            if ghost_is_image:
                canvas.coords(ghost, x, y)
            else:
                canvas.coords(ghost, x - 15, y - 15, x + 15, y + 15)
            return
    except tk.TclError:
        # Window was closed during animation
        return

    # Helper to compute adjusted endpoints and control point used by draw_curved_arrow
    def compute_curve(p_start, p_end, curve_strength=0):
        x1, y1 = p_start
        x2, y2 = p_end
        dx, dy = x2 - x1, y2 - y1
        dist = math.sqrt(dx*dx + dy*dy) if (dx or dy) else 1.0
        ux, uy = dx/dist, dy/dist

        # Move endpoints to the perimeter of the state circles
        ax = x1 + radius * ux
        ay = y1 + radius * uy
        bx = x2 - radius * ux
        by = y2 - radius * uy

        cx = (ax + bx)/2 - curve_strength * uy
        cy = (ay + by)/2 + curve_strength * ux

        return (ax, ay), (cx, cy), (bx, by)

    # Get curve strength for this transition
    cs = transition_curve_map.get((prev_state, state_name), 0)
    P0, C, P2 = compute_curve(positions[prev_state], positions[state_name], curve_strength=cs)

    # Animate along quadratic Bezier curve P(t) = (1-t)^2 * P0 + 2*(1-t)*t * C + t^2 * P2
    try:
        steps = 40
        for i in range(steps + 1):
            t = i/steps
            omt = 1 - t
            nx = omt*omt*P0[0] + 2*omt*t*C[0] + t*t*P2[0]
            ny = omt*omt*P0[1] + 2*omt*t*C[1] + t*t*P2[1]
            if ghost_is_image:
                canvas.coords(ghost, nx, ny)
            else:
                canvas.coords(ghost, nx - 15, ny - 15, nx + 15, ny + 15)
            root.update()
            time.sleep(0.02)

        # After reaching the state's perimeter, move the ghost to the center of the destination state
        center_x, center_y = positions[state_name]
        start_x, start_y = P2
        steps_center = 10
        for i in range(1, steps_center + 1):
            t = i / steps_center
            cx = start_x + (center_x - start_x) * t
            cy = start_y + (center_y - start_y) * t
            if ghost_is_image:
                canvas.coords(ghost, cx, cy)
            else:
                canvas.coords(ghost, cx - 15, cy - 15, cx + 15, cy + 15)
            root.update()
            time.sleep(0.02)
    except tk.TclError:
        # Window was closed during animation
        return

# Create log area
log = tk.Text(root, height=8, width=120, bg="#1E1E1E", fg="#00FF00", font=("Courier", 11))
log.pack(pady=10)
log.insert(tk.END, "=== Pac-Man Ghost DFA Simulation ===\n")
log.insert(tk.END, "Press keys to trigger transitions:\n")
log.insert(tk.END, "  s = Spot Pac-Man\n")
log.insert(tk.END, "  l = Lose Pac-Man\n")
log.insert(tk.END, "  p = Power Pellet\n")
log.insert(tk.END, "  x = Expire\n")
log.insert(tk.END, "  e = Eaten by Pac-Man\n")
log.insert(tk.END, "  b = Reach Base\n")
log.insert(tk.END, "  g = Game Over\n")
log.insert(tk.END, "=" * 50 + "\n")
log.config(state=tk.DISABLED)

def on_key(event):
    global current_state
    symbol = event.char.lower()

    # Check if symbol is valid
    if symbol not in symbols:
        return

    next_state = transitions.get(current_state, {}).get(symbol)
    if next_state:
        log.config(state=tk.NORMAL)
        log.insert(tk.END, f"[{symbol}] {current_state} → {next_state}\n")
        log.see(tk.END)
        log.config(state=tk.DISABLED)
        move_ghost_to(next_state, current_state)
        current_state = next_state
    else:
        log.config(state=tk.NORMAL)
        log.insert(tk.END, f"❌ No transition for '{symbol}' from {current_state}\n")
        log.see(tk.END)
        log.config(state=tk.DISABLED)

root.bind("<Key>", on_key)

move_ghost_to("Wander", None)

root.mainloop()
