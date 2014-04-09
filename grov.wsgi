#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/grov/")

from grov import app as application
application.secret_key = 't0h1e0s1k0i1e0s1a0w1a0i1t0'
