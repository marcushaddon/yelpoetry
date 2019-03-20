#!/bin/bash

cd venv/lib/python3.6/site-packages
zip -r9 ../../../../function.zip .
cd ../../../../
zip -gr function.zip lambda_function.py yelpoet

aws lambda update-function-code --function-name $1 --zip fileb://function.zip

rm -rf function.zip
