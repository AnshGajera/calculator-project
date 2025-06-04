import tkinter as tk

# Global variables for calculator logic
current_number = ""
first_num = None
operation = None
history_string = "" # To store the mathematical process

# --- Color Palette (inspired by Windows Calculator) ---
BG_COLOR = "#F0F0F0"         # Light grey for the overall background
DISPLAY_COLOR = "#FFFFFF"     # White for the display background
TEXT_COLOR = "#333333"       # Dark grey for general text
BUTTON_BG_COLOR = "#FFFFFF"   # White for number and decimal buttons
OPERATOR_BG_COLOR = "#F8F8F8" # Slightly darker grey for operator buttons
EQUALS_BG_COLOR = "#E0B36D"   # Orange/gold for the equals button (common in some designs)
CLEAR_BG_COLOR = "#F8F8F8"    # Same as operator for clear

# --- Font Settings ---
HISTORY_FONT = ("Segoe UI", 12)
DISPLAY_FONT = ("Segoe UI", 24, "bold")
BUTTON_FONT = ("Segoe UI", 16)

def button_click(number):
    """Appends the clicked number/decimal to the display."""
    global current_number
    if "Error" in display.get(): # Clear error message before new input
        current_number = ""
        display.delete(0, tk.END)

    if str(number) == '.' and '.' in current_number: # Prevent multiple decimal points
        return

    current_number += str(number)
    display.delete(0, tk.END)
    display.insert(0, current_number)

def button_operation(op):
    """Stores the first number and the chosen operation, updates history."""
    global first_num, operation, current_number, history_string

    if "Error" in display.get():
        reset_calculator()
        return

    try:
        if current_number:
            first_num = float(current_number)
            history_string = f"{format_number(first_num)} {op} "
        elif first_num is not None: # Allow changing operation if first_num already exists
             # Update history to reflect new operation
             if history_string:
                 history_string = f"{format_number(first_num)} {op} "
        else: # If no number and no first_num, clear and show error
            display.delete(0, tk.END)
            display.insert(0, "Error")
            reset_calculator()
            return # Exit to prevent further processing

        operation = op
        current_number = "" # Reset for the next input
        display.delete(0, tk.END)
        history_display.config(text=history_string) # Update history display
    except ValueError:
        display.delete(0, tk.END)
        display.insert(0, "Error")
        reset_calculator()

def button_equals():
    """Performs the calculation and displays the result, updates history."""
    global first_num, operation, current_number, history_string

    if first_num is None or operation is None or not current_number:
        display.delete(0, tk.END)
        display.insert(0, "Error")
        reset_calculator()
        return

    try:
        second_num = float(current_number)
        result = 0

        # Update history with the full expression before calculation
        history_string += f"{format_number(second_num)} ="
        history_display.config(text=history_string)


        if operation == '+':
            result = first_num + second_num
        elif operation == '-':
            result = first_num - second_num
        elif operation == '*':
            result = first_num * second_num
        elif operation == '/':
            if second_num == 0:
                display.delete(0, tk.END)
                display.insert(0, "Error: Div by 0")
                reset_calculator()
                return
            result = first_num / second_num

        display.delete(0, tk.END)
        # Format result to avoid excessive decimal places if it's an integer
        if abs(result - int(result)) < 1e-9: # Check if it's very close to an integer
            display.insert(0, int(result))
        else:
            display.insert(0, result)

        # Allow chaining operations: result becomes the new first_num
        first_num = result
        operation = None # Reset operation for subsequent calculations
        current_number = str(result) # Update current_number with result for further clicks
        history_string = "" # Clear history after equals, new calculation starts fresh
    except ValueError:
        display.delete(0, tk.END)
        display.insert(0, "Error")
        reset_calculator()
    except Exception: # Catch any other unexpected errors
        display.delete(0, tk.END)
        display.insert(0, "Error")
        reset_calculator()

def button_clear():
    """Resets all calculator variables and clears the display."""
    reset_calculator()
    display.insert(0, "0") # Display '0' after clear

def reset_calculator():
    """Helper function to reset global state."""
    global current_number, first_num, operation, history_string
    current_number = ""
    first_num = None
    operation = None
    history_string = ""
    display.delete(0, tk.END)
    history_display.config(text="") # Clear history display

def format_number(num):
    """Formats a float to an int if it's a whole number."""
    if abs(num - int(num)) < 1e-9:
        return str(int(num))
    return str(num)

