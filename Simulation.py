import tkinter as tk
import os
import math
import time

states = ["Wander", "Chase", "Flee", "Return"]

transitions = {
    "Wander": {"s": "Chase", "p": "Flee"},
    "Chase": {"l": "Wander", "p": "Flee"},
    "Flee": {"x": "Wander", "e": "Return"},
    "Return": {"b": "Wander"}
}

positions = {
    "Wander": (200, 300),
    "Chase": (500, 100),
    "Flee": (800, 300),
    "Return": (500, 500)
}

colors = {
    "Wander": "#A8E6CF",
    "Chase": "#FF8C94",
    "Flee": "#9ED2FF",
    "Return": "#D6A2E8"
}

radius = 60

root = tk.Tk()
root.title("Pac-Man Ghost DFA - Distinct Bidirectional Arrows")
canvas = tk.Canvas(root, width=1000, height=650, bg="white")
canvas.pack(padx=10, pady=10)

# Draw states
for state, (x, y) in positions.items():
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                       fill=colors[state], outline="black", width=3)
    canvas.create_text(x, y, text=state, font=("Helvetica", 13, "bold"))

def draw_curved_arrow(x1, y1, x2, y2, label, curve_strength=0, arrow=tk.LAST):
    dx, dy = x2 - x1, y2 - y1
    dist = math.sqrt(dx*dx + dy*dy)
    ux, uy = dx/dist, dy/dist
    x1 += radius * ux
    y1 += radius * uy
    x2 -= radius * ux
    y2 -= radius * uy

    cx = (x1 + x2)/2 - curve_strength * uy
    cy = (y1 + y2)/2 + curve_strength * ux

    canvas.create_line(x1, y1, cx, cy, x2, y2,
                       smooth=True, arrow=arrow, width=2, fill="black")

    lx = (x1 + x2)/2 - (curve_strength/2)*uy
    ly = (y1 + y2)/2 + (curve_strength/2)*ux
    canvas.create_text(lx, ly - 20, text=label, font=("Helvetica", 10), fill="#333")

def draw_bidirectional_arrow(x1, y1, x2, y2, label1, label2, offset=15):
    dx, dy = x2 - x1, y2 - y1
    dist = math.sqrt(dx*dx + dy*dy)
    ux, uy = dx/dist, dy/dist
    px, py = -uy, ux

    # Offset for first arrow
    sx1, sy1 = x1 + px * offset, y1 + py * offset
    ex1, ey1 = x2 + px * offset, y2 + py * offset

    # Offset for second arrow
    sx2, sy2 = x1 - px * offset, y1 - py * offset
    ex2, ey2 = x2 - px * offset, y2 - py * offset

    # First arrow: points toward (x2,y2) -- arrow at end
    draw_curved_arrow(sx1, sy1, ex1, ey1, label1, curve_strength=60, arrow=tk.LAST)
    # Second arrow: arrow at start so it points toward (x1,y1)
    draw_curved_arrow(sx2, sy2, ex2, ey2, label2, curve_strength=-60, arrow=tk.FIRST)

# Draw bidirectional arrows with distinct lines
draw_bidirectional_arrow(
    positions["Wander"][0], positions["Wander"][1],
    positions["Chase"][0], positions["Chase"][1],
    "Spot Pac-Man", "Lose Pac-Man"
)

draw_bidirectional_arrow(
    positions["Wander"][0], positions["Wander"][1],
    positions["Flee"][0], positions["Flee"][1],
    "Pac-Man Eats Power Pellet", "Power Pellet Expires"
)

# Draw other one-way transitions
draw_curved_arrow(
    positions["Chase"][0], positions["Chase"][1],
    positions["Flee"][0], positions["Flee"][1],
    "Pac-Man Eats Power Pellet"
)
draw_curved_arrow(
    positions["Flee"][0], positions["Flee"][1],
    positions["Return"][0], positions["Return"][1],
    "Eaten by Pac-Man"
)
draw_curved_arrow(
    positions["Return"][0], positions["Return"][1],
    positions["Wander"][0], positions["Wander"][1],
    "Reach Central Base"
)

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
    if not prev_state:
        x, y = positions[state_name]
        if ghost_is_image:
            canvas.coords(ghost, x, y)
        else:
            canvas.coords(ghost, x - 15, y - 15, x + 15, y + 15)
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

    # Determine if this transition is one of the bidirectional pairs that were drawn
    bidir_pairs = {('Wander', 'Chase'), ('Wander', 'Flee')}

    # If it's a bidirectional pair, we used two offset curves; reconstruct which one to follow
    if (prev_state, state_name) in bidir_pairs or (state_name, prev_state) in bidir_pairs:
        # x1,x2 correspond to the order used when drawing the bidirectional arrow
        a_name, b_name = (prev_state, state_name) if (prev_state, state_name) in bidir_pairs else (state_name, prev_state)
        x1, y1 = positions[a_name]
        x2, y2 = positions[b_name]
        dx, dy = x2 - x1, y2 - y1
        dist = math.sqrt(dx*dx + dy*dy)
        ux, uy = dx/dist, dy/dist
        px, py = -uy, ux
        offset = 15

        # First curve (offset +) with curve_strength=60
        sx1, sy1 = x1 + px * offset, y1 + py * offset
        ex1, ey1 = x2 + px * offset, y2 + py * offset

        # Second curve (offset -) with curve_strength=-60
        sx2, sy2 = x1 - px * offset, y1 - py * offset
        ex2, ey2 = x2 - px * offset, y2 - py * offset

        # Map movement direction to the correct curve and orientation
        if prev_state == a_name and state_name == b_name:
            # moving a -> b : follow first curve from sx1->ex1 with curve_strength=60
            P0, C, P2 = compute_curve((sx1, sy1), (ex1, ey1), curve_strength=60)
        else:
            # moving b -> a : follow second curve reversed (from ex2 -> sx2) using curve_strength=-60
            # compute control for the original orientation sx2->ex2, then reverse endpoints
            _, C, _ = compute_curve((sx2, sy2), (ex2, ey2), curve_strength=-60)
            P0 = (ex2, ey2)
            P2 = (sx2, sy2)
    else:
        # Regular one-way transition: compute curve between the state centers
        P0, C, P2 = compute_curve(positions[prev_state], positions[state_name], curve_strength=0)

    # Animate along quadratic Bezier curve P(t) = (1-t)^2 * P0 + 2*(1-t)*t * C + t^2 * P2
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

log = tk.Text(root, height=7, width=100, bg="#111", fg="white", font=("Courier", 10))
log.pack(pady=5)

canvas.create_text(500, 620,
                   text="Keys: s=Spot, l=Lose, p=Power Pellet, x=Expire, e=Eaten, b=Base",
                   font=("Helvetica", 11, "italic"), fill="#333")

def on_key(event):
    global current_state
    symbol = event.char.lower()
    next_state = transitions.get(current_state, {}).get(symbol)
    if next_state:
        log.insert(tk.END, f"{current_state} --{symbol}--> {next_state}\n")
        log.see(tk.END)
        move_ghost_to(next_state, current_state)
        current_state = next_state
    else:
        log.insert(tk.END, f"❌ Invalid transition '{symbol}' from {current_state}\n")
        log.see(tk.END)

root.bind("<Key>", on_key)

move_ghost_to("Wander", None)

root.mainloop()
