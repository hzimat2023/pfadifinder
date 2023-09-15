#!/bin/bash

#Check ob das Script mit sudo-Rechten ausgeführt wird
if [ "$EUID" -ne 0 ]; then
        echo "Bitte dieses Script mit sudo-Rechten ausführen!!"
        echo "Tippe: sudo ./$0"
        echo "----------------------------------------------------------------"
        exit 1
fi


#Script-Variablen:
#--------------
echo "Das Script wird mit folgenden Variablen ausgeführt:"
#1. Pfad zum Git-Repo:
GIT_REPO=https://github.com/hzimat2023/pfadifinder
echo "1. Pfad zum Git-Repo:"
echo $GIT_REPO
#2. Pfad zum App-Ordner:
APP_FOLDER=./pfadifinder
echo "2. Pfad zum App-Ordner:"
echo $APP_FOLDER
#3. mysql-User:
MYSQL_USER=admin
echo "3. mysql-User:"
echo $MYSQL_USER
#4. mysql-PW:
export MYSQL_PW=pzsjh68sDfV5tmDY3GVs
echo "4. mysql-PW:"
echo $MYSQL_PW
#5. mysql-SECRET_KEY:
MYSQL_SECRET_KEY=iautayynxrpsrzumiautayynxrpsrzum
echo "5. mysql-SECRET_KEY:"
echo $MYSQL_SECRET_KEY
#6. mysql-DATABASE_URL:
MYSQL_DATABASE_URL=mysql+pymysql://admin:pzsjh68sDfV5tmDY3GVs@localhost:3306/pfadi
echo "6. mysql-DATABASE_URL:"
echo $MYSQL_DATABASE_URL
#7. mysql-database-name:
MYSQL_DATABASE_NAME=pfadi
echo "7. mysql-database-name:"
echo $MYSQL_DATABASE_NAME
#8. mysql-env-file:
MYSQL_ENV_FILE=.env
echo "8. mysql-env-file:"
echo $MYSQL_ENV_FILE
#9. gunicorn-config:
GUNICORN_CONFIG=/etc/supervisor/conf.d/pfadi.conf
echo "9. gunicorn-config:"
echo $GUNICORN_CONFIG
#10. Current-user:
echo "10. Current-user:"
echo $USER
#11. nginx-config:
NGNIX_CONFIG=pfadi
echo "11. nginx-config:"
echo $NGNIX_CONFIG
# 12. nginx-access_log:
NGNIX_ACCESS_LOG=pfadi_access.log
echo "12. nginx-access_log:"
echo $NGNIX_ACCESS_LOG
# 13. nginx-error_log
NGNIX_ERROR_LOG=pfadi_error.log
echo "13. nginx-error_log"
echo $NGNIX_ERROR_LOG

echo #--------------

#PAUSE
echo "Das Script wird mit oben stehenden Variablen ausgeführt:"
echo "Drücken Sie Enter, um fortzufahren."
read

#system Update, python & mysql-server Installation
#sudo
apt update && apt install python3 python3-venv python3-dev && apt install mysql-server supervisor nginx git && sudo apt upgrade
apt install python3-pip


cd /home/$USER

#PAUSE
echo "Wurde das System-Update erfolgreich durchgeführt?"
echo "Wenn ja, dann drücken Sie Enter, um fortzufahren."
read

#pwd /home/$USER
#GIT_REPO
#git clone https://github.com/hzimat2023/pfadifinder
git clone $GIT_REPO


#PAUSE
echo "Wurde das Git-Repository erfolgreich gedownloaded?"
echo "Wenn ja, dann drücken Sie Enter, um fortzufahren."
read

#APP_FOLDER
#cd $APP_FOLDER
cd $APP_FOLDER

#pwd $APP_FOLDER
rm -rf venv

python3 -m venv venv


#PAUSE
echo "Wurde die virtuelle Python Umgebung erstellt?"
echo "Wenn ja, dann drücken Sie Enter, um fortzufahren."
read

#Umgebung aktivieren
source venv/bin/activate

pip3 install -r requirements.txt

#PAUSE
pwd
echo "Wurden requirements installiert? (Abhängigkeiten)"
echo "Wenn ja, dann drücken Sie Enter, um fortzufahren."
read

#-----------
#Nur wenn fehler mit numphy
#(Ubuntu 20.04)
##nano requirements.txt
#delete "==1.25.2" in line (numpy==1.25.2)
##pip3 install -r requirements.txt
#-----------

#Installation von gunicorn, pymysql,  cryptography
pip3 install gunicorn pymysql cryptography


#PAUSE
echo "Wurden gunicorn pymysql cryptography installiert?"
echo "Wenn ja, dann drücken Sie Enter, um fortzufahren."
echo mariadb...?
read

#sudo
# mysql -u root

# SQL-Anweisungen, die Sie ausführen möchten
SQL_QUERY="create database pfadi character set utf8 collate utf8_bin; \
create user '$MYSQL_USER'@'localhost' identified by ''; \
grant all privileges on pfadi.* to '$MYSQL_USER'@'localhost'; \
flush privileges;"

