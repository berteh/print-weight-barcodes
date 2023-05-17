installation station de tare.

# OS

- installer xubuntu minimial LTS depuis clé usb, *avec autologin* pour l'utilisateur
- redémarrer
- ouvrir terminal: `win+t`

## applications complémentaires

    sudo apt-get install mousepad openssh-server system-config-printer cups nomacs gnome-system-tools
    sudo apt-get install cutecom minicom git python3-pip


## installation automatique des mises à jour de sécurité

Inutile sans connexion internet. [documentation détaillée](https://guide.ubuntu-fr.org/server/automatic-updates.html)

    sudo apt install unattended-upgrades

et vérifier/compléter le fichier de configuration de ces mises-à-jour:

    sudo mousepad /etc/apt/apt.conf.d/20auto-upgrades

qui doit contenir les lignes suivantes:

    APT::Periodic::Update-Package-Lists "1";
    APT::Periodic::Download-Upgradeable-Packages "1";
    APT::Periodic::AutocleanInterval "7";
    APT::Periodic::Unattended-Upgrade "1";


## logiciel du kioske de tare

[page d'infos](https://github.com/berteh/print-weight-barcodes). installation :

    cd && git clone --depth 1 https://github.com/berteh/print-weight-barcodes.git    

OU le copier depuis clé usb :

    cd && cp -r /media/balance1/writable/backup/print-weight-barcodes .

puis installer les librairies requises

    sudo apt-get install python3-tk python3-pil python3-pil.imagetk
    pip install pyserial pycups pyttk pyyaml pytest

 
## eventuellement éditeur de code correct

    wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/sublimehq-archive.gpg > /dev/null
    echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
    sudo apt-get update
    sudo apt-get install sublime-text


# droits d'acces port COM (balance)

    sudo gpasswd --add $USER dialout
    sudo gpasswd --add $USER tty

ou ajouter l'utilisateur aux groupes *dialout* et *tty* via GUI : `settings > Users and Groups > Manage Groups`: sélectionner les groupes et cocher l'utilisateur.

(nécéssite un redémarrage pour entrer en vigueur... mais continuer d'abord jusqu'au touchscreen)



# désactiver screensaver et powersave
`settings > Power Manager`

- display > disable
- general > do nothing
- system > security > decocher "lock screen when going to sleep"

`settings > Screen Saver`

- désactiver "enable screensaver" et "enable lock screen"


# touchscreen

    cd /media/balance1/writable/backup/eGTouch_v2.5.11703.L-x/
    sudo ./setup.sh 

OU télécharger le driver plus récent depuis https://www.eeti.com/drivers_Linux.html , et installer comme ci-dessus. typiquement:

    cd & wget https://www.eeti.com/touch_driver/Linux/20221114/eGTouch_v2.5.11703.L-x.tar.gz
    tar -xvf  eGTouch_v2.5.11703.L-x.tar.gz & cd eGTouch_v2.5.11703.L-x/
    sudo ./setup.sh    

Dans tous les cas, les premiers choix (par défauts) de configuration du driver sont les bons:
    [Y] Yes, I agree
    [1] RS232
    [Enter] key to continue
    (I) [N]
    (I) Default [1]

*Redémarrer*


# imprimante etiquettes

connecter par USB et démarrer l'imprimante.

ajouter une imprimante `RAW`  (! driver *Generic RAW queue* ou *Generic Text*, pas le driver Zebra): via `Settings > Printers`  ou `system-config-printer`

Add > Zebra (connected to USB) > Generic > Raw Queue

donner un nom court simple et unique, par exemple `zebra-raw-1`


## ou via ligne de commande

trouver l'adresse de l'imprimante :

    lpinfo -v | grep Zebra

creer la Queue (modifier l'adresse avec celle du résultat précédent) :

    lpadmin -p zebra-raw-1 -E -v usb://Zebra%20Technologies/ZTC%20ZD410-300dpi%20ZPL?serial=50J194404823 -m raw -o usb-unidir-default=true


# configuration et test du programme de Tare

modifier le fichier `config.yaml` pour renseigner les bonnes infos:

    /opt/sublime_text/sublime_text ~/print-weight-barcodes/config.yaml

- nom d'imprimante
- port de la/les balances
- configuration à 1 ou 2 stations sur le même écran

et éventuellement:
- image à utiliser pour le(s) bouton(s)

Tester le bon fonctionnement du script (les tests doivent tous réussir ou passer):

    cd ~/print-weight-barcodes/ & pytest


## éventuellement tester la communication depuis la balance manuellement

Eventuellement tester la bonne connection avec la balance, avec port : */dev/ttyS0*, baudrate : *9600* et control : *Software* :

    cutecom

(à exécuter avec `sudo` pour droits d'accès si avant redémarrage)

ou tester la communication balance via ligne de commande :  (pour quitter minicom: `ctrl+a  x`)

    minicom -b 9600 -D /dev/ttyS0 -c on -w

## éventuellement tester l'imprimante manuellement

Pour info un éditeur en ligne pour cette syntaxe d'étiquettes :
labelary.com/viewer.html

Il est facile d'imprimer directement le fichier ZPL:

    lpr -P zebra-raw-1 -o raw ~/print-weight-barcodes/labels-samples/label_ean-bravo_300dpi.zpl



# mode kiosk : assurer que le logiciel de tare reste toujours actif

Assure que l'application de tare tourne en permanence, adapté de https://superuser.com/a/1128905

    cd ~/print-weight-barcodes
    ubuntu/install_as_user_service.sh


Pour démarrer/arrêter ce service manuellement il faut cliquer sur les nouveaux raccourcis du bureau, ou exécuter :

    systemctl --user start TareKiosk.service
    systemctl --user stop TareKiosk.service


Pour vérifier l'état du service :

    systemctl --user status TareKiosk.service 


## Full screen ou pas

basculez en full-screen (impossible d'en sortir sans clavier) en modifiant la variable du script:

    mousepad ~/print-weight-barcodes/gui.py

    FULLSCREEN = True

et redémarrez le kiosk (simple alt+f4)
