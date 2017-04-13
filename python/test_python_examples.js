
/*
 For folder in examples, 
 read in the ipynb file. 
 read in the tests.json
 create a codeWithTests ojbect to pass to event. 
 read in expected results from examples folder. 
 call lambda function. 
 compare lambda results with expected results in the folder. 
*/

const fs = require('fs')
const path = require('path')

function getDirectories (srcpath) {
  return fs.readdirSync(srcpath)
    .filter(file => fs.statSync(path.join(srcpath, file)).isDirectory())
}

function getIpynbFileFromDirectory(srcpath){
    //var files = fs.readdirSync(srcpath);
    var files = fs.readdirSync(__dirname+'/examples/'+srcpath).filter(file => file.endsWith("ipynb"));
    file = __dirname+'/examples/'+srcpath+'/'+files[0];
    //console.log(file);
    var ipynbObj = JSON.parse(fs.readFileSync(file, 'utf8'));
    //console.log(ipynbObj);
    return ipynbObj;
} 

function getTestsFromDirectory(srcpath){
    //var files = fs.readdirSync(srcpath);
    file = __dirname+'/examples/'+srcpath+'/tests.json';
    //console.log(file);
    var tests = JSON.parse(fs.readFileSync(file, 'utf8'));
    //console.log(tests);
    return tests;
} 

function testCode(codeWithTests, callback){
  var cmd = 'docker run -v "$PWD":/var/task lambci/lambda:python2.7 verifier.lambda_handler \' '+JSON.stringify(codeWithTests) +'\' ';
  //console.log(cmd);
  var exec = require('child_process').exec;
  exec(cmd, function(error, stdout, stderr) {
    jsonResult = JSON.parse(stdout);
    callback(jsonResult);
  });
}

function compareToExpectedResults(exampleDirectory, results){
    file = __dirname+'/examples/'+exampleDirectory+'/expected_results.json';
    var expectedResults = JSON.parse(fs.readFileSync(file, 'utf8'));
    allResultsMatch = true;
    
    if(expectedResults["allPassed"] != results["allPassed"]){
      allResultsMatch = false; 
    } 

    for(prop in results['testResults']){
        //console.log(prop);
        if(results['testResults'][prop]['success'] != expectedResults['testResults'][prop]['success'] ){
          console.log(exampleDirectory,'test',prop,"does not match expected results.")
          allResultsMatch = false
        } 
    }

    if(allResultsMatch){
      console.log(exampleDirectory,"produced expected results");
    }
    else{
      console.log("\n", exampleDirectory, "did not produce expected results.\n")
      console.log("expectedResults -->",expectedResults);
      console.log(exampleDirectory,"result -->", results);
    }

}


// Execute the test on each example. 
exampleDirectories = getDirectories('examples');

exampleDirectories.map( function(exampleDirectory) {
    //console.log(exampleDirectory);
    ipynbObject = getIpynbFileFromDirectory(exampleDirectory);
    tests = getTestsFromDirectory(exampleDirectory)
     ipynbObject["tests"] = tests;
     result = testCode(ipynbObject, function(results) {
        compareToExpectedResults(exampleDirectory, results)
        
     });
    
});
