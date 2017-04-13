#docker run -v "$PWD":/var/task lambci/lambda:python2.7 python/lambda_function.lambda_handler

# run passing, failing, and erroring tests. 
# docker run -v "$PWD":/var/task lambci/lambda:python2.7 python/verifier.lambda_handler '{"tests": {"1":"self.assertEqual(2,2)","2": "self.assertEqual(sum(1,2),3)","3": "self.assertEqual(1,2)","4": "self.assertEqual()"}}'

# Just a test lambda, run with:
# docker run -v "$PWD":/var/task lambci/lambda:python2.7
from __future__ import print_function
import os
import sys
import unittest
import json
# Might need to do a try catch on this one. 
# import * is only allowed from the root module level. 
#from usercode import *

# TODO: update handler to call run tests using test from passed in event data

def lambda_handler(event, context):
    #print(event)
    
    #print(theResults)
    
    #TODO save the usercode from event data.     
    
    import test_runner
    #some_tests = {"1":"self.assertEqual(2,2)",
    #    "2": "self.assertEqual(sum(1,2),3)", #usercode
    #    "3": "self.assertEqual(1,2)", #failing assert
    #    "4": "self.assertEqual()" # Bad assert
    #}
    #theResults = run_tests(some_tests)
    
    theResults = test_runner.run_tests(event["tests"])
    
    #Test to see if any non-serializable python types are in the result. 
    #jsonResults = json.dumps(theResults)
    #print("---- Printing from container ------\n")
    
    from pprint import pprint
    pprint(theResults)
    print("\n---- End printing from container ------")

    #data = {"some":"data"}
    #print(type(context))
    #print(dir(context))
    #print(context.client_context)
    #print(context.xray_context)
    

    #context.log("hello")
    return theResults

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
