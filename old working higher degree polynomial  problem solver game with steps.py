from sympy import symbols, Eq, solve
import pyttsx3

engine = pyttsx3.init()
x = symbols('x')

def speak(text):
    engine.say(text)
    engine.runAndWait()

def solve_polynomial(coefficients):
    # Generate the equation
    equation_text = "You entered the equation: " + ' + '.join([
        f"{coefficients[i]}*x^{len(coefficients) - i - 1}" if len(coefficients) - i - 1 > 1 else
        (f"{coefficients[i]}*x" if len(coefficients) - i - 1 == 1 else
        f"{coefficients[i]}")
        for i in range(len(coefficients))]) + " = 0"

    print(equation_text)
    speak(equation_text)

    # Solve the equation
    solutions = solve(Eq(sum([coefficients[len(coefficients) - i - 1]*x**i for i in range(len(coefficients))]), 0))

    solution_text = "The solutions are:"
    print(solution_text)
    speak(solution_text)

    for i, sol in enumerate(solutions):
        sol_text = "Solution {} is: {}".format(i+1, sol)
        print(sol_text)
        speak(sol_text)

    return solutions

def main():
    while True:
        welcome_text = "Welcome to the polynomial equation solver!"
        print(welcome_text)
        speak(welcome_text)

        instruction_text = "Please enter the coefficients of the polynomial equation in decreasing order of the powers, separated by commas"
        print(instruction_text)
        speak(instruction_text)

        coefficients = list(map(int, input("Enter coefficients: ").split(',')))

        solve_polynomial(coefficients)

        another_text = "Would you like to solve another equation? Type 'yes' to continue or 'no' to quit."
        print(another_text)
        speak(another_text)

        another_equation = input()
        if another_equation.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
