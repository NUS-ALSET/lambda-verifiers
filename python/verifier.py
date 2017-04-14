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

def save_usercode(ipynbJSON):
    j = ipynbJSON
    of = open("usercode.py", 'w') #usercode.py
    if j["nbformat"] >=4:
        for i,cell in enumerate(j["cells"]):
                of.write("#cell "+str(i)+"\n")
                for line in cell["source"]:
                        of.write(line)
                of.write('\n\n')
    else:
        for i,cell in enumerate(j["worksheets"][0]["cells"]):
                of.write("#cell "+str(i)+"\n")
                for line in cell["input"]:
                        of.write(line)
                of.write('\n\n')
    of.close()


def lambda_handler(event, context):
    save_usercode(event)
    import test_runner
    theResults = test_runner.run_tests(event["tests"])
    try:
        os.remove("usercode.py")
        os.remove("usercode.pyc")
    except OSError:
        pass

    from pprint import pprint
    pprint(theResults)
    print("\n---- End printing from container ------")
    return theResults

if __name__ == "__main__":
    print("Running from command line")
    passed_in_tests = {"5":"self.assertEqual(2,2)",
        "6": "self.assertEqual(1,2)", #failing assert
        "7": "self.assertEqual()" # Bad assert
    }

    theResults = run_tests(passed_in_tests)
    from pprint import pprint
    pprint(theResults)
