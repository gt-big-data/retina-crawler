Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provision :shell, path: "vagrant_bootstrap"
  # config.vm.network "forwarded_port", guest: 80, host: 8080
  #
  config.vm.provider :virtualbox do |v|
    v.memory = 2048
    v.cpus = 2
  end
end
