// dockerLambda will not return result.
var dockerLambda = require('docker-lambda');
var lambdaCallbackResult = dockerLambda({
                dockerImage: "lambci/lambda:python2.7",
                handler: "lambda_function.lambda_handler"
            });
console.log("From dockerLambda -->",lambdaCallbackResult);

// exec will return result.
var exec = require('child_process').exec;
var cmd = 'docker run -v "$PWD":/var/task lambci/lambda:python2.7 lambda_function.lambda_handler';
exec(cmd, function(error, stdout, stderr) {
  console.log("From exec -->",stdout);
});