def toggle_sign():
    """Toggles the sign of the current number."""
    global current_number
    if current_number and "Error" not in display.get():
        try:
            num = float(current_number)
            num *= -1
            current_number = format_number(num)
            display.delete(0, tk.END)
            display.insert(0, current_number)
        except ValueError:
            pass # Do nothing if current_number is not a valid number

def clear_entry():
    """Clears only the current number being entered."""
    global current_number
    current_number = ""
    display.delete(0, tk.END)
    display.insert(0, "0")


# --- GUI Setup ---
root = tk.Tk()
root.title("Simple Calculator")
root.geometry("300x450") # Set initial size, but allow resizing
root.configure(bg=BG_COLOR) # Set background color for the main window

# History Display (Label)
history_display = tk.Label(root, text="", anchor="e", font=HISTORY_FONT,
                           bg=DISPLAY_COLOR, fg=TEXT_COLOR, padx=10, pady=5)
history_display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=(10, 0)) # pady top only

# Main Display Entry Widget
display = tk.Entry(root, width=15, borderwidth=0, font=DISPLAY_FONT, justify="right",
                   bg=DISPLAY_COLOR, fg=TEXT_COLOR, relief="flat", highlightthickness=0)
display.grid(row=1, column=0, columnspan=4, padx=10, pady=(0, 10), ipady=10, sticky="nsew") # pady bottom only
display.insert(0, "0") # Initial display

# --- Define buttons and their layout ---
# (text, row, column, type) type can be 'num', 'op', 'clear', 'equals', 'clear_entry', 'toggle_sign'
buttons_data = [
    ('C', 2, 0, 'clear'), ('CE', 2, 1, 'clear_entry'), ('%', 2, 2, 'op'), ('/', 2, 3, 'op'),
    ('7', 3, 0, 'num'), ('8', 3, 1, 'num'), ('9', 3, 2, 'num'), ('*', 3, 3, 'op'),
    ('4', 4, 0, 'num'), ('5', 4, 1, 'num'), ('6', 4, 2, 'num'), ('-', 4, 3, 'op'),
    ('1', 5, 0, 'num'), ('2', 5, 1, 'num'), ('3', 5, 2, 'num'), ('+', 5, 3, 'op'),
    ('±', 6, 0, 'toggle_sign'), ('0', 6, 1, 'num'), ('.', 6, 2, 'num'), ('=', 6, 3, 'equals')
]

# Configure grid weights to make cells expand proportionally
# History display is row 0, main display is row 1
root.grid_rowconfigure(0, weight=1) # History display row
root.grid_rowconfigure(1, weight=2) # Main display row (larger)
for i in range(2, 7): # Rows for buttons (from row 2 to row 6)
    root.grid_rowconfigure(i, weight=3) # Buttons expand more than history, but less than main display
for i in range(4): # Columns 0-3
    root.grid_columnconfigure(i, weight=1)


# Create and place buttons
for (text, r, c, btn_type) in buttons_data:
    button_command = None
    button_bg = BUTTON_BG_COLOR

    if btn_type == 'num':
        button_command = lambda t=text: button_click(t)
    elif btn_type == 'op':
        button_command = lambda t=text: button_operation(t)
        button_bg = OPERATOR_BG_COLOR
    elif btn_type == 'clear':
        button_command = button_clear
        button_bg = CLEAR_BG_COLOR
    elif btn_type == 'clear_entry':
        button_command = clear_entry
        button_bg = CLEAR_BG_COLOR
    elif btn_type == 'equals':
        button_command = button_equals
        button_bg = EQUALS_BG_COLOR
    elif btn_type == 'toggle_sign':
        button_command = toggle_sign
        button_bg = OPERATOR_BG_COLOR # Often styled like an operator

    btn = tk.Button(root, text=text, font=BUTTON_FONT,
                    bg=button_bg, fg=TEXT_COLOR,
                    activebackground="#DDDDDD" if btn_type not in ('equals', 'op', 'clear', 'clear_entry', 'toggle_sign') else "#B8995C" if btn_type == 'equals' else "#E0E0E0", # Hover color
                    relief="flat", bd=0, # Flat border, no border thickness
                    command=button_command)
    btn.grid(row=r, column=c, sticky="nsew", padx=1, pady=1) # sticky fills cell, padx/y for gaps

# Start the GUI event loop
root.mainloop()