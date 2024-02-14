import sympy as sp
from tkinter import *
from tkinter import messagebox

x = sp.Symbol('x')

def ratio_test(series_function, variable):
    ratio = series_function / series_function.subs(variable, variable + 1)
    limit = sp.limit(ratio, variable, sp.oo)
    
    if limit < 1:
        return "convergent"
    elif limit > 1:
        return "divergent"
    else:
        return "inconclusive"

def root_test(series_function, variable):
    root = series_function**(1/variable)
    limit = sp.limit(root, variable, sp.oo)
    
    if limit < 1:
        return "convergent"
    elif limit > 1:
        return "divergent"
    else:
        return "inconclusive"

def integral_test(series_function, variable):
    integral = sp.integrate(series_function, (variable, 1, sp.oo))
    
    if integral.is_real:
        return "convergent"
    else:
        return "divergent"

def telescoping_test(series_function, variable):
    # Implement your telescoping test here
    pass

def run_tests():
    series_function = function_entry.get()
    if not series_function:
        messagebox.showerror("Error", "Please enter a function")
        return

    try:
        series_function_parsed = sp.sympify(series_function)
    except sp.SympifyError:
        messagebox.showerror("Error", "Invalid function format")
        return

    ratio_result = ratio_test(series_function_parsed, x)
    root_result = root_test(series_function_parsed, x)
    integral_result = integral_test(series_function_parsed, x)
    telescoping_result = telescoping_test(series_function_parsed, x)

    results_text = f"Ratio Test: The series is {ratio_result}.\n"
    results_text += f"Root Test: The series is {root_result}.\n"
    results_text += f"Integral Test: The series is {integral_result}.\n"
    results_text += f"Telescoping Test: The series is {telescoping_result}."

    messagebox.showinfo("Test Results", results_text)

# Create the tkinter application
root = Tk()
root.title("Series Convergence Tests")

# Create labels, entry, and buttons
function_label = Label(root, text="Function (e.g., 1/x**2):")
function_entry = Entry(root)
test_button = Button(root, text="Run Tests", command=run_tests)

# Place the elements in the grid
function_label.grid(row=0, column=0, sticky=W, pady=(10, 5))
function_entry.grid(row=1, column=0, padx=10, pady=5)
test_button.grid(row=2, column=0, padx=10, pady=(5, 10))

# Bind 'Enter' key to run_tests function
function_entry.bind('<Return>', lambda event: run_tests())

# Run the tkinter main loop
root.mainloop()
