import subprocess

def welcome_message():
    print("\nWelcome to Factoring Numbers for the Blind!")

def get_number():
    while True:
        try:
            number = int(input("Please enter the number you would like to get the factors for: "))
            return number
        except ValueError:
            print("That's not a valid number. Please enter an integer value.")

def find_factors(number):
    return [i for i in range(1, number + 1) if number % i == 0]

def announce_factors(number, factors):
    factors_str = ', '.join(map(str, factors))
    print(f"The factors of {number} are: {factors_str}")

def ask_yes_no(question):
    while True:
        choice = input(question).lower()
        if choice in ['yes', 'no']:
            return choice == 'yes'
        else:
            print("Please enter 'yes' or 'no'.")

def copy_to_clipboard(text):
    try:
        # For Windows, use 'clip'
        # For MacOS, use 'pbcopy'
        # For Linux, you might use 'xclip' or 'xsel'
        command = 'pbcopy' if subprocess.os.name == 'posix' else 'clip'
        subprocess.run(command, universal_newlines=True, input=text, check=True)
        print("Copied to clipboard successfully!")
    except Exception as e:
        print("An error occurred while copying to the clipboard:", e)

def main():
    welcome_message()
    while True:
        number = get_number()
        factors = find_factors(number)
        announce_factors(number, factors)

        if ask_yes_no("Would you like to copy them to the clipboard? (yes/no): "):
            text = f"Number: {number}, Factors: {', '.join(map(str, factors))}"
            copy_to_clipboard(text)

        if not ask_yes_no("Would you like to find more factors? (yes/no): "):
            print("Alrighty, See you next time for some more number hunting. Bye!")
            break

if __name__ == "__main__":
    main()
