#!/bin/bash -xv
# run this bash from the print-weight-barcode directory, not the ubuntu subdirectory.

systemctl --user stop TareKiosk.service
systemctl --user disable TareKiosk.service
rm $HOME/.config/systemd/user/TareKiosk.service

cd $(xdg-user-dir DESKTOP)
rm S*Kiosk.desktop
rm $HOME/.config/autostart/'Tare Kiosk.desktop'
