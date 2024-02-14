import pyttsx3
import random
import keyboard
import time

# Initialize the speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

class Card:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.rank = Card.values.index(value)

    def __str__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(s, v) for s in Card.suits for v in Card.values]
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None

def setup_game():
    deck = Deck()
    tableau = [[] for _ in range(7)]
    waste_pile = []
    foundations = {suit: [] for suit in Card.suits}
    
    for i in range(7):
        for j in range(i, 7):
            tableau[j].append(deck.draw())
    
    return deck, tableau, waste_pile, foundations

def can_place_on_tableau(card, pile):
    if not pile:
        return card.value == 'King'
    top_card = pile[-1]
    return (card.rank == top_card.rank - 1 and card.suit in ('Hearts', 'Diamonds') and top_card.suit in ('Clubs', 'Spades')) or (card.rank == top_card.rank - 1 and card.suit in ('Clubs', 'Spades') and top_card.suit in ('Hearts', 'Diamonds'))

def check_auto_move_to_foundation(card, foundations):
    if card.value == 'Ace':
        foundations[card.suit].append(card)
        return True
    if foundations[card.suit] and foundations[card.suit][-1].rank == card.rank - 1:
        foundations[card.suit].append(card)
        return True
    return False

def check_victory(foundations):
    for pile in foundations.values():
        if not pile or pile[-1].value != 'King':
            return False
    return True

def handle_space_key(tableau, waste_pile, foundations, current_pile, current_mode, selected_card, source_pile):
    if selected_card:
        if current_mode == "tableau":
            if can_place_on_tableau(selected_card, tableau[current_pile]):
                tableau[current_pile].append(selected_card)
                selected_card = None
                source_pile = None
                speak("Card placed.")
            else:
                speak("Cannot place card here.")
        else:
            speak("You cannot place cards directly onto the waste pile.")
    else:
        if current_mode == "tableau" and tableau[current_pile]:
            selected_card = tableau[current_pile].pop()
            source_pile = "tableau"
            if check_auto_move_to_foundation(selected_card, foundations):
                selected_card = None
                source_pile = None
                speak(f"Card automatically moved to foundation.")
            else:
                speak(f"You picked up {selected_card}.")
        elif current_mode == "waste" and waste_pile:
            selected_card = waste_pile.pop()
            source_pile = "waste"
            speak(f"You picked up {selected_card}.")

    return selected_card, source_pile

def handle_foundation_key(tableau, waste_pile, foundations, current_pile, current_mode, selected_card, source_pile):
    if selected_card:
        if check_auto_move_to_foundation(selected_card, foundations):
            selected_card = None
            source_pile = None
            speak(f"Card moved to foundation.")
        else:
            speak("Card cannot be placed in foundation.")
    
    return selected_card, source_pile

def handle_info_key(tableau, waste_pile, current_mode, current_pile):
    if current_mode == "tableau":
        speak(f"Pile {current_pile+1} has {len(tableau[current_pile])} cards.")
        if tableau[current_pile]:
            speak(f"Top card is {tableau[current_pile][-1]}.")
        else:
            speak("Pile is empty.")
    elif current_mode == "waste":
        if waste_pile:
            speak(f"Top card of waste is {waste_pile[-1]}")
        else:
            speak("Waste pile is empty.")

def speak_help():
    speak("Navigate with arrow keys. Press space to pick or place a card. D to draw from deck. I for information. F to try auto placing to foundation. W to switch to waste pile. Q to quit.")

def main():
    speak("Welcome to Solitaire for the Blind.")
    
    deck, tableau, waste_pile, foundations = setup_game()
    
    current_pile = 0
    current_mode = "tableau"
    selected_card = None
    source_pile = None

    last_command_time = time.time()

    while True:
        # Adding a delay to avoid multiple actions in quick succession
        while time.time() - last_command_time < 0.5:
            pass

        if check_victory(foundations):
            speak("Congratulations! You have won the game!")
            break

        if current_mode == "tableau":
            speak(f"You're on tableau pile {current_pile + 1}.")
        elif current_mode == "waste":
            speak("You're on the waste pile.")
        
        try:
            if keyboard.is_pressed('right'):
                if current_mode == "tableau":
                    current_pile = (current_pile + 1) % 7
                elif current_mode == "waste":
                    current_mode = "tableau"
                    current_pile = 0
            elif keyboard.is_pressed('left'):
                if current_mode == "tableau":
                    current_pile = (current_pile - 1) % 7
                elif current_mode == "waste":
                    current_mode = "tableau"
                    current_pile = 6
            elif keyboard.is_pressed('d'):
                if selected_card:
                    speak("You can't draw a card while holding another.")
                elif deck.cards:
                    waste_pile.append(deck.draw())
                    speak(f"Card drawn: {waste_pile[-1]}")
                else:
                    speak("The deck is empty.")
            elif keyboard.is_pressed('space'):
                selected_card, source_pile = handle_space_key(tableau, waste_pile, foundations, current_pile, current_mode, selected_card, source_pile)
            elif keyboard.is_pressed('f'):
                selected_card, source_pile = handle_foundation_key(tableau, waste_pile, foundations, current_pile, current_mode, selected_card, source_pile)
            elif keyboard.is_pressed('i'):
                handle_info_key(tableau, waste_pile, current_mode, current_pile)
            elif keyboard.is_pressed('h'):
                speak_help()
            elif keyboard.is_pressed('w'):
                if current_mode == "waste":
                    current_mode = "tableau"
                    current_pile = 0
                else:
                    current_mode = "waste"
            elif keyboard.is_pressed('q'):
                if selected_card:
                    speak("You can't quit while holding a card. Place the card or press Q again to quit.")
                    selected_card = None
                else:
                    speak("Quitting the game.")
                    break
        except KeyboardInterrupt:
            speak("Quitting the game.")
            break

        last_command_time = time.time()

if __name__ == "__main__":
    main()
