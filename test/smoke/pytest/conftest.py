#!/usr/bin/env python3
from urllib3 import disable_warnings

from faker import Faker


fake = Faker()
OPTS = {
    'baikal_baseurl': 'http://localhost:80',
    'baikal_user': 'admin',
    'baikal_pass': 'test1',
    'baikal_dav_user': fake.user_name(),
    'baikal_dav_pass': fake.password(),
    'baikal_dav_email': fake.email(),
    'nxc_baseurl': 'http://localhost:80',
    'nxc_files_dav_prefix': 'remote.php/dav/files',
    'nxc_user': 'admin',
    'nxc_pass': 'CHANGEME',
    'nxc_test_file': 'testfile1.txt'
}


def pytest_sessionstart(session):
    disable_warnings()


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
