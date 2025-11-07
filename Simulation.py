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
        "s": "Chase",
        "p": "Flee",
        "g": "GameOver",
        "l": "Wander",
        "x": "Invalid",
        "e": "Invalid",
        "b": "Invalid"
    },
    "Chase": {
        "l": "Wander",
        "p": "Flee",
        "g": "GameOver",
        "s": "Chase",
        "x": "Invalid",
        "e": "Invalid",
        "b": "Invalid"
    },
    "Flee": {
        "x": "Wander",
        "e": "Return",
        "g": "GameOver",
        "s": "Flee",
        "l": "Flee",
        "p": "Flee",
        "b": "Invalid"
    },
    "Return": {
        "b": "Wander",
        "g": "GameOver",
        "s": "Invalid",
        "l": "Invalid",
        "p": "Invalid",
        "x": "Invalid",
        "e": "Invalid"
    },
    "Invalid": {s: "Invalid" for s in symbols},
    "GameOver": {s: "GameOver" for s in symbols}
}

# Optimized positions
positions = {
    "Wander": (250, 480),
    "Chase": (450, 230),
    "Flee": (850, 180),
    "Return": (550, 680),
    "Invalid": (1100, 680),
    "GameOver": (1100, 280)
}

# State colors
colors = {
    "Wander": "#4CAF50",
    "Chase": "#FF9800",
    "Flee": "#9C27B0",
    "Return": "#FFEB3B",
    "Invalid": "#F44336",
    "GameOver": "#2196F3"
}

radius = 55

root = tk.Tk()
root.title("Pac-Man Ghost DFA Simulation")
canvas = tk.Canvas(root, width=1400, height=900, bg="#F5F5F5")
canvas.pack(padx=10, pady=10)

# Draw states
for state, (x, y) in positions.items():
    if state == "GameOver":
        outer_r = radius + 8
        canvas.create_oval(x - outer_r, y - outer_r, x + outer_r, y + outer_r,
                           outline="black", width=3)
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                           fill=colors[state], outline="black", width=3)
        canvas.create_text(x, y, text=state, font=("Helvetica", 14, "bold"), fill="white")
    else:
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                           fill=colors[state], outline="black", width=3)
        text_color = "white" if state in ["Chase", "Flee", "Invalid"] else "black"
        canvas.create_text(x, y, text=state, font=("Helvetica", 14, "bold"), fill=text_color)


def draw_curved_arrow(x1, y1, x2, y2, label, curve_strength=0, arrow=tk.LAST, label_offset=0, label_pos=None):
    if x1 == x2 and y1 == y2:
        loop_radius = radius * 0.9
        canvas.create_arc(
            x1 - loop_radius, y1 - radius - loop_radius,
            x1 + loop_radius, y1 - radius + loop_radius,
            start=30, extent=300, style="arc", width=3, outline="black"
        )
        arrow_angle = math.radians(330)
        end_x = x1 + loop_radius * math.cos(arrow_angle)
        end_y = (y1 - radius) + loop_radius * math.sin(arrow_angle)
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
        label_y = y1 - radius - loop_radius - 15
        bbox = canvas.create_text(x1, label_y, text=label, font=("Helvetica", 12, "bold"))
        text_bbox = canvas.bbox(bbox)
        canvas.delete(bbox)
        if text_bbox:
            canvas.create_rectangle(text_bbox[0]-4, text_bbox[1]-2, text_bbox[2]+4, text_bbox[3]+2,
                                   fill="white", outline="black", width=1)
        canvas.create_text(x1, label_y, text=label, font=("Helvetica", 12, "bold"), fill="#000")
        return

    dx, dy = x2 - x1, y2 - y1
    dist = math.sqrt(dx*dx + dy*dy)
    ux, uy = dx/dist, dy/dist

    padding = 10
    x1_adj = x1 + (radius + padding) * ux
    y1_adj = y1 + (radius + padding) * uy
    x2_adj = x2 - (radius + padding) * ux
    y2_adj = y2 - (radius + padding) * uy

    perp_x = -uy
    perp_y = ux

    mid_x = (x1_adj + x2_adj) / 2
    mid_y = (y1_adj + y2_adj) / 2
    cx = mid_x + curve_strength * perp_x
    cy = mid_y + curve_strength * perp_y

    canvas.create_line(x1_adj, y1_adj, cx, cy, x2_adj, y2_adj,
                       smooth=True, arrow=arrow, width=3, fill="black", arrowshape=(12, 15, 6))

    if label_pos:
        lx, ly = label_pos
    else:
        lx, ly = (cx, cy - 20)

    temp_text = canvas.create_text(lx, ly, text=label, font=("Helvetica", 12, "bold"))
    text_bbox = canvas.bbox(temp_text)
    canvas.delete(temp_text)
    if text_bbox:
        canvas.create_rectangle(text_bbox[0]-4, text_bbox[1]-2, text_bbox[2]+4, text_bbox[3]+2,
                               fill="white", outline="black", width=1)
    canvas.create_text(lx, ly, text=label, font=("Helvetica", 12, "bold"), fill="#000")


