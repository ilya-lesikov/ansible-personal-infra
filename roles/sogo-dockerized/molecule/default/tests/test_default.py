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


def test_sogo_net_created(host):
    with host.sudo():
        assert host.run_test('docker network inspect sogo_network')


def test_mariadb_container_up(host):
    with host.sudo():
        mariadb_containers = host.docker.get_containers(
            name='mariadb', status='running'
        )
    assert len(mariadb_containers) == 1


def test_mariadb_port_reachable(host):
    retries = range(20)
    for retry in retries:
        try:
            assert host.addr('172.10.70.2').port(3306).is_reachable
        except AssertionError:
            if retry == retries[-1]:
                raise
            else:
                time.sleep(1)
                continue
        break


def test_sogo_container_up(host):
    with host.sudo():
        sogo_containers = host.docker.get_containers(name='sogo', status='running')
    assert len(sogo_containers) == 1


def test_sogo_port_reachable(host):
    retries = range(20)
    for retry in retries:
        try:
            assert host.addr('172.10.70.3').port(80).is_reachable
        except AssertionError:
            if retry == retries[-1]:
                raise
            else:
                time.sleep(1)
                continue
        break
