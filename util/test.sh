#!/bin/sh
cp ../examples/invResult_0318_DAS.txt .
python removeCharLines.py
python processFile_4lay.py


