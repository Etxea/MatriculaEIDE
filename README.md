MatriculaEIDE
============
Este es un pequeño programa para gestionar las matriculas a los examenes de cambridge ofertados por el centro EIDE (http://eide.es)


Install
-------

```
git clone git@github.com:jonlatorre/MatriculaEIDE.git
cd MatriculaEIDE
virtualenv .
. bin/activate
sudo apt-get install libjpeg-dev
pip install -r requirements.txt
echo "SITE_ROOT='$(pwd)'" > matriculas/local_settings.py
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

Run in Docker
------

```
docker build . -t me
docker run -d -p 8000:8000 me
x-www-browser http://localhost:8000
```

Author
------

 - Jon Latorre Martinez <jonlatorremartinez@gmail.com>

License
-------
