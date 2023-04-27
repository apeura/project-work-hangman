import unittest
from frontend.util.utility import *
from frontend.hangman import *
from backend import *


class TestValidation(unittest.TestCase):
    #def test_execute_menu_choice(self):
#        self.assertTrue(execute_menu_choice(1))
#        self.assertTrue(execute_menu_choice(2))
#        self.assertTrue(execute_menu_choice(3))

#        self.assertFalse(execute_menu_choice(7))
#        self.assertFalse(execute_menu_choice(3.5))

#        self.assertEqual(execute_menu_choice(3), 4)
        
        #self.assertRaises(ValueError, execute_menu_choice, ("k"))
        #self.assertRaises(ValueError, execute_menu_choice, ("maurice"))
        #self.assertRaises(ValueError, execute_menu_choice, (" "))
        #self.assertRaises(ValueError, execute_menu_choice, ("-"))
        #self.assertRaises(TypeError, is_date, (0000))


    def test_format_time(self):
        # Test case for time with including hour, minute and second
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

if __name__ == '__main__':
    unittest.main()