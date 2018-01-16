#Aún no funciona...
from setuptools import find_packages, setup
import os

files = ["ui/*"]
with open("README", 'r') as f:
    long_description = f.read()
datafiles = []
datafiles.append(('share/pixmaps', ['data/puesmiau.png']))
datafiles.append(('share/applications', ['data/PuesMiau.desktop']))

setup(name = "Pues Miau",
	version = "0.1",
	description = "Aplicación utilizada para descargar videos desde internet, principalmente desde youtube",
	author = "Wilfer Daniel Ciro Maya",
	author_email = "wilcirom@gmail.com",
	url = "https://wilferciro.github.io/puesmiau.github.io/index.html",
	license = "GPLv3",	
	
	packages = ['puesmiau_app'],
	
	package_data = {'puesmiau_app' : files },
	
	scripts = ["puesmiau"],
	long_description = long_description,
	requires = ['os', 'urllib', 'gi', 'Notify'],
	data_files = datafiles,
	py_modules = ['puesmiau_app'],
	   
) 
