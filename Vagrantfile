BOX_IMAGE = "hashicorp/bionic64" 
BOX_VER = "1.0.282"
NODE_COUNT = 4

Vagrant.configure(2) do |config|

    # ----------------- Sequencer --------------------------

    config.vm.define "sequencer" do |subconfig|
        subconfig.vm.synced_folder "./", "/vagrant"
        subconfig.vm.box = BOX_IMAGE
        subconfig.vm.box_version = BOX_VER
        subconfig.vm.hostname = "sequencer"
        subconfig.vm.network :private_network, ip: "10.0.1.10"
        subconfig.vm.provision "shell", inline: <<-SHELL
            sudo apt-get update
            sudo apt-get -y install python3-pip         
            sudo apt-get install gunicorn
            sudo apt-get -y autoremove
            cd /vagrant/sequencer
            sudo pip3 install -r requirements.txt
        SHELL
        subconfig.trigger.after :up do |trigger|
            trigger.name = "Run sequencer"
            trigger.run_remote = {
                inline: <<-SHELL
                    cp /vagrant/sequencer/sequencer.service /etc/systemd/system
                    systemctl --system daemon-reload
                    systemctl enable sequencer
                    systemctl start sequencer
                SHELL
            }
        end
    end

    # ----------------- Shuffler ---------------------------

    config.vm.define "shuffler" do |subconfig|
        subconfig.vm.synced_folder "./", "/vagrant"
        subconfig.vm.box = BOX_IMAGE
        subconfig.vm.box_version = BOX_VER
        subconfig.vm.hostname = "shuffler"
        subconfig.vm.network :private_network, ip: "10.0.1.11"
        subconfig.vm.provision "shell", inline: <<-SHELL
            sudo apt-get update
            sudo apt-get -y install python3-pip
            sudo apt-get -y autoremove
            cd /vagrant/shuffler
            sudo pip3 install -r requirements.txt
        SHELL
        subconfig.trigger.after :up do |trigger|
            trigger.name = "Run shuffler"
            trigger.run_remote = {
                inline: <<-SHELL
                    cp /vagrant/shuffler/shuffler.service /etc/systemd/system
                    systemctl --system daemon-reload
                    systemctl enable shuffler
                    systemctl start shuffler
                SHELL
            }
        end
    end

    # ----------------- BankServer -------------------------

    (1..NODE_COUNT).each do |i|
        config.vm.define "bank-server-#{i}" do |subconfig|
            subconfig.vm.synced_folder "./", "/vagrant"
            subconfig.vm.box = BOX_IMAGE
            subconfig.vm.box_version = BOX_VER
            subconfig.vm.hostname = "bank-server-#{i}"
            subconfig.vm.network :private_network, ip: "10.0.1.#{i + 11}"
            subconfig.vm.provision "shell", inline: <<-SHELL
                sudo apt-get update
                sudo apt-get -y install python3-pip
                sudo apt-get -y autoremove
                cd /vagrant/bank_server
                sudo pip3 install -r requirements.txt
            SHELL
            subconfig.trigger.after :up do |trigger|
                trigger.name = "Run bank-server"
                trigger.run_remote = {
                    inline: <<-SHELL
                    cp /vagrant/bank_server/bank_server.service /etc/systemd/system
                    systemctl --system daemon-reload
                    systemctl enable bank_server
                    systemctl start bank_server
                    SHELL
                }
            end
        end
    end

end