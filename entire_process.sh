#!/bin/bash

mkdir -p Data
mkdir -p Results

curl -o Data/Movies_Data.csv https://raw.githubusercontent.com/yinghaoz1/tmdb-movie-dataset-analysis/master/tmdb-movies.csv

cd Py
python3 -m venv MAPvenv
source MAPvenv/bin/activate
pip install Pandas

python3 Analyze.py

deactivate
cd ..
