import tkinter as tk
from tkinter import ttk

message_labels: list[tk.Label] = []

def add_message(msg: str, username: str = "Anonymous", isReceived: bool = True):
    color = '#808080' if isReceived else '#218AFF'
    anchor = 'w' if isReceived else 'e'  # w=west (left), e=east (right)


    # create message container 3/5 of the window
    message_container = tk.Frame(messages_frame, padx=3)

    # create user name label set to the left for received messages
    if isReceived:
        username_label = tk.Label(message_container, text=username, fg='grey', height=1, font=('Helvetica', 7), padx=0)
        username_label.pack(side='top', anchor='w') #insert at top of container far left

    # create message box label left grey for others, right blue for user
    message_label = tk.Label(message_container, text=msg, background=color, pady=5, font=("Helvetica", 10))
    
    message_label.pack(anchor='w') #insert message into container
    message_container.pack(anchor=anchor, pady=3) #insert container onto messages frame

    message_labels.append(message_label)
    
    # update current dimensions and resize message box
    message_container.update_idletasks()
    message_label.config(wraplength=max(40, messages_frame.winfo_width() * (3/5)))

    # Update the scroll region to include all content
    messages_frame.update_idletasks()
    canv.config(scrollregion=canv.bbox("all"))

    # Auto-scroll to bottom
    canv.yview_moveto(1.0)
    

def handleSendMessage():
    add_message(entry.get(), isReceived=False)
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

canv = tk.Canvas(root, highlightthickness=0)
ybar = tk.Scrollbar(root,command=canv.yview)
canv.config(yscrollcommand=ybar.set)  

ybar.pack(side='right', fill='y')
canv.pack(side='top', expand=True, fill='both')
          

messages_frame = tk.Frame(canv, padx=10, pady=3)
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

root.mainloop()






