# -*- mode: ruby -*-
# vi: set ft=ruby :
# frozen_string_literal: true

ANSIBLE_INVENTORY='environments/staging'
BAIKAL_DOMAIN = 'staging.baikal.lesikov.com'
NXC_FQDN = 'staging.nextcloud.lesikov.com'

def update_hosts(instance, domains)
  # update /etc/hosts on host
  instance.hostsupdater.aliases = domains
  # update /etc/hosts on guest
  instance.vm.provision 'hosts' do |provisioner|
    provisioner.add_host '127.0.90.1', domains
  end
end

def fix_dns_ubuntu(vm)
  # make ubuntu use standard dns-server on the gateway instead of some shitty
  # 3rd-party ones hardcoded into image
  vm.provision 'shell', inline: <<-SCRIPT
      sudo add-apt-repository ppa:rmescandon/yq
      sudo apt-get install yq -y
      yq delete -i /etc/netplan/01-netcfg.yaml network.ethernets.eth0.nameservers
      sudo netplan apply
  SCRIPT
end

def provision_ansible(vm, playbook, hosts_limit)
  # install python to run ansible
  vm.provision 'shell', inline: <<-SCRIPT
      sudo apt-get install -y python3-minimal
  SCRIPT

  vm.provision 'ansible' do |ansible|
    ansible.playbook = playbook
    ansible.inventory_path = ANSIBLE_INVENTORY
    ansible.limit = hosts_limit
    if ENV.key?('VG_ANSIBLE_SKIP_TAGS')
      ansible.skip_tags = ENV['VG_ANSIBLE_SKIP_TAGS'].split(',')
    end
    if ENV.key?('VG_ANSIBLE_VERBOSITY')
      ansible.verbose = ENV['VG_ANSIBLE_VERBOSITY']
    end
  end
end

def pytest(vm, test_dir, opts)
  vm.provision 'host_shell' do |host_shell|
    host_shell.inline = <<-SCRIPT
        cd test/e2e/pytest/#{test_dir}
        pytest -x --color=yes --tb=line #{opts.join(' ')}
    SCRIPT
  end
end

Vagrant.configure('2') do |config|

  config.vagrant.plugins = %w[
    vagrant-hostsupdater vagrant-host-shell vagrant-hosts
  ]

  config.vm.define 'home_server1' do |home_server1|
    home_server1.vm.box = 'generic/ubuntu1804'
    home_server1.vm.hostname = 'home-server1-staging'
    home_server1.vm.network 'private_network', ip: '10.20.30.2'
    home_server1.vm.provider 'libvirt' do |libvirt|
      libvirt.memory = 2560
      libvirt.cpus = 4
      libvirt.cpu_mode = 'custom'
      libvirt.cpu_model = 'qemu64'
    end

    update_hosts(home_server1, [BAIKAL_DOMAIN, NXC_FQDN])
    fix_dns_ubuntu(home_server1.vm)
    provision_ansible(home_server1.vm, 'playbook.yml', 'home_server1')
    pytest(home_server1.vm, 'home_server1', [
      "--baikal-baseurl='https://#{BAIKAL_DOMAIN}'",
      "--baikal-user='admin'",
      "--baikal-pass='CHANGEME'",
      "--nxc-baseurl='https://#{NXC_FQDN}'",
      "--nxc-user='admin'",
      "--nxc-pass='CHANGEME'",
    ])

  end

  config.vm.define 'home_workstation1' do |home_workstation1|
    home_workstation1.vm.box = 'generic/ubuntu1804'
    home_workstation1.vm.hostname = 'home-workstation1-staging'
    # update /etc/hosts on host
    home_workstation1.vm.network 'private_network', ip: '10.20.30.3'
    home_workstation1.vm.provider 'libvirt' do |libvirt|
      libvirt.memory = 2560
      libvirt.cpus = 4
      libvirt.cpu_mode = 'custom'
      libvirt.cpu_model = 'qemu64'
    end

    fix_dns_ubuntu(home_workstation1.vm)
    provision_ansible(home_workstation1.vm, 'playbook.yml', 'home_workstation1')
  end
end
