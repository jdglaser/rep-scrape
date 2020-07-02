zip -r ../deployment.zip .
aws lambda update-function-code --function-name arn:aws:lambda:us-east-1:618556235307:function:RepScrape --zip-file fileb://C:/Users/jarre/Documents/deployment.zip