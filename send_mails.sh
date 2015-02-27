#/bin/bash
cd /var/www/vhosts/matricula-eide.es/MatriculaEIDE 
. ./bin/activate
./manage.py send_mail >> ./send_mail.log 2>&1
