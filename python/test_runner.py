from __future__ import print_function
import os
import sys
import unittest
import json
# Might need to do a try catch on this one. 
# import * is only allowed from the root module level. 
#from usercode import *

importWasSucessful = True
importErrorMsg = ""
try: 
    from usercode import *
except Exception, e:
    importWasSucessful = False
    importErrorMsg = "Import error ({0}). ".format(e)
    if hasattr(e, 'text'):
        importErrorMsg += e.text

def test_generator(theAssert):
        #This is returning a test to run. 
        def test(self):
            eval(theAssert)
        return test

# Run eval each assert as a unit test test case and return results
def run_tests(theAsserts):
    response = {"allPassed": True}
    
    if( not importWasSucessful):
        print("*** Here")
        response["allPassed"] = False
        response["importErrorMsg"] = importErrorMsg
        return response
    
    testResults = {}
    for key in theAsserts:
        class TestSequense(unittest.TestCase):
            pass

        theAssert = theAsserts[key]
        test_name = 'test_%s' % theAssert
        test = test_generator(theAssert)
        setattr(TestSequense, test_name, test)

        suite = unittest.TestLoader().loadTestsFromTestCase(TestSequense)

        testResult = unittest.TextTestRunner(verbosity=2).run(suite)

        print(testResult.wasSuccessful())
        testResults[key] = { "call": theAssert,
                    "success":testResult.wasSuccessful()}
        if(len(testResult.failures)>0):
            testResults[key]["falures"] = str(testResult.failures[0])
            response["allPassed"] = False
            print(type(testResults[key]["falures"]))
        if(len(testResult.errors)>0):
            testResults[key]["errors"] = str(testResult.errors[0])
            response["allPassed"] = False
            print(type(testResults[key]["errors"]))

    response["testResults"] = testResults
    return response

if __name__ == "__main__":
    print("Running from command line")
    passed_in_tests = {"5":"self.assertEqual(2,2)",
        "6": "self.assertEqual(sum(1,2),3)", #usercode
        "7": "self.assertEqual(1,2)", #failing assert
        "8": "self.assertEqual()" # Bad assert
    }

    theResults = run_tests(passed_in_tests)
    from pprint import pprint
    pprint(theResults)
