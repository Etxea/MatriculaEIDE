#!/bin/bash
source /var/www/vhosts/matricula-eide.es/MatriculaEIDE/bin/activate
/var/www/vhosts/matricula-eide.es/MatriculaEIDE/manage.py runserver > /var/www/vhosts/matricula-eide.es/MatriculaEIDE/server.log
