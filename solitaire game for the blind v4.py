import pyttsx3
import random
import json

# Initialize the speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

# Speech function to communicate with the player
def speak_message(text):
    """Speak out a message using the text-to-speech engine."""
    engine.say(text)
    engine.runAndWait()

# Card class representing a single card
class Card:
    """A class representing a single card in the deck."""
    FACE_CARDS = {'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 1}
    REVERSE_FACE_CARDS = {11: 'Jack', 12: 'Queen', 13: 'King', 1: 'Ace'}
    VALID_SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    VALID_VALUES = list(range(2, 11)) + list(FACE_CARDS.values())

    def __init__(self, suit, value):
        if suit not in Card.VALID_SUITS or value not in Card.VALID_VALUES:
            raise ValueError("Invalid card suit or value")
        self.suit = suit
        self.value = value if isinstance(value, int) else Card.FACE_CARDS[value]
        self.face_up = False

    def __repr__(self):
        value = Card.REVERSE_FACE_CARDS.get(self.value, self.value)
        return f"{value} of {self.suit}" if self.face_up else "Card face down"

    def flip(self):
        """Flip the card to reveal or hide its face."""
        self.face_up = not self.face_up

    def to_dict(self):
        """Convert card to a dictionary for saving state."""
        return {'suit': self.suit, 'value': self.value, 'face_up': self.face_up}

    @staticmethod
    def from_dict(card_dict):
        """Recreate a Card object from a dictionary."""
        if 'suit' in card_dict and 'value' in card_dict:
            card = Card(card_dict['suit'], card_dict['value'])
            card.face_up = card_dict.get('face_up', False)
            return card
        else:
            raise ValueError("Invalid card dictionary representation")

# Deck class representing a deck of 52 cards
class Deck:
    """A class representing a deck of cards."""
    def __init__(self):
        self.suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']
        self.cards = []
        self.waste = []
        self.reset_deck()

    def reset_deck(self):
        self.cards = [Card(suit, value) for suit in self.suits for value in self.values]
        self.waste.clear()
        random.shuffle(self.cards)

    def draw_card(self):
        if self.cards:
            return self.cards.pop()
        elif self.waste:
            self.reshuffle_waste_into_stock()
            return self.cards.pop() if self.cards else None
        else:
            speak_message("No more cards in the deck or waste.")
            return None

    def reshuffle_waste_into_stock(self):
        if not self.waste:
            speak_message("The waste pile is also empty. No cards to draw.")
            return False

        speak_message("The deck is empty. Reshuffling the waste pile into the stock.")
        self.cards = self.waste[:]
        self.waste.clear()
        for card in self.cards:
            card.flip()
        random.shuffle(self.cards)
        return True

# SolitaireGame class representing the game mechanics
class SolitaireGame:
    """A class representing the Solitaire game."""
    def __init__(self):
        self.deck = Deck()
        self.tableau = [[] for _ in range(7)]
        self.foundation = [[] for _ in range(4)]
        self.stock = self.deck.cards[:]
        self.waste = []
        self.undo_stack = []
        self.redo_stack = []
        self.setup_game()

    def setup_game(self):
        """Initial setup for the game."""
        for i in range(7):
            for j in range(i, 7):
                card = self.stock.pop()
                if j == i:
                    card.face_up = True
                self.tableau[j].append(card)

    def draw_from_stock(self):
        """Draw a card from the stock pile and move it to the waste pile."""
        if self.stock:
            card = self.stock.pop()
            card.face_up = True
            self.waste.append(card)
            speak_message(f"Drew {card} from the stock.")
        else:
            speak_message("No more cards in the stock.")

    def move_from_waste(self, destination):
        if not self.waste:
            speak_message("There are no cards in the waste to move.")
            return False

        card_to_move = self.waste[-1]
        destination_pile = self.get_pile_by_name(destination)
        destination_type = "foundation" if destination.startswith('F') else "tableau"

        if destination_pile and self.is_valid_move(card_to_move, destination_pile, destination_type):
            return self.perform_move(self.waste, destination_pile, card_to_move, destination)
        else:
            speak_message(f"Cannot move {card_to_move} to {destination}. Invalid move.")
            return False

def can_be_moved(self, card):
    # Check if the card can be moved to either the foundation or another tableau pile
    for foundation_pile in self.foundation:
        if self.is_valid_move(card, foundation_pile, "foundation"):
            return True  # Return true at the first instance of a valid move to the foundation

    for tableau_pile in self.tableau:
        if self.is_valid_move(card, tableau_pile, "tableau"):
            return True  # Return true at the first instance of a valid move to another tableau pile

    return False  # Return false if no valid moves are found after checking all piles

    def move_card(self, source, destination):
        # Check if pile names are valid
        if not self.is_pile_name_valid(source) or not self.is_pile_name_valid(destination):
        destination_pile = self.get_pile_by_name(destination)

        if not source_pile or not destination_pile or not source_pile[-1].face_up:
            speak_message("Invalid move.")
            return False

        card_to_move = source_pile[-1]
        if self.is_valid_move(card_to_move, destination_pile, destination):
            self.perform_move(source_pile, destination_pile, card_to_move)
            speak_message(f"Moved {card_to_move} from {source} to {destination}.")
            return True
        else:
            speak_message("Invalid move.")
            return False

        # Retrieve the source and destination piles
        source_pile = self.get_pile_by_name(source)


        # Check if there's a card to move and it's face up
        if not source_pile or len(source_pile) == 0 or not source_pile[-1].face_up:
            speak_message("No card to move or the card is face down.")
            return False

        # Get the card to move
        card_to_move = source_pile[-1]
        destination_type = "foundation" if destination.startswith('F') else "tableau"

    # Perform the move if valid, otherwise report invalid move
        if self.is_valid_move(card_to_move, destination_pile, destination_type):
            self.undo_stack.append(self.save_current_state())  # Save current state for undo functionality
            source_pile.pop()  # Remove the card from the source pile
            destination_pile.append(card_to_move)  # Append the card to the destination pile
            card_to_move.face_up = True  # Ensure the card is face up after moving

            if source_pile:  # Flip the next card in the source pile if there is one
                if not source_pile[-1].face_up:
                    source_pile[-1].face_up = True
                    speak_message(f"Flipped the next card in {source}.")

            speak_message(f"Moved {card_to_move} from {source} to {destination}.")
            return True
        else:
            speak_message("Invalid move.")
            return False

        source_pile = self.get_pile_by_name(source)
        destination_pile = self.get_pile_by_name(destination)

        if not source_pile or not source_pile[-1].face_up:
            speak_message("No card to move or the card is face down.")
            return False

        card_to_move = source_pile[-1]
        destination_type = "foundation" if destination.startswith('F') else "tableau"

        if self.is_valid_move(card_to_move, destination_pile, destination_type):
            self.perform_move(source_pile, destination_pile, card_to_move)
            speak_message(f"Moved {card_to_move} from {source} to {destination}.")
            return True
        else:
            speak_message("Invalid move.")
            return False

    def is_valid_move(self, card, destination_pile, destination_type):
        # This method will validate if the move is possible
        if not card.face_up:
            return False
        if destination_type == "tableau":
            if not destination_pile and card.value == 13:  # King
                return True
            elif destination_pile:
                last_card = destination_pile[-1]
                return (card.value == last_card.value - 1 and
                        (card.suit in ['Hearts', 'Diamonds']) != (last_card.suit in ['Hearts', 'Diamonds']))
        elif destination_type == "foundation":
            if not destination_pile and card.value == 1:  # Ace
                return True
            elif destination_pile:
                last_card = destination_pile[-1]
                return (card.suit == last_card.suit and
                        card.value == last_card.value + 1)
        return False

    source_card = source_pile[-1]

    def flip_tableau_cards(self):
        for pile in self.tableau:
            if pile and not pile[-1].face_up:
                pile[-1].face_up = True
                speak_message(f"Flipped top card of Tableau pile: {pile[-1]}")

    def provide_detailed_instructions(self):
        # Expanded instructions with more details
        instructions = (
            "Welcome to Solitaire for the Blind, also known as Klondike. "
            "The game is played with a standard deck of 52 cards. "
            "There are four foundation piles, one for each suit, and they must be built up from Ace to King. "
            "The goal is to move all the cards to the foundation piles, "
            "which must be built up by suit from Ace to King.\n\n"
            "The tableau consists of seven columns, where cards are built down in alternating colors. "
            "Each pile begins with one card face up and the rest face down. "
            "Cards can be moved between tableau piles in descending order and alternating colors. "
            "Only Kings or sequences starting with a King can be moved to empty tableau spaces.\n\n"
            "The stock pile allows you to draw cards, moving them to the waste pile. "
            "Only the top card of the waste pile can be played to the tableau or foundations.\n\n"
            "Commands are as follows:\n"
            "Use 'MOVE <source> <destination>' to move cards between tableau and foundation: Move a card from one pile to another. For example, 'MOVE T1 F1' moves a card from Tableau 1 to Foundation 1.\n "
            "'DRAW': Draw a card from the stock to the waste.\n"
            "To Use the 'MOVE' command to move cards. For example, 'MOVE T1 T2' moves the top card from tableau 1 to tableau 2. "
            "Draw cards from the stock when needed. "
            "If a tableau column is empty, only a King or a sequence starting with a King can be placed there. "
            "You can also move the top card from the waste to either tableau or foundation with 'MOVE_FROM_WASTE <destination>'. "
            "'SAVE' to save the game, 'LOAD' to load a saved game, and 'UNDO'/'REDO' to reverse actions. "
            "To undo or redo a move, use 'UNDO' or 'REDO'. "
            "'STATUS': Get a brief status of the current game, including the count of cards in each pile.\n"
            "'VIEW <pile>': View the contents of a specific pile, such as 'VIEW T1' for Tableau 1.\n"
            "'QUIT': Exit the game.\n\n"
            "To perform a move, type the command followed by the source and the destination. "
            "For example, to move a card from the waste to Foundation 1, type 'MOVE_FROM_WASTE F1'.\n\n"
            "'HELP': Hear this message again.\n"
            "Use 'HELP' for command assistance. Play wisely and good luck!"
            "Good luck and have fun!"
        )
        speak_message(instructions)

def provide_help(self):
    help_message = (
        "Commands you can use:\n"
        "MOVE <source> <destination>: To move a card from one pile to another.\n"
        "DRAW: To draw a card from the stock.\n"
        "MOVE_FROM_WASTE <destination>: To move the top card from the waste.\n"
        "SAVE: To save the current game state.\n"
        "LOAD: To load a previously saved game.\n"
        "UNDO: To undo the last move.\n"
        "REDO: To redo an undone move.\n"
        "STATUS: To get a brief status of the game.\n"
        "VIEW <pile>: To view the contents of a pile.\n"
        "QUIT: To exit the game.\n"
        "HELP: To hear this message again."
    )
    speak_message(help_message)

    def parse_input(self, user_input):
        # This method should handle a single round of input from the user
        parts = user_input.strip().upper().split()
        if not parts:
            speak_message("Invalid command format. Please try again.")
            return False

        command = parts[0]
        if command == "MOVE" and len(parts) == 3:
            self.move_card(parts[1], parts[2])
        elif command == "DRAW":
            self.draw_from_stock()
        elif command == "MOVE_FROM_WASTE" and len(parts) == 2:
            self.move_from_waste(parts[1])
        elif command == "SAVE":
            self.save_game()
        elif command == "LOAD":
            self.load_game()
        elif command == "UNDO":
            self.undo_move()
        elif command == "REDO":
            self.redo_move()
        elif command == "HELP":
            self.provide_help()
        elif command == "INSTRUCTIONS":
            self.provide_detailed_instructions()
        elif command == "QUIT":
            speak_message("Exiting the game. Goodbye!")
            exit(0)
        elif command == "STATUS":
            self.speak_game_status()
        elif command == "VIEW" and len(parts) == 2:
            self.speak_pile_contents(parts[1])
        else:
            speak_message("Unknown or invalid command.")
            return False

        return True




        self.undo_stack.append(self.save_current_state())  # Saving the state for undo functionality
        source_pile.pop()  # Remove the card from the source pile
        destination_pile.append(card_to_move)  # Add the card to the destination pile
        card_to_move.face_up = True  # Ensuring the card is face up after the move

        # Flip the next card
    def move_card(self, source, destination):
    # Validate pile names
        if not self.is_pile_name_valid(source) or not self.is_pile_name_valid(destination):
            speak_message("Invalid pile names. Please try again.")
            return False

    # Get the piles by their names
        source_pile = self.get_pile_by_name(source)
        destination_pile = self.get_pile_by_name(destination)

    # Ensure there is a card to move and it's face up
        if not source_pile or not source_pile[-1].face_up:
            speak_message("No card to move or the card is face down.")
            return False

        card_to_move = source_pile[-1]
        destination_type = "foundation" if destination.startswith('F') else "tableau"

# Perform the move if valid, otherwise report invalid move
        if self.is_valid_move(card_to_move, destination_pile, destination_type):
            self.perform_move(source_pile, destination_pile, card_to_move)
            speak_message(f"Moved {card_to_move} from {source} to {destination}.")
            return True
        else:
            speak_message("Invalid move.")
            return False

    def is_pile_name_valid(self, pile_name):
        # Checks if the pile name is valid (e.g., "T1" for Tableau 1, "F1" for Foundation 1, "S" for Stock, "W" for Waste)
        valid_tableaus = [f"T{i+1}" for i in range(len(self.tableau))]
        valid_foundations = [f"F{i+1}" for i in range(len(self.foundation))]
        return pile_name in valid_tableaus + valid_foundations + ['S', 'W']

    def get_pile_by_name(self, name):
        # Returns the correct pile based on the name, raises ValueError if the pile name is unknown
        if name.startswith('T'):
            return self.tableau[int(name[1:]) - 1]
        elif name.startswith('F'):
            return self.foundation[int(name[1:]) - 1]
        elif name == 'S':
            return self.stock
        elif name == 'W':
            return self.waste
        else:
            raise ValueError(f"Unknown pile name: {name}")

    def is_valid_move(self, source_pile, destination_pile, destination_type):
        if not source_pile:
            return False
        source_card = source_pile[-1]

        if destination_type == "tableau":
            if not destination_pile and source_card.value == 13:  # King
                return True
            elif destination_pile:
                destination_card = destination_pile[-1]
                is_alternate_color = (source_card.suit in ['Hearts', 'Diamonds']) != (destination_card.suit in ['Hearts', 'Diamonds'])
                is_one_less = source_card.value == destination_card.value - 1
                return is_alternate_color and is_one_less

        elif destination_type == "foundation":
            if not destination_pile:
                return source_card.value == 1  # Ace
            else:
                top_card = destination_pile[-1]
                is_same_suit = source_card.suit == top_card.suit
                is_one_more = source_card.value == top_card.value + 1
                return is_same_suit and is_one_more

        return False  # If none of the conditions are met, the move is not valid

    def perform_move(self, source_pile, destination_pile, card_to_move, destination):
        # This method will perform the actual move if it's valid
        destination_type = destination[0].lower()
        if self.is_valid_move(card_to_move, destination_pile, destination_type):
            source_pile.remove(card_to_move)
            destination_pile.append(card_to_move)
            card_to_move.face_up = True
            speak_message(f"Moved {card_to_move} to {destination}.")
            if source_pile and not source_pile[-1].face_up:
                source_pile[-1].face_up = True
            return True
        else:
            speak_message(f"Cannot move {card_to_move} to {destination}. Move is not valid.")
            return False

        source_pile.remove(card_to_move)
        destination_pile.append(card_to_move)
        card_to_move.face_up = True

        if source_pile and not source_pile[-1].face_up:
            source_pile[-1].face_up = True

    def move_card(self, source, destination):
        # Correct indentation for the whole block
        source_pile = self.get_pile_by_name(source)
        destination_pile = self.get_pile_by_name(destination)
        if not source_pile or not source_pile[-1].face_up:
            speak_message("Cannot move from an empty pile or move a face-down card.")
            return False

        card_to_move = source_pile[-1]
        destination_type = "foundation" if destination.startswith('F') else "tableau"
        if self.is_valid_move(card_to_move, destination_pile, destination_type):
            self.undo_stack.append(self.save_current_state())
            self.redo_stack.clear()
            source_pile.pop()
            destination_pile.append(card_to_move)
            if source.startswith('T') and source_pile and not source_pile[-1].face_up:
                source_pile[-1].face_up = True
        # Flip the next card in the source pile if there's any and it's face down
            if source_pile and not source_pile[-1].face_up:
                source_pile[-1].face_up = True
            card_to_move.face_up = True
            speak_message(f"Moved {card_to_move} from {source} to {destination}.")
            return True
        else:
            speak_message("Invalid move.")
            return False

def undo_move(self):
    if self.undo_stack:
        last_state = self.undo_stack.pop()
        self.redo_stack.append(self.save_current_state())
        self.restore_state(last_state)
        speak_message("Move undone.")
    else:
        speak_message("No moves to undo.")

def redo_move(self):
    if self.redo_stack:
        state_to_redo = self.redo_stack.pop()
        self.undo_stack.append(self.save_current_state())
        self.restore_state(state_to_redo)
        speak_message("Move redone.")
    else:
        speak_message("No moves to redo.")

        self.undo_stack.append(self.save_current_state())
        self.restore_state(state_to_redo)
        speak_message("Move redone.")

        if self.redo_stack:
            state_to_redo = self.redo_stack.pop()
            self.undo_stack.append(self.save_current_state())
            self.restore_state(state_to_redo)
            speak_message("Move redone.")
        else:
            speak_message("No moves to redo.")

def handle_empty_stock_and_waste(self):
    if not self.stock and not self.waste:
        speak_message("Both stock and waste are empty. Check for possible moves in tableau and foundation.")

    def handle_user_input(self, input_str):
        parts = input_str.strip().upper().split()
        if not parts:
            speak_message("Invalid command format. Please try again.")
            return

        command = parts[0]
        if command == "MOVE" and len(parts) == 3:
            self.move_card(parts[1], parts[2])
        elif command == "DRAW":
            self.draw_from_stock()
    elif command == "MOVE_FROM_WASTE" and len(parts) == 2:
        self.move_from_waste(parts[1])
    elif command == "SAVE":
        self.save_game()
    elif command == "LOAD":
        self.load_game()
    elif command == "UNDO":
        self.undo_move()
    elif command == "REDO":
        self.redo_move()
    elif command == "HELP":
        self.provide_help()
    elif command == "INSTRUCTIONS":
        self.provide_detailed_instructions()
    elif command == "QUIT":
        speak_message("Exiting the game. Goodbye!")
        exit(0)
    elif command == "STATUS":
            self.speak_game_status()
        elif command == "VIEW" and len(parts) == 2:
            self.speak_pile_contents(parts[1])
        else:
            speak_message("Unknown or invalid command.")

        if len(parts) >= 1:
            command = parts[0]
            if command == "MOVE" and len(parts) == 3:
                self.move_card(parts[1], parts[2])
            elif command == "DRAW":
                self.draw_from_stock()
            elif command == "MOVE_FROM_WASTE" and len(parts) == 2:
                self.move_from_waste(parts[1])
            elif command == "SAVE":
                self.save_game()
            elif command == "LOAD":
                self.load_game()
            elif command == "UNDO":
                self.undo_move()
            elif command == "REDO":
                self.redo_move()
            else:
                speak_message("Unknown command")
        else:
            speak_message("Invalid command format")

def auto_move_to_foundation(self):
    for tableau_pile in self.tableau:
        if tableau_pile and tableau_pile[-1].face_up:
            card_to_move = tableau_pile[-1]
            for foundation_pile in self.foundation:
                if self.is_valid_move(card_to_move, foundation_pile, "foundation"):
                    self.perform_move(tableau_pile, foundation_pile, card_to_move)
                    speak_message(f"Auto-moved {card_to_move} to foundation.")
                    return True
    return False
    moved = False
    for pile in self.tableau:
        if pile and self.is_valid_move(pile[-1], None, "foundation"):
    for i, pile in enumerate(self.tableau):
        if pile and pile[-1].face_up:
            for j, foundation_pile in enumerate(self.foundation):
                if self.is_valid_move(pile[-1], foundation_pile, "foundation"):
                    self.perform_move(pile, foundation_pile, pile[-1], f"Foundation {j+1}")
                    speak_message(f"Auto-moved {pile[-1]} from Tableau {i+1} to Foundation {j+1}")
                    moved = True
                    break
        if moved:
            break
                    return  # Return after one move to avoid multiple auto-moves at once

    def restart_game(self):
        """Restart the game with initial setup."""
        speak_message("Restarting the game.")
        self.setup_game()
        speak_message("Game restarted.")
    self.waste.clear()
    self.undo_stack.clear()
    self.redo_stack.clear()

    def is_pile_complete(self, pile):
        if len(pile) != 13:
            return False
        expected_order = list(range(1, 14))  # Ace (1) to King (13)
        return all(card.value == expected_value for card, expected_value in zip(pile, expected_order))

    def end_game_summary(self):
        total_moves = len(self.undo_stack)
        speak_message(f"Game over. Total moves made: {total_moves}")

    def handle_user_input(self, input_str):
        parts = input_str.split()

        # Check if there's any input at all
        if len(parts) == 0:
            speak_message("Invalid command format.")
            return

        # Extract the command and convert to uppercase
        command = parts[0].upper()

        # Process the command
        if command == "MOVE" and len(parts) == 3:
            self.move_card(parts[1], parts[2])
        elif command == "DRAW":
            self.draw_from_stock()
        elif command == "MOVE_FROM_WASTE" and len(parts) == 2:
            self.move_from_waste(parts[1])
        elif command == "SAVE":
            self.save_game()
        elif command == "LOAD":
            self.load_game()
        elif command == "UNDO":
            self.undo_move()
        elif command == "REDO":
            self.redo_move()
        elif command == "QUIT":
            speak_message("Exiting the game. Goodbye!")
            exit(0)
        elif command == "STATUS":

    def provide_hint(self):
        hints = self.hint_from_tableau_to_foundation()
        hints.extend(self.hint_from_waste())
        hints.extend(self.hint_within_tableau())
        hints.extend(self.provide_complex_hint())

        if hints:
            for hint in hints:
                speak_message(hint)
        else:
            speak_message("No hints available at the moment.")

    def hint_from_tableau_to_foundation(self):
        hints = []
        for i, tableau_pile in enumerate(self.tableau):
            if tableau_pile and tableau_pile[-1].face_up:
                card = tableau_pile[-1]
                for j, foundation_pile in enumerate(self.foundation):
                    if self.is_valid_move(card, foundation_pile, "foundation"):
                        hints.append(f"Try moving {card} from Tableau {i+1} to Foundation {j+1}.")
        return hints

    def hint_from_waste(self):
        hints = []
        if self.waste:
            card_to_move = self.waste[-1]
            for i, foundation_pile in enumerate(self.foundation):
                if self.is_valid_move(card_to_move, foundation_pile, "foundation"):
                    hints.append(f"Try moving {card_to_move} from Waste to Foundation {i+1}.")
            for i, tableau_pile in enumerate(self.tableau):
                if self.is_valid_move(card_to_move, tableau_pile, "tableau"):
                    hints.append(f"Try moving {card_to_move} from Waste to Tableau {i+1}.")
        return hints

    def hint_within_tableau(self):
        hints = []
        for i, source_pile in enumerate(self.tableau):
            if source_pile and source_pile[-1].face_up:
                for j, dest_pile in enumerate(self.tableau):
                    if i != j and self.is_valid_move(source_pile[-1], dest_pile, "tableau"):
                        hints.append(f"Try moving {source_pile[-1]} from Tableau {i+1} to Tableau {j+1}.")
        return hints

    def provide_complex_hint(self):
        hints = []
        # Checking for moves that free up a face-down card
        for i, pile in enumerate(self.tableau):
            for j in range(len(pile) - 1, -1, -1):
                card = pile[j]
                if not card.face_up:
                    if j > 0 and pile[j - 1].face_up:
                        hints.append(f"Consider moving cards above {pile[j - 1]} in Tableau {i+1} to free a face-down card.")
                    break  # Break if we've found a face-down card

        # Suggesting moves that build up a tableau pile
        for i, pile in enumerate(self.tableau):
            if pile and pile[-1].face_up:
                for j, search_pile in enumerate(self.tableau):
                    if search_pile and search_pile[-1].face_up and i != j:
                        if (pile[-1].value == search_pile[-1].value - 1) and \
                           ((pile[-1].suit in ['Hearts', 'Diamonds']) != (search_pile[-1].suit in ['Hearts', 'Diamonds'])):
                            hints.append(f"Consider moving {search_pile[-1]} from Tableau {j+1} to Tableau {i+1} to build up the sequence.")
        return hints

def save_current_state(self):
    """
    Capture the current game state, including the tableau, foundation, stock, and waste.
    :return: A dictionary representing the current game state.
    """
    state = {
        'tableau': [[card.to_dict() for card in pile] for pile in self.tableau],
        'foundation': [[card.to_dict() for card in pile] for pile in self.foundation],
        'stock': [card.to_dict() for card in self.stock],
        'waste': [card.to_dict() for card in self.waste]
        # Add additional state components as necessary
    }
    return state

def restore_state(self, state):
    """
    Restore the game state from the provided dictionary.
    :param state: A dictionary representing the game state to restore.
    """
    try:
        self.tableau = [[Card.from_dict(card_dict) for card_dict in pile] for pile in state['tableau']]
        self.foundation = [[Card.from_dict(card_dict) for card_dict in pile] for pile in state['foundation']]
        self.stock = [Card.from_dict(card_dict) for card_dict in state['stock']]
        self.waste = [Card.from_dict(card_dict) for card_dict in state['waste']]
        # Restore additional state components as necessary
        speak_message("Game state restored successfully.")
    except Exception as e:
        speak_message(f"Failed to restore game state: {e}")

def save_game(self, filename="solitaire_save.json"):
    """
    Save the current game state to a file.
    """
    try:
        state = self.save_current_state()
        with open(filename, 'w') as file:
            json.dump(state, file)
        speak_message("Game state saved successfully.")
    except Exception as e:
        speak_message(f"An error occurred while saving the game: {e}")

def load_game(self, filename="solitaire_save.json"):
    """
    Load the game state from a file.
    """
    try:
        with open(filename, 'r') as file:
            game_state = json.load(file)
        self.restore_state(game_state)
        speak_message("Game loaded successfully.")
    except FileNotFoundError:
        speak_message("No saved game found.")
    except json.JSONDecodeError:
        speak_message("Error decoding the game data. The save file might be corrupted.")
    except Exception as e:
        speak_message(f"An error occurred while loading the game: {e}")










    def set_difficulty(self, level):
        self.difficulty_settings = {
            'easy': {'turn_over': 1, 'stock_pass_limit': float('inf'), 'speech_rate': 120},
            'medium': {'turn_over': 3, 'stock_pass_limit': 3, 'speech_rate': 150},
            'hard': {'turn_over': 3, 'stock_pass_limit': 1, 'speech_rate': 180}
        }

        level = level.lower()
        if level in self.difficulty_settings:
            settings = self.difficulty_settings[level]
            self.turn_over = settings['turn_over']  # Number of cards to turn over from the stock
            self.stock_pass_limit = settings['stock_pass_limit']  # Max number of passes through the stock
            engine.setProperty('rate', settings['speech_rate'])  # Speech rate for difficulty
            speak_message(f"Difficulty set to {level}.")
        else:
            speak_message("Invalid difficulty level. Please choose 'easy', 'medium', or 'hard'.")

def speak_game_status(self):
        if brief:
            # Short summary of the game status
    stock_count = len(self.stock)
    waste_count = len(self.waste)
    tableau_info = ", ".join(f"Tableau {i+1}: {len(pile)} cards" for i, pile in enumerate(self.tableau))
    foundation_info = ", ".join(f"Foundation {i+1}: {len(pile)} cards" for i, pile in enumerate(self.foundation))
    status_message = f"Stock: {stock_count} cards, Waste: {waste_count} cards, {tableau_info}, {foundation_info}"
    speak_message(status_message)

            status_message += ", ".join([f"Foundation {i+1}: {count}" for i, count in enumerate(foundation_counts)])
        speak_message(status_message)
        else:
            self.speak_game_state()

def speak_pile_contents(self, pile_name):
    pile = self.get_pile_by_name(pile_name)
    if pile:
        pile_description = ', '.join(str(card) for card in pile)
        speak_message(f"{pile_name}: {pile_description if pile else 'empty'}")
    else:
        speak_message(f"Unknown pile name: {pile_name}")

    def save_current_state(self):
        # This method will save the current game state
        state = {
            'tableau': [[card.to_dict() for card in pile] for pile in self.tableau],
            'foundation': [[card.to_dict() for card in pile] for pile in self.foundation],
            'stock': [card.to_dict() for card in self.stock],
            'waste': [card.to_dict() for card in self.waste],
            'undo_stack': self.undo_stack,
            'redo_stack': self.redo_stack
        }
        return state

    def restore_state(self, state):
        # This method will restore the game state from a saved state
        self.tableau = [[Card.from_dict(card_dict) for card_dict in pile_dict] for pile_dict in state['tableau']]
        self.foundation = [[Card.from_dict(card_dict) for card_dict in pile_dict] for pile_dict in state['foundation']]
        self.stock = [Card.from_dict(card_dict) for card_dict in state['stock']]
        self.waste = [Card.from_dict(card_dict) for card_dict in state['waste']]
        self.undo_stack = state['undo_stack']
        self.redo_stack = state['redo_stack']

    def speak_game_state(self):
        for i, pile in enumerate(self.tableau):
            pile_description = ', '.join(str(card) for card in pile)
            speak_message(f"Tableau pile {i + 1}: {pile_description if pile else 'empty'}")
        waste_description = ', '.join(str(card) for card in self.waste)
        speak_message(f"Waste: {waste_description if self.waste else 'empty'}")
        for i, pile in enumerate(self.foundation):
            pile_description = ', '.join(str(card) for card in pile)
            speak_message(f"Foundation pile {i + 1}: {pile_description if pile else 'empty'}")

    def get_pile_by_name(self, name):
        if name.startswith('T'):
            return self.tableau[int(name[1:]) - 1]
        elif name.startswith('F'):
            return self.foundation[int(name[1:]) - 1]
        elif name == 'S':
            return self.stock
        elif name == 'W':
            return self.waste
        else:
            raise ValueError(f"Unknown pile name: {name}")

def check_game_over(self):
    # Check if there are moves from stock or waste
    if self.stock or self.waste:
        return False
    for tableau_pile in self.tableau:
        if tableau_pile and any(self.is_valid_move(card, other_pile, "tableau") for card in tableau_pile for other_pile in self.tableau if other_pile is not tableau_pile):
            return False
    return True
                if any(self.is_valid_move(tableau_pile[-1], other_pile, "tableau") for other_pile in self.tableau if other_pile is not tableau_pile):
                    return False
        return True

            for foundation_pile in self.foundation:
                if self.is_valid_move(tableau_pile[-1], foundation_pile, "foundation"):
                    return False
            for other_pile in self.tableau:
                if other_pile != tableau_pile and self.is_valid_move(tableau_pile[-1], other_pile, "tableau"):
                    return False
    # If no moves are possible, the game is over
    return True

        if not self.stock and not self.waste and all(not pile[-1].face_up for pile in self.tableau):
            return True

def check_for_win(self):
    return all(len(pile) == 13 for pile in self.foundation)

    def ask_to_play_again(self):
        speak_message("Would you like to play again? Enter 'yes' or 'no':")
        response = input().lower()
        if response == 'yes':
            self.restart_game()
            self.setup_game()
            return True
        else:
            speak_message("Thank you for playing. Goodbye!")
            exit(0)

    def play(self):
        # The main game loop
        try:
            self.setup_game()
            while not self.check_game_over():
                user_input = input("Your move (or type 'HELP' for options): ")
                self.handle_user_input(user_input)
            self.speak_game_state()  # Initial state of the game
            while True:
                user_input = input("Your move (or type 'HELP' for options): ")
                self.parse_input(user_input)
            if self.check_for_win():
                speak_message("Congratulations! You have won the game!")
            else:
                speak_message("Game over. There are no more moves available.")
        except Exception as e:
            speak_message(f"An error occurred: {e}")

        """Start the game loop."""
        while not self.check_game_over():
            user_input = input("Your move (or type 'HELP' for options): ")
            self.handle_user_input(user_input)

            if self.check_for_win():
                speak_message("Congratulations! You have won the game!")
            else:
                speak_message("Game over. There are no more moves available.")
        except Exception as e:
            speak_message(f"An error occurred: {e}")

                if self.check_game_over():
                    self.end_game_summary()
                    if not self.ask_to_play_again():
                        break
                elif self.check_for_win():
                    speak_message("Congratulations! You have won the game.")
                    if not self.ask_to_play_again():
                        break
        except Exception as e:
            speak_message(f"An error occurred: {str(e)}")

def main():
    """Main function to run the Solitaire game."""
    game = SolitaireGame()
    game.play()
# Ensure the main guard is at the top level of indentation
if __name__ == "__main__":
    game = SolitaireGame()
    game.play()
    main()
