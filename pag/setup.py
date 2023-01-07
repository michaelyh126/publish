import py2exe
from distutils.core import setup

options = {"py2exe": {"excludes": ["arcpy"]}}
setup(console=['test.py'], options=options)