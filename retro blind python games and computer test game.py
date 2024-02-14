import tkinter as tk
import pyttsx3
import random

class RetroTriviaGame:
    def __init__(self, master):
        self.master = master
        self.master.title('Retro Game Collection')
        self.engine = pyttsx3.init()
        self.question_label = tk.Label(master, text="Game information will appear here.")
        self.question_label.pack()
        self.entry = tk.Entry(master)
        self.entry.pack()

        self.score = 0  # New variable for the score
        self.score_label = tk.Label(master, text=f"Score: {self.score}")
        self.score_label.pack()

        self.questions_answers = [("What is the capital of France?", "Paris"),
                                  ("What is the capital of Italy?", "Rome"),
                                  ("What is the capital of Germany?", "Berlin")]

        self.programming_questions_answers = [("Which programming language is most popular for web development?", "javascript"),
                                              ("What language is commonly used for scientific computing and data analysis?", "python"),
                                              ("Which language is known for its use in system programming?", "c")]

        self.current_question = 0
        self.target_number = random.randint(1, 100)
        self.game_state = 0  # 0: Trivia, 1: Number Guessing, 2: Adventure, 3: Programming Quiz

        # New for adventure game
        self.adventure_game_state = {"room": 0, "has_key": False, "chest_open": False}
        self.adventure_rooms = ["You're in a room with a key on the floor.", 
                                "You're in a room with a closed treasure chest."]

        # Bindings
        self.entry.bind("<Return>", self.check_answer)
        self.master.bind("<Right>", self.next_question)
        self.master.bind("<Left>", self.prev_question)
        self.master.bind("<Up>", self.switch_game)
        self.master.bind("<Down>", self.switch_game)

        self.ask_question()

    def say_text(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def ask_question(self):
        if self.game_state == 0:
            try:
                self.question, self.answer = self.questions_answers[self.current_question]
            except IndexError:
                self.say_text("Error, no more questions available.")
                return
            self.question_label.config(text=self.question)
            self.say_text(self.question)
        elif self.game_state == 1:
            self.question_label.config(text="Guess the number between 1 and 100.")
            self.say_text("Guess the number between 1 and 100.")
        elif self.game_state == 2:  # Adventure game
            self.question_label.config(text=self.adventure_rooms[self.adventure_game_state["room"]])
            self.say_text(self.adventure_rooms[self.adventure_game_state["room"]])
        else:  # New for programming quiz
            try:
                self.question, self.answer = self.programming_questions_answers[self.current_question]
            except IndexError:
                self.say_text("Error, no more questions available.")
                return
            self.question_label.config(text=self.question)
            self.say_text(self.question)
        self.entry.focus_set()  # Set focus to the text entry box

    def check_answer(self, event):
        user_answer = self.entry.get().lower()
        if self.game_state in [0, 3]:  # Trivia or programming quiz
            if user_answer == self.answer.lower():
                self.say_text("Correct!")
                self.score += 1  # Increase the score
                self.score_label.config(text=f"Score: {self.score}")  # Update the score label
                self.entry.delete(0, 'end')
                self.next_question(None)
            else:
                self.say_text("Incorrect. Try again.")
        elif self.game_state == 1:  # Number guessing game
            # Same as before
            # ...
        else:  # Adventure game
            # Same as before
            # ...
        self.entry.delete(0, 'end')
        self.ask_question()

    def next_question(self, event):
        if self.game_state in [0, 3]:  # Trivia or programming quiz
            self.current_question += 1
            self.ask_question()

    def prev_question(self, event):
        if self.game_state in [0, 3]:  # Trivia or programming quiz
            if self.current_question > 0:
                self.current_question -= 1
                self.ask_question()

    def switch_game(self, event):
        self.game_state = (self.game_state + 1) % 4  # Now 4 games
        if self.game_state == 0:
            self.say_text("Switched to the trivia game.")
        elif self.game_state == 1:
            self.say_text("Switched to the number guessing game.")
        elif self.game_state == 2:  # Adventure game
            self.say_text("Switched to the adventure game.")
        else:  # Programming quiz
            self.say_text("Switched to the programming quiz.")
        self.ask_question()

root = tk.Tk()
game = RetroTriviaGame(root)
root.mainloop()
