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


def test_baikal_container_up(host):
    with host.sudo():
        baikal_containers = host.docker.get_containers(
            name='baikal', status='running'
        )
    assert len(baikal_containers) == 1


def test_baikal_port_reachable(host):
    retries = range(20)
    for retry in retries:
        try:
            assert host.addr('172.10.71.3').port(80).is_reachable
        except AssertionError:
            if retry == retries[-1]:
                raise
            else:
                time.sleep(1)
                continue
        break


def test_baikal_app_reachable(host):
    retries = range(20)
    for retry in retries:
        try:
            assert host.run_test('curl -sS http://172.10.71.3:80 | grep Baikal')
        except AssertionError:
            if retry == retries[-1]:
                raise
            else:
                time.sleep(1)
                continue
        break
