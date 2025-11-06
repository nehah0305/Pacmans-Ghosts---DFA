import tkinter as tk
import time
import re

# Regular expression representing ghost behavior
pattern = re.compile(r'^(s(l|p|x|e|b)*)*$')

# Define DFA states and transitions
states = {
    "Wander": {"s": "Chase"},
    "Chase": {"l": "Wander", "p": "Flee"},
    "Flee": {"x": "Chase", "e": "Return"},
    "Return": {"b": "Wander"}
}

current_state = "Wander"

def transition(event):
    global current_state
    symbol = event.char
    next_state = states.get(current_state, {}).get(symbol)
    if next_state:
        log.insert(tk.END, f"{current_state} --{symbol}--> {next_state}\n")
        current_state = next_state
        canvas.itemconfig(state_text, text=current_state)
    else:
        log.insert(tk.END, f"❌ Invalid transition for '{symbol}' from {current_state}\n")

# GUI setup
root = tk.Tk()
root.title("Pac-Man Ghost DFA Simulation")

canvas = tk.Canvas(root, width=400, height=200, bg="black")
canvas.pack()
state_text = canvas.create_text(200, 100, text=current_state, fill="red", font=("Helvetica", 30, "bold"))

log = tk.Text(root, height=10, width=50)
log.pack()

tk.Label(root, text="Press keys: s, l, p, x, e, b").pack()

root.bind("<Key>", transition)
root.mainloop()
