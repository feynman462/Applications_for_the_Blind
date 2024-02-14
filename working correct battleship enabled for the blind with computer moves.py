import random
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

class Board:
    # ... unchanged ...

class Ship:
    # ... unchanged ...

class Player:
    def __init__(self, name, board):
        self.name = name
        self.board = board

    def place_ships(self, ships):
        for ship in ships:
            while True:
                print(f"Placing a {ship.name} which is {ship.length} units long")
                while True:
                    try:
                        x = int(input(f"Enter the x-coordinate to place your {ship.name}: "))
                        y = int(input(f"Enter the y-coordinate to place your {ship.name}: "))
                        direction = input("Place ship horizontally or vertically (H/V)? ").lower()
                        if self.valid_ship_placement(ship, x, y, direction):
                            horizontal = direction == 'h'
                            self.board.place_ship(ship, x, y, horizontal)
                            break
                        else:
                            print("Invalid position. Try again.")
                    except ValueError:
                        print("Invalid input. Enter a valid integer for x and y coordinates.")

    def valid_coordinates(self, x, y):
        return 0 <= x < self.board.width and 0 <= y < self.board.height

    def valid_ship_placement(self, ship, x, y, direction):
        if not self.valid_coordinates(x, y):
            return False
        if direction not in ['h', 'v']:
            return False
        if direction == 'h' and x + ship.length > self.board.width:
            return False
        if direction == 'v' and y + ship.length > self.board.height:
            return False
        return True

class Game:
    # ... unchanged ...

def main_menu(game=None):
    # ... unchanged ...

if __name__ == "__main__":
    main_menu()
