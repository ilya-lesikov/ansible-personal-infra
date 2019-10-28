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


def test_traefik_container_up(host):
    with host.sudo():
        traefik_containers = host.docker.get_containers(
            name='traefik', status='running'
        )
    assert len(traefik_containers) == 1


@flaky(max_runs=10, min_passes=1, rerun_filter=_delay_rerun)
def test_traefik_ports_reachable(host):
    addr = host.addr('172.10.70.2')
    assert addr.port(80).is_reachable
    assert addr.port(443).is_reachable
    assert addr.port(8080).is_reachable


@flaky(max_runs=10, min_passes=1, rerun_filter=_delay_rerun)
def test_traefik_api_reachable(host):
    out = host.check_output('curl -sS -k --digest --user admin:CHANGEME'
                            ' http://172.10.70.2:8080/api/rawdata')
    assert 'api@internal' in out


@flaky(max_runs=10, min_passes=1, rerun_filter=_delay_rerun)
def test_traefik_service1_added(host):
    out = host.check_output('curl -sS -k --digest --user admin:CHANGEME'
                            ' http://172.10.70.2:8080/api/rawdata')

    assert '"http-service1@file"' in out
    assert '"https-service1@file"' in out
    assert '"http-to-https@file"' in out
    assert '"rule":"Host(`service1.example.org`)"' in out
    assert '"url":"http://172.10.71.3:80"' in out
