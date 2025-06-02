#!/bin/bash

python src/data/splitting.py
python src/data/preprocessing.py
python src/models/gridsearch.py
python src/models/training.py
python src/models/evaluation.py
