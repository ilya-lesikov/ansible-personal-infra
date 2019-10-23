# -*- mode: ruby -*-
# vi: set ft=ruby :


Vagrant.configure('2') do |config|
  baikal_domain = 'staging.baikal.lesikov.com'

  config.vagrant.plugins = [
    'vagrant-hostsupdater', 'vagrant-host-shell', 'vagrant-hosts'
  ]

  config.vm.define 'ub1804' do |ub1804|
    ub1804.vm.box = 'generic/ubuntu1804'

    # ub1804.ssh.username = 'vagrant'
    # ub1804.ssh.password = 'vagrant'

    ub1804.vm.hostname = 'home-server1-staging'
    ub1804.hostsupdater.aliases = [baikal_domain]
    ub1804.vm.network 'private_network', ip: '10.20.30.2'

    ub1804.vm.provider 'libvirt' do |libvirt|
      libvirt.memory = 2560
      libvirt.cpus = 4
      libvirt.cpu_mode = 'custom'
      libvirt.cpu_model = 'qemu64'
    end

    ub1804.vm.provision 'hosts' do |provisioner|
      provisioner.add_host '127.0.90.1', [baikal_domain]
    end

    # make ubuntu use standard dns-server on the gateway instead of some shitty
    # 3rd-party ones that hardcoded into image
		ub1804.vm.provision 'shell', inline: <<-EOF
      sudo add-apt-repository ppa:rmescandon/yq
      sudo apt-get install yq -y
      yq delete -i /etc/netplan/01-netcfg.yaml network.ethernets.eth0.nameservers
      sudo netplan apply
			EOF

    ub1804.vm.provision 'shell', inline: <<-EOF
      sudo apt-get install -y python-minimal python-docker
      EOF

    ub1804.vm.provision 'ansible' do |ansible|
      ansible.extra_vars = {
        cloudflare_api_email: ENV['CF_API_EMAIL'],
        cloudflare_api_key: ENV['CF_API_KEY'],
      }
      ansible.playbook = 'home-server1.yml'
      ansible.inventory_path = 'environments/staging'
      # ansible.verbose = 'vvvv'
      ansible.limit = 'all'
    end

    ub1804.vm.provision 'host_shell' do |host_shell|
      host_shell.inline = <<-EOF
        cd test/smoke/pytest
        pytest -x --color=yes --tb=line \
          --baikal-baseurl='https://#{baikal_domain}/'
        EOF
    end

  end
end

# out = `cd test/smoke/pytest &&\
#   pytest --color=yes -x --tb=line --baikal-baseurl='https://#{baikal_domain}/' 2>&1`
# $?.success? ? out : abort(out + "\nPYTEST FAILED")
