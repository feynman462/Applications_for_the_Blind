import sympy as sp
import pyperclip
import pyttsx3
import re

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def convert_to_python_expression(expression):
    expression = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expression)
    expression = expression.replace('^', '**')
    return expression

def human_readable_poly(poly):
    return str(poly.as_expr()).replace('**', '^')

def parse_polynomial(expression, variable):
    try:
        python_expression = convert_to_python_expression(expression)
        parsed_expression = sp.sympify(python_expression, locals={variable.name: variable})
        if not parsed_expression.is_polynomial():
            raise ValueError("Input is not a valid polynomial.")
        poly = sp.Poly(parsed_expression, variable)
    except (sp.SympifyError, ValueError) as e:
        raise ValueError(f"Invalid polynomial expression: {e}")
    return poly

def generate_step_description(remainder, divisor_poly, step_number):
    # Correctly extracting the leading terms
    leading_term_dividend = remainder.LT()[0] * remainder.gen**remainder.degree()
    leading_term_divisor = divisor_poly.LT()[0] * divisor_poly.gen**divisor_poly.degree()
    term_quotient = leading_term_dividend / leading_term_divisor
    new_remainder = remainder - term_quotient * divisor_poly
    description = (f"Step {step_number}: Divide the leading term of the remainder ({human_readable_poly(leading_term_dividend)}) "
                   f"by the leading term of the divisor ({human_readable_poly(leading_term_divisor)}).\n"
                   f"-> This gives the term {human_readable_poly(term_quotient)}.\n"
                   f"-> Multiply the divisor {human_readable_poly(divisor_poly)} by {human_readable_poly(term_quotient)} and subtract from the remainder.\n"
                   f"-> Updated remainder: {human_readable_poly(new_remainder)}.\n")
    return term_quotient, new_remainder, description

def polynomial_long_division(dividend, divisor):
    x = sp.symbols('x')
    dividend_poly = parse_polynomial(dividend, x)
    divisor_poly = parse_polynomial(divisor, x)

    if divisor_poly == 0:
        raise ValueError("Divisor cannot be zero.")

    if sp.degree(dividend_poly) < sp.degree(divisor_poly):
        raise ValueError("Degree of dividend must be greater than or equal to the divisor.")

    quotient_terms = []
    remainder = dividend_poly
    step_descriptions = []
    step_number = 1

    while remainder != 0 and sp.degree(remainder) >= sp.degree(divisor_poly):
        term_quotient, new_remainder, step_description = generate_step_description(remainder, divisor_poly, step_number)
        quotient_terms.append(term_quotient)
        step_descriptions.append(step_description)
        remainder = new_remainder
        step_number += 1

    final_quotient = sum(quotient_terms)
    final_description = (f"Final Quotient: {human_readable_poly(final_quotient)}\n"
                         f"Final Remainder: {human_readable_poly(remainder)}")
    step_descriptions.append(final_description)
    return final_quotient, remainder, step_descriptions

def main():
    try:
        speak("Enter the dividend polynomial.")
        dividend = input("Enter the dividend polynomial (e.g., 'x^3 - 19x - 30'): ")
        speak("Now, enter the divisor polynomial.")
        divisor = input("Enter the divisor polynomial (e.g., 'x - 5'): ")

        quotient, remainder, division_steps = polynomial_long_division(dividend, divisor)
        detailed_steps = "\n".join(division_steps)
        print(detailed_steps)

        speak("Do you want to copy the steps to the clipboard?")
        if input("Copy steps to clipboard? (y/n): ").strip().lower() == 'y':
            pyperclip.copy(detailed_steps)
            print("Steps copied to clipboard.")
            speak("Steps copied to clipboard.")

        speak("Do you want to hear the steps read aloud?")
        if input("Read steps aloud? (y/n): ").strip().lower() == 'y':
            speak(detailed_steps)

    except ValueError as ve:
        error_message = f"Input error: {ve}"
        print(error_message)
        speak(error_message)
        with open("error_log.txt", "a") as file:
            file.write(error_message + "\n")
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        print(error_message)
        speak(error_message)
        with open("error_log.txt", "a") as file:
            file.write(error_message + "\n")

if __name__ == "__main__":
    main()
