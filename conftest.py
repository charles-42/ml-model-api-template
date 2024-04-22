def pytest_addoption(parser):
    parser.addoption("--run_name", action="store", default="test_run")
    parser.addoption("--start_date", action="store", default="2017-01-01")
    parser.addoption("--end_date", action="store", default="2018-01-01")

def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    option_value = metafunc.config.option.run_name
    if 'run_name' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("run_name", [option_value])
        