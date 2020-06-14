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


def test_terraria_container_up(host):
    with host.sudo():
        terraria_containers = host.docker.get_containers(
            name='terraria', status='running'
        )
    assert len(terraria_containers) == 1


@flaky(max_runs=10, min_passes=1, rerun_filter=_delay_rerun)
def test_terraria_port_reachable(host):
    assert host.addr('172.10.74.3').port(7777).is_reachable
