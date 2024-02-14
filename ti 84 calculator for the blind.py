import numpy as np
import tkinter as tk
from tkinter import simpledialog, messagebox
import math
from enum import Enum
import pyttsx3
import pyperclip
import ast

engine = pyttsx3.init()

PI = math.pi
EULER = math.e

class Operations(Enum):
    ADD = '+'
    SUBTRACT = '-'
    MULTIPLY = '*'
    DIVIDE = '/'
    SQUARE_ROOT = 'sqrt'
    FACTORIAL = '!'
    ABS = 'abs'
    ROUND = 'round'
    LOG_BASE = 'log_base'
    SOLVE_SYSTEM = 'solve_system'
    GRAPH = 'graph'
    SIN = 'sin'
    COS = 'cos'
    TAN = 'tan'
    EXP = 'exp'
    POW = 'pow'
    MAT_ADD = 'mat_add'
    MAT_SUB = 'mat_sub'
    MAT_MUL = 'mat_mul'
    MAT_DET = 'mat_det'
    MAT_INV = 'mat_inv'
    QUIT = 'quit'

def speak(text):
    engine.say(text)
    engine.runAndWait()

def validate_matrix_input(input_string):
    try:
        matrix = np.array(ast.literal_eval(input_string))
        if matrix.ndim != 2:
            return None
        return matrix
    except:
        return None

def perform_operation(operation, arg1, arg2=None):
    # unchanged code

def get_input_and_perform_operation(event=None):
    operation = simpledialog.askstring("Operation", "Enter operation or 'quit' to exit:")
    if not operation:
        speak("Operation was cancelled.")
        return
    if operation.lower() == Operations.QUIT.value:
        root.destroy()
        return

    # Matrix operations
    elif operation.lower() in {Operations.MAT_ADD.value, Operations.MAT_SUB.value, Operations.MAT_MUL.value}:
        arg1 = validate_matrix_input(simpledialog.askstring("Matrix 1", "Enter matrix 1 as a 2D list:"))
        if arg1 is None:
            speak("Invalid matrix 1 input.")
            return
        arg2 = validate_matrix_input(simpledialog.askstring("Matrix 2", "Enter matrix 2 as a 2D list:"))
        if arg2 is None:
            speak("Invalid matrix 2 input.")
            return
    elif operation.lower() in {Operations.MAT_DET.value, Operations.MAT_INV.value}:
        arg1 = validate_matrix_input(simpledialog.askstring("Matrix", "Enter matrix as a 2D list:"))
        if arg1 is None:
            speak("Invalid matrix input.")
            return
        arg2 = None
    else:
        arg1 = simpledialog.askfloat("Argument 1", "Enter first argument:")
        if arg1 is None:
            speak("Invalid argument 1 input.")
            return
        if operation.lower() not in {Operations.SQUARE_ROOT.value, Operations.FACTORIAL.value, Operations.ABS.value, Operations.ROUND.value, Operations.SIN.value, Operations.COS.value, Operations.TAN.value, Operations.EXP.value}:
            arg2 = simpledialog.askfloat("Argument 2", "Enter second argument:")
            if arg2 is None:
                speak("Invalid argument 2 input.")
                return
        else:
            arg2 = None
    result = perform_operation(operation, arg1, arg2)
    # unchanged code

root = tk.Tk()
root.withdraw()

instructions = """
Welcome to the blind graphing calculator. 
Press enter or click the 'Perform Operation' button to start. 
You can perform basic operations such as addition, subtraction, multiplication, and division by entering the corresponding symbols. 
For advanced operations, you can enter 'sqrt' for square root, '!' for factorial, 'abs' for absolute value, and 'round' for rounding, 
'log_base' for logarithm with base.
To graph a function, enter 'graph' and provide the function in terms of x.
To solve a system of equations, enter 'solve_system' and provide the system of equations, separated by commas.
For matrix operations, enter 'mat_add' for addition, 'mat_sub' for subtraction, 'mat_mul' for multiplication, 'mat_det' for determinant and 'mat_inv' for inverse.
To quit, enter 'quit'.
The result will be copied to the clipboard.
"""
print(instructions)
speak(instructions)

# GUI setup
root.title("Blind Graphing Calculator")
root.geometry("400x200")
frame = tk.Frame(root)
frame.pack()

info_label = tk.Label(frame, text="Please click the button or press Enter to start an operation.")
info_label.pack(side=tk.TOP)

button = tk.Button(frame, text="Perform Operation", command=get_input_and_perform_operation)
button.pack(side=tk.BOTTOM)
root.bind('<Return>', get_input_and_perform_operation)

root.mainloop()
    