# Start arrow
start_x, start_y = positions["Wander"]
canvas.create_line(start_x - 120, start_y, start_x - radius - 10, start_y,
                   arrow=tk.LAST, width=3, fill="black", arrowshape=(12, 15, 6))
canvas.create_text(start_x - 150, start_y, text="Start", font=("Helvetica", 12, "bold"))

# Transitions
draw_curved_arrow(*positions["Wander"], *positions["Chase"], "s", curve_strength=50, label_pos=(320, 390))
draw_curved_arrow(*positions["Chase"], *positions["Wander"], "l", curve_strength=50, label_pos=(320, 320))

# ✅ Single clean arrows between Wander ↔ Flee
draw_curved_arrow(*positions["Wander"], *positions["Flee"], "x", curve_strength=70, label_pos=(490, 350))
draw_curved_arrow(*positions["Flee"], *positions["Wander"], "p", curve_strength=70, label_pos=(650, 340))

draw_curved_arrow(*positions["Chase"], *positions["Flee"], "p", curve_strength=-30, label_pos=(680, 170))
draw_curved_arrow(*positions["Flee"], *positions["Return"], "e", curve_strength=60, label_pos=(710, 390))
draw_curved_arrow(*positions["Return"], *positions["Wander"], "b", curve_strength=-80, label_pos=(320, 610))

invalid_transitions = [
    ("Wander", "[x,e,b]", -100, (400, 510)),
    ("Chase", "[x,e,b]", 80, (860, 520)),
    ("Flee", "[b]", -30, (960, 450)),
    ("Return", "[s,l,p,x,e]", 100, (800, 710))
]

for state, sym_str, curve, pos in invalid_transitions:
    draw_curved_arrow(*positions[state], *positions["Invalid"], sym_str, curve_strength=curve, label_pos=pos)

gameover_transitions = [
    ("Wander", 100, (580, 430)),
    ("Chase", 60, (590, 230)),
    ("Flee", 30, (960, 200)),
    ("Return", -80, (670, 610))
]

for state, curve, pos in gameover_transitions:
    draw_curved_arrow(*positions[state], *positions["GameOver"], "g", curve_strength=curve, label_pos=pos)

draw_curved_arrow(*positions["Wander"], *positions["Wander"], "l")
draw_curved_arrow(*positions["Chase"], *positions["Chase"], "s")
draw_curved_arrow(*positions["Flee"], *positions["Flee"], "[s,l,p]")
draw_curved_arrow(*positions["Invalid"], *positions["Invalid"], "All")
draw_curved_arrow(*positions["GameOver"], *positions["GameOver"], "All")

