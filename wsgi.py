from django.core.handlers.wsgi import WSGIHandler

import pinax.env


# setup the environment for Django and Pinax
pinax.env.setup_environ(__file__)

import MatriculaEIDE.monitor
MatriculaEIDE.monitor.start(interval=1.0)

# set application for WSGI processing
application = WSGIHandler()