# Verwenden Sie den mysql-Befehl mit -u und -p, um Benutzer und Passwort zu übergeben, und -e, um die SQL-Anweisungen direkt auszuführen.
# Die Option -e wird verwendet, um die SQL-Anweisungen nacheinander auszuführen.
mysql -u$MYSQL_USER -p$MYSQL_PASSWORD -e $SQL_QUERY

# Beenden Sie die MySQL-Shell
mysql -u$MYSQL_USER -p$MYSQL_PASSWORD -e exit

#PAUSE
echo "Wurden mysql Database erstellt?"
echo "Wenn ja, dann drücken Sie Enter, um fortzufahren."
read


#mysql-SECRET_KEY
#mysql-DATABASE_URL
#mysql-env-file
#Datei .env erstellen
#(über prüfen mit cat .env)
# nano .env
#Inhalt einfügen:
echo "SECRET_KEY=$MYSQL_SECRET_KEY" > $MYSQL_ENV_FILE
echo "DATABASE_URL=$MYSQL_DATABASE_URL" >> $MYSQL_ENV_FILE

#PAUSE
echo "Wurden mysql env Datei erstellt?"
echo "Wenn ja, dann drücken Sie Enter, um fortzufahren."
read

#DATENBANK-TABELLEN ERZEUGEN
flask db upgrade

#mysql-User
#mysql-PW
mysql -u $MYSQL_USER -p$MYSQL_DATABASE_NAME -p$MYSQL_PASSWORD < backup.sql
# output:
# Enter password: 
#pw:

#-----------
#Backup erstellen (optional):
#sudo
##mysqldump -u admin -p  pfadi > backup.sql
# output:
#Enter password: 
#pw:
##pzsjh68sDfV5tmDY3GVs
#optional:
#sudo
##mysqldump -u root  pfadi > backup.sql
#-----------

#KONFIGURATION VON GUNICORN UND SUPERVISOR XXX = Applikationsname

#9. gunicorn-config-file (pfadi.conf)
#2. Pfad zum App-Ordner: ($APP_FOLDER)
#10. Current-user (social_yesod)
# sudo nano /etc/supervisor/conf.d/pfadi.conf
#Inhalt einfügen:
touch > $GUNICORN_CONFIG
cat <<EOF > $GUNICORN_CONFIG
[program:$NGNIX_CONFIG]
command=$APP_FOLDER/venv/bin/gunicorn -b localhost:8000 -w 4 app:app
directory=$APP_FOLDER
user=$USER
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
EOF

#PAUSE
echo "Wurden ginicorn-config Datei erstellt?"
echo "Wenn ja, dann drücken Sie Enter, um fortzufahren."
read

#sudo
supervisorctl reload

mkdir certs
#openssl Zertifikat erstellen (selbst signiert)
yes "" | openssl req -new -newkey rsa:4096 -days 365 -nodes \
-x509 -keyout certs/key.pem -out certs/cert.pem

#!!!!!
#output alles mit Enter bestätigen...(yes "" | )


#PAUSE
echo "Wurden openssl Zertifikat erstellt?"
echo "Wenn ja, dann drücken Sie Enter, um fortzufahren."
read

echo "export FLASK_APP=app.py" >> ~/.profile


#sudo
rm /etc/nginx/sites-enabled/default

#11. nginx-config-file (/etc/nginx/sites-enabled/pfadi)
#2. Pfad zum App-Ordner:
# 12. nginx-access_log (/var/log/pfadi_access.log)
# 13. nginx-error_log
#sudo nano /etc/nginx/sites-enabled/pfadi
#Inhalt einfügen:
touch > /etc/nginx/sites-enabled/$NGNIX_CONFIG
cat <<EOF > /etc/nginx/sites-enabled/$NGNIX_CONFIG
server {
    # Für Requests auf Port 80 (http)
    listen 80;
    server_name _;

    location / {
        # Redirect von http-Requests an die gleiche URL, aber per https
        return 301 https://$host$request_uri;
    }
}

server {
    # Für Requests auf Port 443 (https)
    listen 443 ssl;
    server_name _;

    # Speicherort des SSL-Zertifikats und des Schlüssels
    ssl_certificate $APP_FOLDER/certs/cert.pem;
    ssl_certificate_key $APP_FOLDER/certs/key.pem;

    # Zugriffs- und Fehlerlogs sollen in /var/log geschrieben werden
    access_log /var/log/$NGNIX_ACCESS_LOG;
    error_log /var/log/$NGNIX_ERROR_LOG;

    location / {
        # Weitergabe von Requests an Gunicorn
        proxy_pass http://localhost:8000;
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
EOF


#PAUSE
echo "Wurde Ngnix-Cinfig Datei erstellt?"
echo "Wenn ja, dann drücken Sie Enter, um fortzufahren."
read

    
#sudo
supervisorctl reload

#sudo
supervisorctl status

#sudo
systemctl restart nginx

#sudo
service nginx reload

systemctl status nginx.service


#PAUSE
echo "Wurde Ngnix neugestartet?"
echo "Wenn ja, dann drücken Sie Enter, um fortzufahren."
read

#PAUSE
echo "Ende vom Script, drücken Sie Enter, um fortzufahren."
read
