import chess
import chess.engine
import pyttsx3

# Initialize the Speech Engine
engine = pyttsx3.init()

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def describe_board(board):
    description = ""
    for rank in reversed(range(8)):  # chess ranks are 1-8, python-chess ranks are 0-7
        for file in range(8):  # chess files are a-h, python-chess files are 0-7
            square = chess.square(file, rank)
            piece = board.piece_at(square)
            if piece is not None:
                description += f"{piece.symbol()} at {chess.square_name(square)}, "
    return description[:-2]  # remove last comma and space

def get_computer_move(board):
    # use python-chess's simple engine to select a move
    with chess.engine.SimpleEngine.popen_uci("/path/to/your/engine") as engine:
        result = engine.play(board, chess.engine.Limit(time=2.0))  # adjust time as necessary
        return result.move

def main():
    board = chess.Board()

    while not board.is_game_over():
        print(board)
        speak_text("It's your turn.")
        speak_text(describe_board(board))

        move = None
        while move not in board.legal_moves:
            raw_move = input("Enter your move in algebraic notation: ")
            try:
                move = chess.Move.from_uci(raw_move)
                if move not in board.legal_moves:
                    raise ValueError
            except:
                print("Invalid move!")
                speak_text("Invalid move!")
                move = None  # reset move so the while loop continues

        board.push(move)
        speak_text("You moved " + raw_move)

        if board.is_check():
            speak_text("Check!")

        if not board.is_game_over():
            computer_move = get_computer_move(board)
            board.push(computer_move)
            speak_text("Computer moved " + computer_move.uci())

    if board.is_checkmate():
        print("Checkmate!")
        speak_text("Checkmate!")
    elif board.is_stalemate():
        print("Stalemate!")
        speak_text("Stalemate!")
    elif board.is_insufficient_material():
        print("Draw due to insufficient material.")
        speak_text("Draw due to insufficient material.")
    else:  # game could also end in a draw for several reasons
        print("The game is a draw.")
        speak_text("The game is a draw.")

if __name__ == "__main__":
    main()
