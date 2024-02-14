import pygame
import sys
from pygame.locals import *

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Define keyboard keys mapping to piano notes
key_to_note = {
    K_a: "C4",
    K_s: "D4",
    K_d: "E4",
    K_f: "F4",
    K_g: "G4",
    K_h: "A4",
    K_j: "B4",
    K_k: "C5",
}

# Load piano note sounds
note_sounds = {
    note: pygame.mixer.Sound(f"piano_sounds/{note}.wav") for note in key_to_note.values()
}

# Set up the display window
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Keyboard Instruments")

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

        # Play note when key is
