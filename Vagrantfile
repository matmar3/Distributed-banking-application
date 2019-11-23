Vagrant.configure(2) do |config|
    # default for all
    config.vm.synced_folder "./", "/vagrant"

    # VM for Sequencer
    config.vm.define "sequencer" do |cfg|
      # Sequencer location
      cfg.vm.synced_folder "./sequencer", "/vagrant/sequencer"
      # VM box
      cfg.vm.box = "hashicorp/bionic64"
      cfg.vm.box_version = "1.0.282"
      # Network configuration
      cfg.vm.network "private_network", ip: "10.0.1.11"
      # Provision a Python environment
      cfg.vm.provision "shell", inline: <<-SHELL
        # Install tools
        sudo apt-get update
        sudo apt-get -y install python-pip
        sudo apt-get -y autoremove
        # Install app dependencies
        cd /vagrant/sequencer
        sudo pip install -r requirements.txt
        # Run server
        nohup python server.py &
      SHELL
    end

    # VM for Sequencer 2
    config.vm.define "sequencer2" do |cfg|
      # Sequencer location
      cfg.vm.synced_folder "./sequencer", "/vagrant/sequencer"
      # VM box
      cfg.vm.box = "hashicorp/bionic64"
      cfg.vm.box_version = "1.0.282"
      # Network configuration
      cfg.vm.network "private_network", ip: "10.0.1.10"
      # Provision a Python environment
      cfg.vm.provision "shell", inline: <<-SHELL
        # Install tools
        sudo apt-get update
        sudo apt-get -y install python-pip
        sudo apt-get -y autoremove
        # Install app dependencies
        cd /vagrant/sequencer
        sudo pip install -r requirements.txt
        # Run server
        python server.py
      SHELL
    end


end
