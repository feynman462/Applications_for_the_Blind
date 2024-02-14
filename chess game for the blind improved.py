import chess
import chess.engine
import pyttsx3
import keyboard  # Ensure this package is installed

# Initialize the Speech Engine
engine = pyttsx3.init()

def speak_text(text):
    try:
        engine.endLoop()  # Try to end any existing speech loop
    except:
        pass  # Ignore if there's no loop running
    engine.say(text)
    engine.runAndWait()

def describe_board(board):
    description = ""
    for rank in reversed(range(8)):
        for file in range(8):
            square = chess.square(file, rank)
            piece = board.piece_at(square)
            if piece:
                piece_name = piece.symbol().upper() if piece.color == chess.WHITE else piece.symbol()
                description += f"{piece_name} on {chess.square_name(square)}, "
    return description[:-2]  # Remove the last comma and space

def help_to_play():
    help_message = (
        "To move a piece, enter the starting and ending squares in algebraic notation. "
        "For example, to move a piece from a2 to a4, type 'a2a4'. "
        "For pawn promotion, add the letter of the new piece at the end, like 'e7e8q' for a queen. "
        "To castle kingside, use 'e1g1' for White or 'e8g8' for Black. "
        "To castle queenside, use 'e1c1' for White or 'e8c8' for Black. "
        "Type 'help' during your turn for this message."
    )
    speak_text(help_message)
    print(help_message)

def describe_move(move):
    return f"Move from {chess.square_name(move.from_square)} to {chess.square_name(move.to_square)}"

def main():
    speak_text("Welcome to Chess for the Blind.")
    print("Welcome to Chess for the Blind.")

    engine_path = r"C:\Users\user\Documents\CHAT GBT FILES\chess for the blind folder\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"
    board = chess.Board()

    keyboard.add_hotkey('ctrl+h', help_to_play)

    while not board.is_game_over():
        print(board)
        speak_text("It's your turn.")
        speak_text(describe_board(board))

        move = None
        while move not in board.legal_moves:
            raw_move = input("Enter your move in algebraic notation or type 'help' for assistance: ")
            if raw_move.lower() == 'help':
                help_to_play()
                continue
            if len(raw_move) not in [4, 5]:
                print("Invalid move!")
                speak_text("Invalid move!")
                continue
            try:
                move = chess.Move.from_uci(raw_move)
                if move not in board.legal_moves:
                    raise ValueError
            except:
                print("Invalid move!")
                speak_text("Invalid move!")
                move = None

        if move:
            board.push(move)
            speak_text("You moved " + describe_move(move))

        if board.is_check():
            speak_text("Check!")

        if not board.is_game_over():
            with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
                result = engine.play(board, chess.engine.Limit(time=2.0))
                computer_move = result.move
                board.push(computer_move)
                speak_text("Computer moved " + describe_move(computer_move))

        if board.is_checkmate():
            print("Checkmate!")
            speak_text("Checkmate!")
        elif board.is_stalemate():
            print("Stalemate!")
            speak_text("Stalemate!")
        elif board.is_insufficient_material():
            print("Draw due to insufficient material.")
            speak_text("Draw due to insufficient material.")
        else:
            print("The game is a draw.")
            speak_text("The game is a draw.")

    keyboard.remove_hotkey('ctrl+h')

if __name__ == "__main__":
    main()
