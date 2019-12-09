# -*- mode: ruby -*-
# vi: set ft=ruby :
# frozen_string_literal: true

Vagrant.configure('2') do |config|
  baikal_domain = 'staging.baikal.lesikov.com'
  nxc_fqdn = 'staging.nextcloud.lesikov.com'

  config.vagrant.plugins = %w[
    vagrant-hostsupdater vagrant-host-shell vagrant-hosts
  ]

  config.vm.define 'ub1804' do |ub1804|
    ub1804.vm.box = 'generic/ubuntu1804'
    ub1804.vm.hostname = 'home-server1-staging'
    # update /etc/hosts on host
    ub1804.hostsupdater.aliases = [baikal_domain]
    ub1804.vm.network 'private_network', ip: '10.20.30.2'

    ub1804.vm.provider 'libvirt' do |libvirt|
      libvirt.memory = 2560
      libvirt.cpus = 4
      libvirt.cpu_mode = 'custom'
      libvirt.cpu_model = 'qemu64'
    end

    # update /etc/hosts on guest
    ub1804.vm.provision 'hosts' do |provisioner|
      provisioner.add_host '127.0.90.1', [baikal_domain]
      provisioner.add_host '127.0.90.2', [nxc_fqdn]
    end

    # make ubuntu use standard dns-server on the gateway instead of some shitty
    # 3rd-party ones hardcoded into image
    ub1804.vm.provision 'shell', inline: <<-SCRIPT
      sudo add-apt-repository ppa:rmescandon/yq
      sudo apt-get install yq -y
      yq delete -i /etc/netplan/01-netcfg.yaml network.ethernets.eth0.nameservers
      sudo netplan apply
    SCRIPT

    # install python to run ansible
    ub1804.vm.provision 'shell', inline: <<-SCRIPT
      sudo apt-get install -y python3-minimal
    SCRIPT

    # provision with ansible
    ub1804.vm.provision 'ansible' do |ansible|
      ansible.playbook = 'home-server1.yml'
      ansible.inventory_path = 'environments/staging'
      ansible.limit = 'all'
    end

    # perform infra-wide smoke testing
    ub1804.vm.provision 'host_shell' do |host_shell|
      host_shell.inline = <<-SCRIPT
        cd test/smoke/pytest
        pytest -x --color=yes --tb=line \
          --baikal-baseurl='https://#{baikal_domain}/' \
          --baikal-user='admin' \
          --baikal-pass='CHANGEME' \
          --nxc_baseurl='https://#{nxc_fqdn}' \
          --nxc-user='admin' \
          --nxc-pass='CHANGEME'
      SCRIPT
    end
  end
end
