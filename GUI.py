import tkinter as tk
from tkinter import ttk

user = False

def add_message(msg: str, isUser: bool):
    color = 'blue' if isUser else 'grey'
    anchor = 'e' if isUser else 'w'  # e=east (right), w=west (left)
    label = tk.Label(messages_frame, text=msg, background=color)
    label.pack(anchor=anchor, padx=5, pady=2)
    # set wraplength to half of messages_frame's current width so the label uses ~50% of available width
    label.update_idletasks()
    label.config(wraplength=max(40, messages_frame.winfo_width() // 2))
    global user
    user = not user

root = tk.Tk()
# set window size and center it on screen
width, height = 400, 300
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
x = (screen_w - width) // 2
y = (screen_h - height) // 2
root.geometry(f"{width}x{height}+{x}+{y}")

messages_frame = tk.Frame(root, background='white', padx=5)
messages_frame.pack(fill="both", expand=True)

scrollbar = tk.Scrollbar(messages_frame)
scrollbar.pack(side="right", fill="y")



# Row 2: Another label and entry
input_row = ttk.Frame(root)
input_row.pack(fill='x', padx=5, pady=5)

entry = ttk.Entry(input_row)
send_button = ttk.Button(input_row, text="Send", command=lambda: add_message(entry.get(), user))
send_button.pack(side='right')
entry.pack(side='left', fill='x', expand=True, padx=(5, 0))



# Row 3: Button centered
ttk.Button(root, text="Quit", command=root.destroy).pack(pady=10)

root.mainloop()






