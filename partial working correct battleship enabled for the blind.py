import random
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

class Ship:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.hits = 0

    def hit(self):
        self.hits += 1

    def is_sunk(self):
        return self.hits == self.size

class Game:
    def __init__(self, width, height, num_ships):
        self.width = width
        self.height = height
        self.num_ships = num_ships
        self.ships = []
        self.board = [[None for _ in range(width)] for _ in range(height)]
        self.create_ships()

    def create_ships(self):
        for _ in range(self.num_ships):
            while True:
                name = f"Ship {len(self.ships) + 1}"
                size = random.randint(2, 5)
                x = random.randint(0, self.width - size)
                y = random.randint(0, self.height - 1)

                if not any(self.board[y][x + j] for j in range(size)):
                    for j in range(size):
                        self.board[y][x + j] = Ship(name, size)
                    self.ships.append(Ship(name, size))
                    break

    def play(self):
        speak("Welcome to Battleship! Let's start the game.")
        while not self.is_game_over():
            self.print_board()
            move = self.get_move()
            if not self.do_move(move):
                speak("Invalid move!")

        speak("Game over!")

    def get_move(self):
        speak("Please enter the row and column coordinates separated by a space.")
        while True:
            try:
                x, y = input().strip().split()
                x, y = int(x), int(y)
                if not (0 <= x < self.width and 0 <= y < self.height):
                    speak("Invalid input! Please enter a valid coordinate.")
                else:
                    return x, y
            except ValueError:
                speak("Invalid input! Please enter a valid coordinate.")

    def do_move(self, move):
        x, y = move
        ship = self.board[y][x]
        if ship:
            if ship.is_sunk():
                speak(f"You hit an already sunk {ship.name}!")
            else:
                ship.hit()
                speak(f"You hit a {ship.name}!")
                if ship.is_sunk():
                    speak(f"You sunk a {ship.name}!")
            return True
        else:
            speak("Miss!")
            return False

    def is_game_over(self):
        return all(ship.is_sunk() for ship in self.ships)

    def print_board(self):
        for row in self.board:
            print(" ".join("X" if ship else "." for ship in row))

if __name__ == "__main__":
    game = Game(10, 10, 5)
    game.play()
