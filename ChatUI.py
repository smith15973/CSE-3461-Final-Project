import tkinter as tk
from tkinter import ttk

class ChatUI:
    def __init__(self, width:int = 400, height:int = 400):
        """
        Initialize the chat UI.
        
        Args:
            width: Window width in pixels
            height: Window height in pixels
        """
        self.message_labels: list[tk.Label] = []
        self._create_window(width, height)
        self._create_ui()

    def _create_window(self, width:int, height:int):
        """Create the main window"""
        self.root = tk.Tk()
        self.root.title("Chat")
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.minsize(400, 400)

    def _create_ui(self):
        """Create all UI components."""
        # Create input row at bottom
        input_row = ttk.Frame(self.root)
        input_row.pack(side='bottom', fill='x', padx=5, pady=5)
        input_row.pack_propagate(False)  # Prevent frame from shrinking
        input_row.config(height=30)  # Fixed height

        #scrollable messages area
        self.canv = tk.Canvas(self.root, highlightthickness=0)
        ybar = tk.Scrollbar(self.root,command=self.canv.yview)
        self.canv.config(yscrollcommand=ybar.set)  
        ybar.pack(side='right', fill='y')
        self.canv.pack(side='top', expand=True, fill='both')
          
        self.messages_frame = tk.Frame(self.canv, padx=10, pady=3)
        self.canv_frame = self.canv.create_window((0, 0), window=self.messages_frame, anchor='nw')

        self.canv.bind('<Configure>', self._on_canvas_configure)

        #Input entry and send button
        self.entry = ttk.Entry(input_row)
        self.entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        self.send_button = ttk.Button(input_row, text="Send", command=lambda: self._handleSendMessage())
        self.send_button.pack(side='right')

        # Bind Enter key to send message
        self.entry.bind('<Return>', lambda e: self._handleSendMessage())
        self.entry.focus()
        

    def _handleSendMessage(self):
        """Handle send button or enter key press."""
        message = self.entry.get().strip()
        if message:
            self.add_message(message, isReceived=False)
            self.entry.delete(0, tk.END)


    # Make the frame expand to canvas width
    def _on_canvas_configure(self, event):
        """Handle canvas resize events."""
        self.canv.itemconfig(self.canv_frame, width=event.width)

        #update message wrap lengths
        new_label_width = self.messages_frame.winfo_width() * (3/5)
        for ml in self.message_labels:
            ml.config(wraplength=max(40, new_label_width))
        
        # Update scroll region after reconfiguring
        self.canv.update_idletasks()
        self.canv.config(scrollregion=self.canv.bbox("all"))


    def add_message(self, msg: str, username: str = "Anonymous", isReceived: bool = True):
        """
        Add a message to the chat window.
        
        Args:
            msg: The message text
            username: Username to display (only shown for received messages)
            isReceived: True for received messages (left, gray), False for sent (right, blue)
        """
        color = '#808080' if isReceived else '#218AFF'
        anchor = 'w' if isReceived else 'e'  # w=west (left), e=east (right)

        # create message container
        message_container = tk.Frame(self.messages_frame, padx=3)

        # Add username label for received messages
        if isReceived:
            username_label = tk.Label(message_container, text=username, fg='grey', height=1, font=('Helvetica', 7), padx=0)
            username_label.pack(side='top', anchor='w') #insert at top of container far left

        # create message label
        message_label = tk.Label(
            message_container,
            text=msg,
            background=color, 
            pady=5, 
            font=("Helvetica", 10)
        )
        message_label.pack(anchor='w') #insert message into container
        message_container.pack(anchor=anchor, pady=3) #insert container onto messages frame
        self.message_labels.append(message_label)
        
        # update wrap length
        message_container.update_idletasks()
        message_label.config(wraplength=max(40, self.messages_frame.winfo_width() * (3/5)))

        # Auto-scroll to bottom
        self.messages_frame.update_idletasks()
        self.canv.config(scrollregion=self.canv.bbox("all"))
        self.canv.yview_moveto(1.0)

    def run(self):
        """Start the UI main loop (blocking)."""
        self.root.mainloop()
        
    def destroy(self):
        """Close the window."""
        self.root.destroy()





