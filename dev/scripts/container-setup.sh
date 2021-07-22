#!/bin/bash

python -m venv env
source env/bin/activate
pip install -r dev/requirements.txt
pip install -r requirements.txt
