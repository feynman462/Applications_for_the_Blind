import random
import string
import pyttsx3
import requests
from flask import Flask, jsonify

app = Flask(__name__)
# Initialize the Text-to-Speech engine
engine = pyttsx3.init()

# Replace 'YOUR_RAPIDAPI_KEY' with your actual RapidAPI key
RAPIDAPI_KEY = 'YOUR_RAPIDAPI_KEY'

def speak(text):
    """Speak out the text for auditory feedback."""
    engine.say(text)
    engine.runAndWait()
    engine.stop()

@app.route('/getRandomWord', methods=['GET'])
def fetch_word_list(level):
    # Define your own logic to fetch word list based on the level.
    # You can use an API or a predefined list.
    # For simplicity, we'll use a predefined list here.
    word_list = ["word1", "word2", "word3"]  # Modify as needed
    return word_list

@app.route('/getRandomWord', methods=['GET'])
def get_random_word():
    """Fetch a random word from the API."""
    url = "https://random-word-by-api-ninjas.p.rapidapi.com/v1/randomword"
    headers = {
        'X-RapidAPI-Key': RAPIDAPI_KEY,
        'X-RapidAPI-Host': 'random-word-by-api-ninjas.p.rapidapi.com'
    }
    try:
        response = requests.get(url, headers=headers)
        word = response.json().get('word', 'defaultword')  # Modify as per actual response structure
        return jsonify(word=word)
    except requests.exceptions.RequestException as e:
        speak("Error fetching word: " + str(e))
        return jsonify(error=str(e)), 500

def place_word_in_grid(grid, word):
    """Attempt to place a word in the grid with random orientation."""
    size = len(grid)
    word_length = len(word)
    max_attempts = 100

    for _ in range(max_attempts):
        orientation = random.choice(['horizontal', 'vertical'])
        x, y = random.randint(0, size - word_length), random.randint(0, size - word_length)

        if can_place_word(grid, word, x, y, orientation):
            for i in range(word_length):
                if orientation == 'horizontal':
                    grid[y][x + i] = word[i]
                else:
                    grid[y + i][x] = word[i]
            return True
    return False  # If the word can't be placed after all attempts

    while attempts < max_attempts:
        orientation = random.randint(0, 1)
        start_x, start_y = random.randint(0, size - word_length), random.randint(0, size - 1)

        if orientation == 0 and all(grid[start_y][i] == '.' for i in range(start_x, start_x + word_length)):
            for i in range(word_length):
                grid[start_y][start_x + i] = word[i]
            return True
        elif orientation == 1 and all(grid[i][start_x] == '.' for i in range(start_y, start_y + word_length)):
            for i in range(word_length):
                grid[start_y + i][start_x] = word[i]
            return True

        attempts += 1
    return False  # Indicates that placement was unsuccessful

def can_place_word(grid, word, x, y, orientation):
    """Check if the word can be placed at the given position and orientation."""
    size = len(grid)
    word_length = len(word)

    if orientation == 'horizontal' and x + word_length <= size:
        if all(grid[y][x + i] == '.' for i in range(word_length)):
            return True

    if orientation == 'vertical' and y + word_length <= size:
        if all(grid[y + i][x] == '.' for i in range(word_length)):
            return True

    return False

def fill_empty_spots(grid):
    """Fill the empty spots in the grid with random letters."""
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == '.':
                grid[y][x] = random.choice(string.ascii_uppercase)

def generate_grid(size, word_list):
    """Generate a grid and populate it with words."""
    grid = [['.' for _ in range(size)] for _ in range(size)]
    for word in word_list:
        if not place_word_in_grid(grid, word):
            speak(f"Warning: Could not place word {word} in the grid.")
            print(f"Warning: Could not place word {word} in the grid.")
    fill_empty_spots(grid)
    return grid
    for y in range(size):
        for x in range(size):
            if grid[y][x] == '.':
                grid[y][x] = random.choice(string.ascii_uppercase)
    return grid

def print_grid(grid):
    """Print the grid - primarily for testing purposes."""
    for row in grid:
        print(' '.join(row))

def read_letter(grid, x, y):
    """Reads the letter at the specified position."""
    return grid[y][x]

