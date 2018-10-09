import unittest
from src.table.Table import Table
from test import support

class unitTestTable(unittest.Testcase):

    #def setUp(self):
        #setup variables needed to run test

    #def tearDown(self):
        #code that needs cleaning up goes here

    def testOne(self):
        print("hi")



def test_main():
    support.run_unittest(unitTestTable)


if __name__ == '__main__':
    test_main()