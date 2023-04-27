# python3 -m unittest test.test_hangman
#E
#======================================================================
#ERROR: test_hangman (unittest.loader._FailedTest)
#----------------------------------------------------------------------
#ImportError: Failed to import test module: test_hangman
#Traceback (most recent call last):
#  File "/usr/lib/python3.10/unittest/loader.py", line 154, in loadTestsFromName
#    module = __import__(module_name)
#  File "/mnt/c/Users/peura/project-work-hangman/test/test_hangman.py", line 5, in <module>
#    from frontend.hangman import execute_menu_choice
#  File "/mnt/c/Users/peura/project-work-hangman/frontend/hangman.py", line 5, in <module>
#    from util.drawings import draw_hangman
#ModuleNotFoundError: No module named 'util'

import os
#print(os.getcwd()) #/mnt/c/Users/peura/project-work-hangman/test

import sys
#sys.path.append("/mnt/c/Users/peura/project-work-hangman/test")

import unittest

from frontend.hangman import execute_menu_choice
from frontend.util.drawings import draw_hangman
from frontend.util.utility import *

class TestValidation(unittest.TestCase):
    def test_execute_menu_choice(self):
        pass
