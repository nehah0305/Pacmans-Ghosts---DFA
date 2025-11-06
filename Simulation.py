import tkinter as tk
import math

# DFA definition
states = ["Wander", "Chase", "Flee", "Return"]
transitions = {
    "Wander": {"s": "Chase"},
    "Chase": {"l": "Wander", "p": "Flee"},
    "Flee": {"x": "Chase", "e": "Return"},
    "Return": {"b": "Wander"}
}

# Layout positions (x, y) for each state node
positions = {
    "Wander": (150, 200),
    "Chase": (400, 100),
    "Flee": (650, 200),
    "Return": (400, 350)
}

# Tkinter setup
root = tk.Tk()
root.title("Pac-Man Ghost DFA Visualizer")

canvas = tk.Canvas(root, width=800, height=500, bg="black")
canvas.pack()

# Draw states as circles
radius = 40
state_circles = {}
for name, (x, y) in positions.items():
    circle = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="gray", outline="white", width=3)
    canvas.create_text(x, y, text=name, fill="white", font=("Helvetica", 14, "bold"))
    state_circles[name] = circle

# Draw transitions as arrows (lines)
def draw_arrow(x1, y1, x2, y2, label):
    dx, dy = x2 - x1, y2 - y1
    dist = math.sqrt(dx ** 2 + dy ** 2)
    ux, uy = dx / dist, dy / dist
    x1 += radius * ux
    y1 += radius * uy
    x2 -= radius * ux
    y2 -= radius * uy
    canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill="yellow", width=2)
    lx, ly = (x1 + x2) / 2, (y1 + y2) / 2
    canvas.create_text(lx, ly - 15, text=label, fill="cyan", font=("Helvetica", 12, "bold"))

# Add arrows for transitions
for from_state, mapping in transitions.items():
    x1, y1 = positions[from_state]
    for symbol, to_state in mapping.items():
        x2, y2 = positions[to_state]
        draw_arrow(x1, y1, x2, y2, symbol)

# Ghost marker (moving token)
ghost = canvas.create_oval(0, 0, 0, 0, fill="red", outline="orange", width=3)

current_state = "Wander"

def move_ghost_to(state_name):
    x, y = positions[state_name]
    canvas.coords(ghost, x - 15, y - 15, x + 15, y + 15)

# Initial ghost position
move_ghost_to(current_state)

# Text area for logs
log = tk.Text(root, height=6, width=70, bg="#111", fg="white", font=("Courier", 10))
log.pack(pady=10)

canvas.create_text(400, 470, text="Press keys: s, l, p, x, e, b", fill="cyan", font=("Helvetica", 14, "bold"))

def on_key(event):
    global current_state
    symbol = event.char
    next_state = transitions.get(current_state, {}).get(symbol)
    if next_state:
        log.insert(tk.END, f"{current_state} --{symbol}--> {next_state}\n")
        log.see(tk.END)
        current_state = next_state
        move_ghost_to(current_state)
    else:
        log.insert(tk.END, f"❌ Invalid transition '{symbol}' from {current_state}\n")
        log.see(tk.END)

root.bind("<Key>", on_key)

root.mainloop()
