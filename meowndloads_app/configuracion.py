#!/usr/bin/env python3
from gi.repository import GLib
import shelve
import os, errno

class configuracion():
	directorio = GLib.get_user_config_dir()+"/meowndloads/"
	archivo = "configuracion"
	def __init__(self):
		if not os.path.isfile(self.directorio+self.archivo):
			self.crear_inicial()
	
	def crear_inicial(self):
		try:
			os.makedirs(self.directorio)
			self.configuracion_defecto()
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise
		print('creador')
	
	def abrir_archivo_configuracion(self):
		if not os.path.isfile(self.directorio+self.archivo):
			self.crear_inicial()
		d = shelve.open(self.directorio+self.archivo)
		return d
	def configuracion_defecto(self):
		d = self.abrir_archivo_configuracion()
		d['descargas_dir'] = GLib.get_user_special_dir(GLib.USER_DIRECTORY_DOWNLOAD)
		d['usuario_youtube'] = ''
		d['contrasena_youtube'] = ''
		d['guarda_cache'] = False
		d['iniciar_sesion_youtube'] = False
		d['Mostrar_Notificacion'] = True
		d.close()
	
	def devuelve_descargas_dir(self):
		try:
			d = self.abrir_archivo_configuracion()
			directorio_descargas = d['descargas_dir']
			d.close()
		except:
			directorio_descargas = GLib.get_user_special_dir(GLib.USER_DIRECTORY_DOWNLOAD)
		return directorio_descargas
	
	def devuelve_usuario_youtube(self):
		try:
			d = self.abrir_archivo_configuracion()
			usuario_youtube = d['usuario_youtube']
			d.close()
		except:
			usuario_youtube = ''
		return usuario_youtube
	
	def devuelve_guarda_cache(self):
		try:
			d = self.abrir_archivo_configuracion()
			guarda_cache = d['guarda_cache']
			d.close()
		except:
			guarda_cache = True
		return guarda_cache
	
	def existe_contrasena_youtube(self):
		try:
			d = self.abrir_archivo_configuracion()
			contrasena_youtube = d['contrasena_youtube']
			d.close()
		except:
			contrasena_youtube = ''
		if contrasena_youtube!='':
			return True
		else:
			return False
	def devuelve_contrasena_youtube(self):
		try:
			d = self.abrir_archivo_configuracion()
			contrasena_youtube = d['contrasena_youtube']
			d.close()
		except:
			contrasena_youtube = ''
		return contrasena_youtube
	
	def devuelve_inicia_sesion_youtube(self):
		try:
			d = self.abrir_archivo_configuracion()
			iniciar_sesion_youtube = d['iniciar_sesion_youtube']
			d.close()
		except:
			iniciar_sesion_youtube = False
		return iniciar_sesion_youtube
	
	def devuelve_muestra_notificacion(self):
		try:
			d = self.abrir_archivo_configuracion()
			Mostrar_Notificacion = d['Mostrar_Notificacion']
			d.close()
		except:
			Mostrar_Notificacion = False
		return Mostrar_Notificacion
		
	def crear_cache(self):
		try:
			os.makedirs(self.directorio+"cache/")
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise
		print('creador')
		
	def devuelve_directorio_cache(self):
		if not os.path.isfile(self.directorio+"cache/cache.txt"):
			self.crear_cache()
		return self.directorio+"cache/cache.txt"
	
	def guarda_configuracion(self,directorio_descarga,usuario_youtube,contrasena_youtube,guarda_cache,iniciar_sesion_youtube,Mostrar_Notificacion):
		d = self.abrir_archivo_configuracion()
		d['descargas_dir'] = directorio_descarga
		d['usuario_youtube'] = usuario_youtube
		d['guarda_cache'] = guarda_cache
		d['iniciar_sesion_youtube'] = iniciar_sesion_youtube
		d['Mostrar_Notificacion'] = Mostrar_Notificacion		
		if contrasena_youtube!='':
			d['contrasena_youtube'] = contrasena_youtube
		d.close()

