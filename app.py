from flask import Flask, render_template, request, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.secret_key = 'frbfbfbfv'  
boggle_game = Boggle()

@app.route('/')
def home():
    """Display the Boggle board."""
    board = boggle_game.make_board()
    session['board'] = board
    session['score'] = 0  # Initialize score
    return render_template('index.html', board=board)

@app.route('/check', methods=['POST'])
def check_word():
    """Check if the submitted word is valid."""
    guess = request.json.get('guess')
    board = session['board']

    result = boggle_game.check_valid_word(board, guess)

    if result == 'ok':
        session['score'] += len(guess)  # Update score if the word is valid
    return jsonify({"result": result})

@app.route('/score', methods=['POST'])
def save_score():
    """Save the current game score."""
    score = session.get('score', 0)
    total_games = session.get('total_games', 0) + 1
    highest_score = max(score, session.get('highest_score', 0))
    
    session['total_games'] = total_games
    session['highest_score'] = highest_score

    return jsonify({"total_games": total_games, "highest_score": highest_score})

if __name__ == "__main__":
    app.run(debug=True)