#!/bin/bash
set -euxo pipefail

HOME_DIR="${HOME}"

if [ -e $HOME_DIR/.config/systemd/user/INA226VoltAndCurrent_twin.service ]; then
	systemctl --user disable INA226VoltAndCurrent_twin.service
fi

sudo ln -s $HOME_DIR/INA226_Library/service_files/INA226VoltAndCurrent_twin.service $HOME_DIR/.config/systemd/user/INA226VoltAndCurrent_twin.service
systemctl --user daemon-reload
systemctl --user enable INA226VoltAndCurrent_twin.service

cat << EOS
=========================================
setup successful!

please 

"systemctl --user start INA226VoltAndCurrent_twin.service" 
or 
"systemctl --user restart INA226VoltAndCurrent_twin.service" 
or
reboot

=========================================
EOS
