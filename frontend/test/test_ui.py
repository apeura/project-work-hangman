#python3 -m unittest discover 

from unittest.mock import patch
import unittest
from util.utility import *
from util.drawings import *
from hangman import *

class TestValidation(unittest.TestCase):

    def test_format_time(self):
        # ASSERT EQUAL
        # Test case for time with including hour, minute and seconds
        game_time = "01:23:45"
        expected_output = "1 hour 23 minutes 45 seconds"
        self.assertEqual(format_time(game_time), expected_output)

        # Test case for time with only minutes and seconds
        game_time = "00:05:30"
        expected_output = "5 minutes 30 seconds"
        self.assertEqual(format_time(game_time), expected_output)

        # Test case for time with only seconds
        game_time = "00:00:45"
        expected_output = "0 minutes 45 seconds"
        self.assertEqual(format_time(game_time), expected_output)

        # ASSERT NOT EQUAL
        # Test case for time with only seconds
        # should output only seconds
        game_time = "00:00:45"
        expected_output = "0 hours 0 minutes 45 seconds"
        self.assertNotEqual(format_time(game_time), expected_output)

        # Test case for time with hour, minute and seconds
        # game_time format is incorrect as the hour is 1, not 01
        game_time = "10:10:10"
        expected_output = "10 hour 10 minute 10 seconds"
        self.assertNotEqual(format_time(game_time), expected_output)


    def test_print_menu_take_choice(self):
        
        # Ensure menu is printed and user input is taken
        with patch('builtins.input', side_effect=["1"]):
            with patch('hangman.execute_menu_choice', return_value=None) as mock_exec:
                print_menu_take_choice()
                mock_exec.assert_called_once_with("1")


if __name__ == '__main__':
    unittest.main()