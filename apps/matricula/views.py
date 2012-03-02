from django.contrib.auth.decorators import login_required, permission_required

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

@login_required
def imprimir_matricula(request, pk):
    logger.debug("Vamos a imprimir")
    return None
