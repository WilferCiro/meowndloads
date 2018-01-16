#Aún no funciona...
from setuptools import find_packages, setup
import os

files = ["ui/*"]
with open("README", 'r') as f:
    long_description = f.read()
datafiles = []
datafiles.append(('share/pixmaps', ['data/meowndloads.png']))
datafiles.append(('share/applications', ['data/Meowndloads.desktop']))

setup(name = "Meowndloads",
	version = "0.1",
	description = "Aplicación utilizada para descargar videos desde internet, principalmente desde youtube",
	author = "Wilfer Daniel Ciro Maya",
	author_email = "wilcirom@gmail.com",
	url = "https://wilferciro.github.io/puesmiau.github.io/index.html",
	license = "GPLv3",	
	
	packages = ['meowndloads_app'],
	
	package_data = {'meowndloads_app' : files },
	
	scripts = ["meowndloads"],
	long_description = long_description,
	requires = ['os', 'urllib', 'gi', 'Notify'],
	data_files = datafiles,
	py_modules = ['meowndloads_app'],
	   
) 
