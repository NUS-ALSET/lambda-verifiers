var dockerLambda = require('docker-lambda');
console.log("Preparing to test docker images");

theEvent = {tests:{"1":"self.assertEqual(2,2)"}};

// docker run -v "$PWD":/var/task lambci/lambda index.handler '{"some": "event"}

var lambdaCallbackResult = dockerLambda({
                //dockerImage: "lambci/lambda:python2.7",
                //dockerArgs: ['-m', '1.5G'],
                //handler: "verifier.lambda_handler",
                event: theEvent});

console.log(lambdaCallbackResult);
