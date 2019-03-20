#!/bin/bash

zip -r function.zip main.py yelpoet venv/lib/python3.6/site-packages

aws lambda update-function-code --function-name $1 --zip fileb://function.zip

rm function.zip
