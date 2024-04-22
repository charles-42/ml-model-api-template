#!/bin/bash

# Define your Python script and its parameters
run_name="second_run_2017"
start_date="2017-01-01"
end_date="2018-01-01"

# Run the Python script with parameters
python -m model.main $run_name $start_date $end_date 

# # Define your pytest command and its parameters
pytest_parameters="--run_name=$run_name"

# # Run pytest with parameters
pytest model $pytest_parameters