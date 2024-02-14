import time

# Initialize the game state
game_state = [
    [" ", " ", " ", "G"],
    [" ", " ", "P", " "],
    [" ", " ", " ", " "],
    [" ", "G", " ", " "],
]

# Game loop
while True:
    # Read the player's input
    direction = input("Enter a direction (up, down, left, right): ")

    # Update the game state based on the player's input
    # This is simplified for the example and doesn't include logic for ghosts, walls, or pellets
    for y in range(len(game_state)):
        for x in range(len(game_state[y])):
            if game_state[y][x] == "P":
                game_state[y][x] = " " # Pac-Man leaves an empty space behind
                if direction == "up":
                    game_state[y-1][x] = "P"
                elif direction == "down":
                    game_state[y+1][x] = "P"
                elif direction == "left":
                    game_state[y][x-1] = "P"
                elif direction == "right":
                    game_state[y][x+1] = "P"
    
    # Check if a ghost is nearby and play a sound
    # This is also simplified and doesn't actually play a sound
    for y in range(len(game_state)):
        for x in range(len(game_state[y])):
            if game_state[y][x] == "G":
                if abs(y - y) <= 1 and abs(x - x) <= 1:  # If the ghost is within 1 space of Pac-Man
                    print("Ghost sound!")  # In a real game, this would play a sound instead of printing text

    # Print the game state
    for row in game_state:
        print(" ".join(row))
    
    time.sleep(0.5)  # Pause for a bit before the next loop
