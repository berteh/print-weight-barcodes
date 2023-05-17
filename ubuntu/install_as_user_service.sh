#!/bin/bash -xv
# run this bash from the print-weight-barcode directory, not the ubuntu subdirectory.

mkdir -p $HOME/.config/systemd/user/
while read line; do   # Replace all instances on line of script-dir with $PWD
   echo ${line//script-dir/$PWD}
done < TareKiosk.service > $HOME/.config/systemd/user/TareKiosk.service
systemctl --user daemon-reload
systemctl --user enable TareKiosk.service
#systemctl --user start TareKiosk.service

cp ubuntu/S*.desktop $(xdg-user-dir DESKTOP)
mkdir $HOME/.config/autostart/
cp ubuntu/'Tare Kiosk.desktop' $HOME/.config/autostart/