transition_curve_map = {
    ("Wander", "Chase"): 50,
    ("Chase", "Wander"): 50,
    ("Wander", "Flee"): 70,
    ("Flee", "Wander"): 70,
    ("Chase", "Flee"): -30,
    ("Flee", "Return"): 60,
    ("Return", "Wander"): -80,
    ("Wander", "Invalid"): -100,
    ("Chase", "Invalid"): 80,
    ("Flee", "Invalid"): -30,
    ("Return", "Invalid"): 100,
    ("Wander", "GameOver"): 100,
    ("Chase", "GameOver"): 60,
    ("Flee", "GameOver"): 30,
    ("Return", "GameOver"): -80,
    ("Invalid", "GameOver"): -100,
    # Self-loops
    ("Wander", "Wander"): 0,
    ("Chase", "Chase"): 0,
    ("Flee", "Flee"): 0,
    ("Invalid", "Invalid"): 0,
    ("GameOver", "GameOver"): 0
}

ghost_img = None
ghost = None
ghost_is_image = False

img_path = os.path.join(os.path.dirname(__file__), "ghost.png")
if os.path.exists(img_path):
    try:
        ghost_img = tk.PhotoImage(file=img_path)
        iw, ih = ghost_img.width(), ghost_img.height()
        if max(iw, ih) > 30:
            sub = max(1, int(max(iw, ih) / 30))
            ghost_img = ghost_img.subsample(sub, sub)
        ghost = canvas.create_image(0, 0, image=ghost_img)
        ghost_is_image = True
    except Exception:
        ghost = canvas.create_oval(0, 0, 0, 0, fill="red", outline="orange", width=3)
else:
    ghost = canvas.create_oval(0, 0, 0, 0, fill="red", outline="orange", width=3)

current_state = "Wander"

# Draw legend for input symbols
legend_x = 50
legend_y = 50
legend_title = "Input Symbols:"
canvas.create_text(legend_x, legend_y, text=legend_title, font=("Helvetica", 14, "bold"), anchor="w", fill="black")

symbol_descriptions = {
    's': 'Spot Pac-Man',
    'l': 'Lose Pac-Man',
    'p': 'Power Pellet',
    'x': 'Expire (power ends)',
    'e': 'Eaten by Pac-Man',
    'b': 'Back to Base',
    'g': 'Game Over'
}

y_offset = legend_y + 25
for symbol, description in symbol_descriptions.items():
    # Draw symbol in a small box
    box_size = 20
    canvas.create_rectangle(legend_x, y_offset - 10, legend_x + box_size, y_offset + 10,
                           fill="white", outline="black", width=2)
    canvas.create_text(legend_x + box_size/2, y_offset, text=symbol,
                      font=("Helvetica", 12, "bold"), fill="black")
    # Draw description
    canvas.create_text(legend_x + box_size + 10, y_offset, text=description,
                      font=("Helvetica", 11), anchor="w", fill="black")
    y_offset += 30


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
        return

    def compute_curve(p_start, p_end, curve_strength=0):
        x1, y1 = p_start
        x2, y2 = p_end
        dx, dy = x2 - x1, y2 - y1
        dist = math.sqrt(dx*dx + dy*dy) if (dx or dy) else 1.0
        ux, uy = dx/dist, dy/dist
        ax = x1 + radius * ux
        ay = y1 + radius * uy
        bx = x2 - radius * ux
        by = y2 - radius * uy
        cx = (ax + bx)/2 - curve_strength * uy
        cy = (ay + by)/2 + curve_strength * ux
        return (ax, ay), (cx, cy), (bx, by)

    cs = transition_curve_map.get((prev_state, state_name), 0)
    P0, C, P2 = compute_curve(positions[prev_state], positions[state_name], curve_strength=cs)

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
        cx, cy = positions[state_name]
        for i in range(10):
            t = (i+1)/10
            nx = P2[0] + (cx - P2[0])*t
            ny = P2[1] + (cy - P2[1])*t
            if ghost_is_image:
                canvas.coords(ghost, nx, ny)
            else:
                canvas.coords(ghost, nx - 15, ny - 15, nx + 15, ny + 15)
            root.update()
            time.sleep(0.02)
    except tk.TclError:
        return


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
