import logging

import bonobo_docker
import mondrian

mondrian.setup(excepthook=True)
logger = logging.getLogger(bonobo_docker.__name__)
