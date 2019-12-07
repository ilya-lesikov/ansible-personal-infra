#!/usr/bin/env python3
import time

from flaky import flaky


def _is_assertion_error(err):
    return issubclass(err[0], AssertionError)


def _delay_rerun(err, *args):
    time.sleep(2)
    return _is_assertion_error(err)


def test_docker_service_up(host):
    docker = host.service('docker')
    assert docker.is_running
    assert docker.is_enabled


def test_postgres_container_up(host):
    with host.sudo():
        postgres_containers = host.docker.get_containers(
            name='postgres', status='running'
        )
    assert len(postgres_containers) == 1


@flaky(max_runs=10, min_passes=1, rerun_filter=_delay_rerun)
def test_postgres_port_reachable(host):
    assert host.addr('172.10.72.3').port(5432).is_reachable


@flaky(max_runs=10, min_passes=1, rerun_filter=_delay_rerun)
def test_postgres_user_added(host):
    out = host.check_output(
        "PGPASSWORD=CHANGEME psql -h 172.10.72.3 -U postgres "
        "-c \"SELECT usename FROM pg_catalog.pg_user WHERE usename = 'user1';\""
    )
    assert 'user1' in out


@flaky(max_runs=10, min_passes=1, rerun_filter=_delay_rerun)
def test_postgres_db_added(host):
    out = host.check_output(
        "PGPASSWORD=CHANGEME psql -h 172.10.72.3 -U postgres "
        "-c \"SELECT datname FROM pg_catalog.pg_database "
        "WHERE datname = 'user1_db';\""
    )
    assert 'user1_db' in out
