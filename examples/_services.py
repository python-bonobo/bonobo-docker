import bonobo
import os

def get_services():
    return {
        'fs': bonobo.open_fs(os.path.join(os.path.dirname(__file__), '.')),
    }
