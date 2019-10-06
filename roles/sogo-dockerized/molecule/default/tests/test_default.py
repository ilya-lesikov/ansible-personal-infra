import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


# def test_hosts_file(host):
#     f = host.file('/etc/hosts')

#     assert f.exists assert f.user == 'root'
#     assert f.group == 'root'


def test_docker_up(host):
    docker = host.service('docker')
    assert docker.is_running
    assert docker.is_enabled


def test_mariadb_up(host):
    with host.sudo():
        mariadb_containers = host.docker.get_containers(
            name='mariadb', status='running'
        )
    assert len(mariadb_containers) == 1

    with host.sudo():
        mariadb_ip = mariadb_containers[0].inspect()['NetworkSettings']['IPAddress']
    assert host.addr(mariadb_ip).port(3306).is_reachable


def test_sogo_up(host):
    with host.sudo():
        sogo_containers = host.docker.get_containers(name='sogo', status='running')
    assert len(sogo_containers) == 1

    with host.sudo():
        sogo_ip = sogo_containers[0].inspect()['NetworkSettings']['IPAddress']
    assert host.addr(sogo_ip).port(80).is_reachable
    # pytest.raises(KeyError):
