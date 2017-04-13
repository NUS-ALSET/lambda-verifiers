//docker run -v "$PWD":/var/task lambci/lambda node/index.foo '{"some": "event"}'
//docker run -v "$PWD":/var/task lambci/lambda index.handler '{"some": "event"}
var exports = module.exports = {};
        
exports.handler = function(event, context) {
  console.log(event);
  context.succeed({'Hello':'from handler'});
  return;
};

exports.foo = function(event, context) {
  console.log({"From":"index.foo","how":"to pass data"});
  context.succeed({'Hello':'from foo'});
  return;
};
