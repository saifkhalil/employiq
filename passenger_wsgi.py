import imp
import os
import sys


sys.path.insert(0, os.path.dirname(__file__))

wsgi = imp.load_source('wsgi', 'passenger_wsgi.py')
application = wsgi.application

# import importlib
# import os
# import sys
# import sys, os

# INTERP = "/home/vrgqyjmh92to/virtualenv/repositories/recruitment/3.7/bin/python"
# if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)
# from core.wsgi import application