#!/usr/bin/env python3
from faker import Faker


fake = Faker()
OPTS = {
    'baikal_baseurl': 'http://localhost:80',
    'baikal_user': 'admin',
    'baikal_pass': 'test1',
    'baikal_dav_user': fake.user_name(),
    'baikal_dav_pass': fake.password(),
    'baikal_dav_email': fake.email()
}


def pytest_addoption(parser):
    for opt, default in OPTS.items():
        parser.addoption(f'--{opt.replace("_", "-")}', action="store", default=default)


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    for opt, _ in OPTS.items():
        val = vars(metafunc.config.option)[opt]
        if opt in metafunc.fixturenames and val is not None:
            metafunc.parametrize(opt, [val])
