from frontend.hangman import execute_menu_choice
import unittest

class TestValidation(unittest.TestCase):
    def test_execute_menu_choice(self):
#        self.assertTrue(execute_menu_choice(1))
#        self.assertTrue(execute_menu_choice(2))
#        self.assertTrue(execute_menu_choice(3))

#        self.assertFalse(execute_menu_choice(7))
#        self.assertFalse(execute_menu_choice(3.5))

#        self.assertEqual(execute_menu_choice(3), 4)
        
        self.assertRaises(ValueError, execute_menu_choice, ("k"))
        self.assertRaises(ValueError, execute_menu_choice, ("maurice"))
        self.assertRaises(ValueError, execute_menu_choice, (" "))
        self.assertRaises(ValueError, execute_menu_choice, ("-"))
        #self.assertRaises(TypeError, is_date, (0000))

if __name__ == '__main__':
    unittest.main()