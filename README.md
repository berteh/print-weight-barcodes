# mode kiosk

Keep the app running via a custom systemd service : from https://superuser.com/a/1128905

either use the provided script that will configure and start the service: 

    ./install_as_user_service.sh

or do it manually for a finer understanding :

- edit script-dir in TareKiosk.service
- cp TareKiosk.service $HOME/.config/systemd/user/TareKiosk.service
- systemctl --user daemon-reload
- systemctl --user enable TareKiosk.service
- systemctl --user start TareKiosk.service


see service status at

    systemctl --user status TareKiosk.service 

stop service at

    systemctl --user stop TareKiosk.service