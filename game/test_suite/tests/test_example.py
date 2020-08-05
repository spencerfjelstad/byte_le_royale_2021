# This is a quick example test file to show you the basics.
# Always remember to add the proper details to the __init__.py file in the 'tests' folder
# to insure your tests are run.

import unittest

class TestExample(unittest.TestCase): #File and class title should say what the file is testing to avoid confusion

    def setUp(self): # This method is used to set up anything you wish to test prior to every test method below.
        self.d = { # Here I'm just setting up a quick dictionary for example.
            "string" : "Hello World!",
            "array" : [1, 2, 3, 4, 5],
            "integer" : 42
            }
    
    def test_dict_array(self): # Test methods should always start with the word 'test'
        t = self.d["array"]
        self.assertEqual(t, [1, 2, 3, 4, 5])
        self.assertEqual(t[2], 3)
        t[2] = 0
        self.assertEqual(t[2], 0)


if __name__ == '__main__':
    unittest.main
