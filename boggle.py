"""Utilities related to Boggle game."""

from random import choice
import string

class Boggle:
    def __init__(self):
        self.words = self.read_dict("words.txt")  # Load the dictionary

    def read_dict(self, dict_path):
        """Read and return all words in the dictionary as a set."""
        try:
            with open(dict_path) as dict_file:
                return {w.strip().upper() for w in dict_file if w.strip()}  # Use a set for faster lookups
        except FileNotFoundError:
            print(f"Error: The file {dict_path} was not found.")
            return set()  # Return an empty set if the file is not found

    def make_board(self):
        """Make and return a random Boggle board."""
        board = [[choice(string.ascii_uppercase) for _ in range(5)] for _ in range(5)]
        print("Generated board:", board)  # Debugging line
        return board

    def check_valid_word(self, board, word):
        """Check if a word is valid in the dictionary and/or the Boggle board."""
        word_upper = word.upper()  # Convert word to uppercase for consistency
        print(f"Checking word: {word_upper}")  # Debugging line
        word_exists = word_upper in self.words
        print(f"Word exists in dictionary: {word_exists}")  # Debugging line
        valid_word = self.find(board, word_upper)

        if word_exists and valid_word:
            return "ok"
        elif word_exists:
            return "not-on-board"
        else:
            return "not-a-word"

    def find_from(self, board, word, y, x, seen):
        """Check if we can find a word on the board, starting at coordinates (y, x)."""
        # Out of bounds
        if not (0 <= x < 5 and 0 <= y < 5):
            return False
        
        # Letter does not match
        if board[y][x] != word[0]:
            return False
        
        # Letter already used in this path
        if (y, x) in seen:
            return False
        
        # We've found the last letter of the word
        if len(word) == 1:
            return True

        # Mark this letter as seen and continue searching
        seen.add((y, x))

        # Explore neighbors (including diagonals)
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy == 0 and dx == 0:  # Skip the current letter
                    continue
                if self.find_from(board, word[1:], y + dy, x + dx, seen):
                    return True

        # Unmark this letter as seen (backtracking)
        seen.remove((y, x))
        return False

    def find(self, board, word):
        """Check if the word can be found in the board."""
        for y in range(5):
            for x in range(5):
                if self.find_from(board, word, y, x, seen=set()):
                    return True
        return False