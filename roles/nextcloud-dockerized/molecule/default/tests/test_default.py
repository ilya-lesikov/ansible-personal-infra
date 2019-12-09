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


def test_nextcloud_container_up(host):
    with host.sudo():
        nextcloud_containers = host.docker.get_containers(
            name='nextcloud', status='running'
        )
    assert len(nextcloud_containers) == 1


@flaky(max_runs=10, min_passes=1, rerun_filter=_delay_rerun)
def test_nextcloud_ip_port_reachable(host):
    assert host.addr('172.10.73.3').port(80).is_reachable


@flaky(max_runs=10, min_passes=1, rerun_filter=_delay_rerun)
def test_nextcloud_domain_port_reachable(host):
    assert host.addr('nextcloud.example.org').port(80).is_reachable


@flaky(max_runs=10, min_passes=1, rerun_filter=_delay_rerun)
def test_nextcloud_app_reachable(host):
    out = host.check_output('curl -L -sS http://nextcloud.example.org:80')
    assert 'loginUsername' in out
