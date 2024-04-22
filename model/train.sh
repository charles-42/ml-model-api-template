#!/bin/bash

# Define your Python script and its parameters
run_name="first_run_2017"
start_date="2017-01-01"
end_date="2018-01-01"

# Run the Python script with parameters
python model/main.py $run_name $start_date $end_date 

# # Define your pytest command and its parameters
pytest_parameters="--run_name=$run_name"

# # Run pytest with parameters
pytest model/test_quality.py $pytest_parameters