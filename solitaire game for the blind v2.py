import pyttsx3
import keyboard
import random
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
    for foundation in foundations.values():
        if len(foundation) != 13:
            return False
    return True

def move_between_tableau(source_pile, dest_pile):
    if not source_pile:
        return False
    card_to_move = source_pile[-1]
    if can_place_on_tableau(card_to_move, dest_pile):
        dest_pile.append(source_pile.pop())
        speak(f"Moved {card_to_move} to another pile in tableau.")
        return True
    return False

def draw_from_stock(deck, waste_pile):
    if deck.cards:
        waste_pile.append(deck.draw())
        speak(f"Drew a card from the deck. Top card in waste pile is now {waste_pile[-1]}.")
    else:
        speak("The deck is empty. No more cards to draw.")

def auto_move_to_foundation(tableau, waste_pile, foundations):
    for pile in tableau:
        if pile:
            top_card = pile[-1]
            if check_auto_move_to_foundation(top_card, foundations):
                foundations[top_card.suit].append(pile.pop())
                speak(f"Automatically moved {top_card} to its foundation.")
                return True
    if waste_pile:
        top_card = waste_pile[-1]
        if check_auto_move_to_foundation(top_card, foundations):
            foundations[top_card.suit].append(waste_pile.pop())
            speak(f"Automatically moved {top_card} from waste pile to its foundation.")
            return True
    return False

def main():
    speak("Welcome to Solitaire for the Blind.")
    deck, tableau, waste_pile, foundations = setup_game()

    current_mode = "tableau"
    current_pile = 0

    while True:
        try:
            current_key = keyboard.read_event(suppress=True).name

            if current_key == 'right':
                if current_mode == "tableau" and current_pile < 6:
                    current_pile += 1
                    if tableau[current_pile]:
                        speak(f"Now at pile {current_pile + 1} with top card {tableau[current_pile][-1]}")
                    else:
                        speak(f"Pile {current_pile + 1} is empty.")

            elif current_key == 'left':
                if current_mode == "tableau" and current_pile > 0:
                    current_pile -= 1
                    if tableau[current_pile]:
                        speak(f"Now at pile {current_pile + 1} with top card {tableau[current_pile][-1]}")
                    else:
                        speak(f"Pile {current_pile + 1} is empty.")

            elif current_key == 'down':
                if current_mode == "tableau":
                    current_mode = "waste"
                    if waste_pile:
                        speak(f"Now in waste pile with top card {waste_pile[-1]}")
                    else:
                        speak("Waste pile is empty.")

            elif current_key == 'up':
                if current_mode == "waste":
                    current_mode = "tableau"
                    if tableau[current_pile]:
                        speak(f"Back to tableau at pile {current_pile + 1} with top card {tableau[current_pile][-1]}")
                    else:
                        speak(f"Pile {current_pile + 1} is empty.")

            elif current_key == 'draw':
                draw_from_stock(deck, waste_pile)

            elif current_key == 'move':
                if current_mode == "tableau":
                    for i, pile in enumerate(tableau):
                        if i != current_pile and move_between_tableau(tableau[current_pile], pile):
                            break
                elif current_mode == "waste" and waste_pile:
                    card = waste_pile[-1]
                    for pile in tableau:
                        if can_place_on_tableau(card, pile):
                            pile.append(waste_pile.pop())
                            speak(f"Moved {card} from waste pile to tableau.")
                            break

            elif current_key == 'f':  # Move to foundation directly
                if current_mode == "tableau" and tableau[current_pile]:
                    card = tableau[current_pile][-1]
                    if check_auto_move_to_foundation(card, foundations):
                        foundations[card.suit].append(tableau[current_pile].pop())
                        speak(f"Moved {card} directly to foundation.")
                elif current_mode == "waste" and waste_pile:
                    card = waste_pile[-1]
                    if check_auto_move_to_foundation(card, foundations):
                        foundations[card.suit].append(waste_pile.pop())
                        speak(f"Moved {card} from waste pile directly to foundation.")

            # Additional controls can be added here for more gameplay functionality

            while auto_move_to_foundation(tableau, waste_pile, foundations):
                pass

        except Exception as e:
            speak(f"An error occurred: {str(e)}")

        if check_victory(foundations):
            speak("Congratulations! You've won!")
            break

if __name__ == "__main__":
    main()
