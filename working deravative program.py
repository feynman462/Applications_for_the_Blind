import sympy as sp
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    print(f"{text}")
    engine.say(text)
    engine.runAndWait()

def validate_expression(expr_str):
    try:
        return sp.sympify(expr_str)
    except sp.SympifyError:
        speak("Invalid expression. Please re-enter.")
        return None

def perform_operations():
    x = sp.Symbol('x')

    while True:
        speak("Select the operation you want to perform:")
        speak("1. Power Rule Derivative")
        speak("2. Quotient Rule Derivative")
        speak("3. Product Rule Derivative")
        speak("4. Chain Rule Derivative")
        speak("5. Indefinite Integral")
        speak("Type 'exit' to quit.")
        choice = input("Enter your choice: ")

        if choice.lower() == 'exit':
            break

        func_str = input("Enter a function: ")
        f = validate_expression(func_str)
        if f is None:
            continue

        if choice == '1':
            # Power Rule Derivative
            speak("Performing Power Rule Derivative...")
            power_rule_derivative = sp.diff(f, x)
            speak(f"The derivative using the power rule is: {power_rule_derivative}")
        elif choice == '2':
            # Quotient Rule Derivative
            speak("Performing Quotient Rule Derivative...")
            g_str = input("Enter a function for the denominator: ")
            g = validate_expression(g_str)
            if g is None:
                continue
            quotient_rule_derivative = (sp.diff(f, x) * g - f * sp.diff(g, x)) / g**2
            speak(f"The derivative using the quotient rule is: {quotient_rule_derivative}")
        elif choice == '3':
            # Product Rule Derivative
            speak("Performing Product Rule Derivative...")
            g_str = input("Enter a function for the other factor: ")
            g = validate_expression(g_str)
            if g is None:
                continue
            product_rule_derivative = f * sp.diff(g, x) + g * sp.diff(f, x)
            speak(f"The derivative using the product rule is: {product_rule_derivative}")
        elif choice == '4':
            # Chain Rule Derivative
            speak("Performing Chain Rule Derivative...")
            h_str = input("Enter an inner function for the chain rule: ")
            h = validate_expression(h_str)
            if h is None:
                continue
            chain_rule_derivative = sp.diff(f.subs(x, h), h) * sp.diff(h, x)
            speak(f"The derivative using the chain rule is: {chain_rule_derivative}")
        elif choice == '5':
            # Indefinite Integral
            speak("Performing Indefinite Integral...")
            indefinite_integral = sp.integrate(f, x)
            speak(f"The indefinite integral is: {indefinite_integral}")
        else:
            speak("Invalid choice. Please enter a valid option.")

def main():
    speak("Welcome to the Calculus Helper program for visually impaired users.")
    perform_operations()

if __name__ == "__main__":
    main()
