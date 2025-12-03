import tkinter as tk
from tkinter import ttk

user = False
message_labels: list[tk.Label] = []

def add_message(msg: str, isUser: bool):
    color = 'blue' if isUser else 'grey'
    anchor = 'e' if isUser else 'w'  # e=east (right), w=west (left)
    label = tk.Label(messages_frame, text=msg, background=color, padx=6, pady=5)
    message_labels.append(label)
    label.pack(anchor=anchor, padx=5, pady=3)
    # set wraplength to half of messages_frame's current width so the label uses ~50% of available width
    label.update_idletasks()
    label.config(wraplength=max(40, messages_frame.winfo_width() * (3/5)))

    # Update the scroll region to include all content
    messages_frame.update_idletasks()
    canv.config(scrollregion=canv.bbox("all"))

    # Auto-scroll to bottom
    canv.yview_moveto(1.0)
    

def handleSendMessage():
    global user
    add_message(entry.get(), user)
    user = not user
    entry.delete(0, tk.END)


root = tk.Tk()
# set window size and center it on screen
width, height = 400, 300
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
x = (screen_w - width) // 2
y = (screen_h - height) // 2
root.geometry(f"{width}x{height}+{x}+{y}")

# Set minimum window size to prevent input from disappearing
root.minsize(400, 200)

# Create input row FIRST (pack at bottom)
input_row = ttk.Frame(root)
input_row.pack(side='bottom', fill='x', padx=5, pady=5)
input_row.pack_propagate(False)  # Prevent frame from shrinking
input_row.config(height=30)  # Fixed height

canv = tk.Canvas(root, bg='green', highlightthickness=0)
ybar = tk.Scrollbar(root,command=canv.yview)
canv.config(yscrollcommand=ybar.set)  

ybar.pack(side='right', fill='y')
canv.pack(side='top', expand=True, fill='both')
          

messages_frame = tk.Frame(canv, background='yellow')
canv_frame = canv.create_window((0, 0), window=messages_frame, anchor='nw')

# Make the frame expand to canvas width
def on_canvas_configure(event):
    canv.itemconfig(canv_frame, width=event.width)

    #update messages to correct widths
    new_label_width = messages_frame.winfo_width() * (3/5)
    for ml in message_labels:
        ml.config(wraplength=max(40, new_label_width))
    
    # Update scroll region after reconfiguring
    canv.update_idletasks()
    canv.config(scrollregion=canv.bbox("all"))

canv.bind('<Configure>', on_canvas_configure)

entry = ttk.Entry(input_row)
entry.pack(side='left', fill='x', expand=True, padx=(0, 5))

send_button = ttk.Button(input_row, text="Send", command=lambda: handleSendMessage())
send_button.pack(side='right')


# Bind Enter key to send message
entry.bind('<Return>', lambda e: handleSendMessage())



# # Row 3: Button centered
# # ttk.Button(root, text="Quit", command=root.destroy).pack(pady=10)

for i in range(20):
    add_message('hello', i%2==0)

root.mainloop()






