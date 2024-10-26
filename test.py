from unittest import TestCase
from app import app
from flask import session

class FlaskTests(TestCase):

    def setUp(self):
        """Setup for tests; creates test client."""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_home_page(self):
        """Test the home page to ensure it displays the board."""
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Boggle Game', response.data)  # Check for the title

    def test_check_valid_word(self):
        """Test valid word submission."""
        with self.client:
            self.client.get('/')  # Initialize game and create board
            board = session['board']
            valid_word = "YOUR_VALID_WORD"  # Replace with an actual valid word from the board

            response = self.client.post('/check', json={"guess": valid_word})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'ok')

    def test_check_invalid_word(self):
        """Test invalid word submission."""
        with self.client:
            self.client.get('/')
            invalid_word = "INVALIDWORD"

            response = self.client.post('/check', json={"guess": invalid_word})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'not-a-word')

    def test_check_word_not_on_board(self):
        """Test word that is valid but not on the board."""
        with self.client:
            self.client.get('/')
            board = session['board']
            not_on_board_word = "NOT_ON_BOARD"  # Choose a valid word not present on the board

            response = self.client.post('/check', json={"guess": not_on_board_word})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'not-on