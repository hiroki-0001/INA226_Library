#!/bin/bash
set -euxo pipefail

HOME_DIR="${HOME}"

if [ -e /etc/systemd/system/INA226VoltAndCurrent_single.service ]; then
	sudo systemctl disable INA226VoltAndCurrent_single.service
fi

sudo ln -s $HOME_DIR/INA226_Library/service_files/INA226VoltAndCurrent_single.service /etc/systemd/system/INA226VoltAndCurrent_single.service
sudo systemctl daemon-reload
sudo systemctl enable INA226VoltAndCurrent_single.service

cat << EOS
=========================================
setup successful!

please 

"sudo systemctl start INA226VoltAndCurrent_single.service" 
or 
reboot

=========================================
EOS