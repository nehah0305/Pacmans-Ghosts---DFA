import tkinter as tk
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

# Ghost marker
ghost = canvas.create_oval(0, 0, 0, 0, fill="red", outline="orange", width=3)
current_state = "Wander"

def move_ghost_to(state_name, prev_state):
    if not prev_state:
        x, y = positions[state_name]
        canvas.coords(ghost, x - 15, y - 15, x + 15, y + 15)
        return

    x1, y1 = positions[prev_state]
    x2, y2 = positions[state_name]
    steps = 20
    for i in range(steps + 1):
        nx = x1 + (x2 - x1) * i / steps
        ny = y1 + (y2 - y1) * i / steps
        canvas.coords(ghost, nx - 15, ny - 15, nx + 15, ny + 15)
        root.update()
        time.sleep(0.03)

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
