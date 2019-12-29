import unittest
import student_code

class SetupTest(unittest.TestCase):
    def test1(self):
    	result = student_code.hello_world()
    	self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