def navigate(grid, x, y, direction):
    """Navigate through the grid based on user input."""
    # Navigation logic
    if direction == 'UP' and y > 0: y -= 1
    elif direction == 'DOWN' and y < len(grid) - 1: y += 1
    elif direction == 'LEFT' and x > 0: x -= 1
    elif direction == 'RIGHT' and x < len(grid[0]) - 1: x += 1
        x += 1
    return x, y

def is_adjacent(first, second):
    """Checks if the second position is adjacent to the first."""
    fx, fy = first
    sx, sy = second
    return abs(fx - sx) <= 1 and abs(fy - sy) <= 1

def check_word(grid, selected_letters, word_list):
    """Check if selected letters form a valid word."""
    word = ''.join(grid[y][x] for x, y in selected_letters)
    reversed_word = word[::-1]
    return word in word_list or word[::-1] in word_list

def get_adjacent_positions(x, y, size):
    adjacent_positions = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < size and 0 <= new_y < size:
                adjacent_positions.append((new_x, new_y))
    return adjacent_positions

def can_select_letter(selected_letters, new_position, grid):
    """Checks if the new letter position can be selected based on the game rules."""
    if not selected_letters:  # First letter can always be selected
        return True
    if len(selected_letters) == 1:  # Second letter must be adjacent
        return new_position in get_adjacent_positions(*selected_letters[0], len(grid))
    # Subsequent letters must be in a straight line
    first, second = selected_letters[0], selected_letters[1]
    direction = (second[0] - first[0], second[1] - first[1])
    expected_position = (second[0] + direction[0], second[1] + direction[1])
    return new_position == expected_position

from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/getRandomWord', methods=['GET'])
def get_random_word():
    url = "https://exampleapi.p.rapidapi.com/randomword"  # The API endpoint from RapidAPI
    headers = {
        'x-rapidapi-host': "exampleapi.p.rapidapi.com",  # The API host from RapidAPI
        'x-rapidapi-key': "YOUR_RAPIDAPI_KEY"  # Your RapidAPI Key
    }

    response = requests.get(url, headers=headers)
    word = response.json()  # Extracting word depends on the API's response structure

    return jsonify(word=word)

if __name__ == '__main__':
    app.run()

def main():
    # [Main function logic]
    speak("Welcome to Word Connect For The Blind!")
    print("Welcome to Word Connect For The Blind!")

    size = 15  # Grid size
    level = 'easy'  # The level can be changed as needed or prompted from the user
    word_list = fetch_word_list(level)
    grid = generate_grid(size, word_list)

    print_grid(grid)
    hints_on = False
    player_position = (0, 0)
    selected_letters = []

    # Game loop
    while True:
        command = input("Enter command: ").upper()
        if command == 'Q':
            speak("Goodbye!")
            break
        elif command == 'HINTS':
            hints_on = not hints_on
            speak("Hints turned on." if hints_on else "Hints turned off.")
            if hints_on:
                speak(f"Words to find: {', '.join(word_list)}")

        x, y = player_position

        if command in ['W', 'A', 'S', 'D']:
            new_x, new_y = navigate(grid, x, y, command)
            if (new_x, new_y) != player_position:
                player_position = (new_x, new_y)
                current_letter = read_letter(grid, new_x, new_y)
                speak(f"Moved to {current_letter}.")
                print(f"Current position: {new_x}, {new_y}")
            else:
                speak("You can't move in that direction.")
        elif command == 'SPACE':
            new_position = (x, y)
            if can_select_letter(selected_letters, new_position, grid):
                selected_letters.append(new_position)
                selected_letters_string = ''.join(read_letter(grid, px, py) for px, py in selected_letters)
                speak(f"Selected letters: {selected_letters_string}")
                print(f"Selected letters: {selected_letters_string}")
            else:
                speak("Invalid selection.")
                print("Invalid selection.")
        elif command == 'F':
            correct = check_word(grid, selected_letters, word_list)
            result_message = "Correct word!" if correct else "Incorrect word."
            speak(result_message)
            print(result_message)
            selected_letters = []

    speak("Thank you for playing Word Connect For The Blind!")
    print("Thank you for playing Word Connect For The Blind!")

if __name__ == '__main__':
    app.run()
    main()
