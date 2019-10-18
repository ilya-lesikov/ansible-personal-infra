import os
import time

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


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


def test_traefik_ports_reachable(host):
    addr = host.addr('172.10.70.2')
    retries = range(20)
    for retry in retries:
        try:
            assert addr.port(80).is_reachable
            assert addr.port(443).is_reachable
            assert addr.port(8080).is_reachable
        except AssertionError:
            if retry == retries[-1]:
                raise
            else:
                time.sleep(1)
                continue
        break


def test_traefik_api_reachable(host):
    retries = range(20)
    for retry in retries:
        try:
            assert host.run_test('curl -sS -k --digest --user admin:CHANGEME'
                                 ' http://172.10.70.2:8080/api/rawdata'
                                 ' | grep -F "api@internal"')
        except AssertionError:
            if retry == retries[-1]:
                raise
            else:
                time.sleep(1)
                continue
        break


def test_traefik_service1_added(host):
    retries = range(20)
    for retry in retries:
        try:
            cmd = host.run('curl -sS -k --digest --user admin:CHANGEME'
                           ' http://172.10.70.2:8080/api/rawdata')
            assert cmd.rc == 0
        except AssertionError:
            if retry == retries[-1]:
                raise
            else:
                time.sleep(1)
                continue
        break

    assert '"http-service1@file"' in cmd.stdout
    assert '"https-service1@file"' in cmd.stdout
    assert '"http-to-https@file"' in cmd.stdout
    assert '"rule":"Host(`service1.example.org`)"' in cmd.stdout
    assert '"url":"http://172.10.71.3:80"' in cmd.stdout
