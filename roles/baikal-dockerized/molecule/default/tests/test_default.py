#!/usr/bin/env python2
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


def test_baikal_container_up(host):
    with host.sudo():
        baikal_containers = host.docker.get_containers(
            name='baikal', status='running'
        )
    assert len(baikal_containers) == 1


@flaky(max_runs=10, min_passes=1, rerun_filter=_delay_rerun)
def test_baikal_port_reachable(host):
    assert host.addr('172.10.71.3').port(80).is_reachable


@flaky(max_runs=10, min_passes=1, rerun_filter=_delay_rerun)
def test_baikal_app_reachable(host):
    out = host.check_output('curl -sS http://172.10.71.3:80')
    assert 'is running alright' in out
