# mode kiosk

Keep the app running via a custom systemd service : (from https://superuser.com/a/1128905)

- edit <username> and script path in TareKiosk.service
- cp TareKiosk.service /home/$USER/.config/systemd/user/TareKiosk.service
- systemctl --user daemon-reload
- systemctl --user enable TareKiosk.service
- systemctl --user start TareKiosk.service


see service status at

    systemctl --user status TareKiosk.service 

stop service at

    systemctl --user stop TareKiosk.service