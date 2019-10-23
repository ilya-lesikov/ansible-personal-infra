# -*- mode: ruby -*-
# vi: set ft=ruby :


Vagrant.configure('2') do |config|
  baikal_domain = 'staging.baikal.lesikov.com'

  config.vagrant.plugins = ['vagrant-hostsupdater', 'vagrant-host-shell']

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

    ub1804.vm.provision 'ansible' do |ansible|
      ansible.playbook = 'staging.yml'
    end

    ub1804.vm.provision 'host_shell' do |host_shell|
      host_shell.inline = <<-EOF
        cd test/smoke/pytest
        pytest -x --color=yes --tb=line \
          --baikal-baseurl='https://#{baikal_domain}:38888/'
        EOF
    end

		# ub1804.vm.provision 'shell', inline: <<-SCRIPT
		# 	echo #{ub1804.vm.networks[0][1][:ip]}
		# 	echo I am provisioning...
		# 	date > /etc/vagrant_provisioned_at
		# 	SCRIPT
  end
end

# out = `cd test/smoke/pytest &&\
#   pytest --color=yes -x --tb=line --baikal-baseurl='https://#{baikal_domain}/' 2>&1`
# $?.success? ? out : abort(out + "\nPYTEST FAILED")
