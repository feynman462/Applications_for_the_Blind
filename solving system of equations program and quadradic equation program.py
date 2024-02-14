import numpy as np
import pyperclip
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def solve_linear(equations):
    coefficients = []
    constants = []

    for equation in equations:
        parts = equation.split('=')
        coefficients.append([int(i) for i in parts[0].split(',')])
        constants.append(int(parts[1]))

    coefficients = np.array(coefficients)
    constants = np.array(constants)

    solutions = np.linalg.solve(coefficients, constants)

    return solutions

def solve_quadratic(a, b, c):
    root1 = (-b + np.sqrt(b**2 - 4*a*c)) / (2*a)
    root2 = (-b - np.sqrt(b**2 - 4*a*c)) / (2*a)

    return [root1, root2]

speak("Welcome! This program can solve quadratic equations and system of linear equations.")
while True:
    speak("\nEnter '1' to solve a system of two linear equations (x+y=#).")
    speak("Enter '2' to solve a system of three linear equations (x+y+z=#).")
    speak("Enter '3' to solve a quadratic equation (ax^2+bx+c=#).")
    speak("Type 'exit' to quit.")
    option = input()
    if option == '1' or option == '2':
        speak("\nEnter your system of linear equations in the format ax,bx,cx=d (omit cx if solving for two variables) where a, b, c, and d are coefficients. One equation per line. Enter 'done' when finished.")
        equations = []
        while True:
            equation = input()
            if equation.lower() == 'done':
                break
            equations.append(equation)
        solutions = solve_linear(equations)
        speak(f"\nThe solution to your system of equations is: {solutions}")
        speak("Do you want to copy the results? (yes/no)")
        if input().lower() == 'yes':
            pyperclip.copy(str(solutions))
            speak("Results copied to clipboard.")
    elif option == '3':
        speak("\nEnter the coefficients a, b, c of the quadratic equation ax^2+bx+c=0.")
        a = int(input("Enter a: "))
        b = int(input("Enter b: "))
        c = int(input("Enter c: "))
        solutions = solve_quadratic(a, b, c)
        speak(f"\nThe roots of your quadratic equation are: {solutions}")
        speak("Do you want to copy the results? (yes/no)")
        if input().lower() == 'yes':
            pyperclip.copy(str(solutions))
            speak("Results copied to clipboard.")
    elif option.lower() == 'exit':
        break
    else:
        speak("\nInvalid option. Please try again.")
