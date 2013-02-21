from django.core.handlers.wsgi import WSGIHandler

import pinax.env


# setup the environment for Django and Pinax
pinax.env.setup_environ(__file__)

#import MatriculaEIDE.monitor
#MatriculaEIDE.monitor.start(interval=1.0)

def application(environ, start_response):
    status = '200 OK'

    if not environ['mod_wsgi.process_group']:
      output = 'EMBEDDED MODE'
    else:
      output = 'DAEMON MODE'

    response_headers = [('Content-Type', 'text/plain'),
                        ('Content-Length', str(len(output)))]

    start_response(status, response_headers)

    return [output]

# set application for WSGI processing
application = WSGIHandler()

