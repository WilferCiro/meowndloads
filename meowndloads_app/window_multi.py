#!/usr/bin/env python3
"""
Al o los que vean esto, disculpen por el desorden :3
si tienen dudas o quieren hacer aportes, les agradecería muchísimo wilcirom@gmail.com
"""

from __future__ import unicode_literals
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, Gdk, Gio, GLib
from gi.repository.GdkPixbuf import Pixbuf
from urllib.request import urlopen
from modulo_youtube_dl import propiedades_cancion, modulo_descarga
from configuracion import configuracion
import threading
from tipo_url import tipo_url
import math
from gi.repository import Notify
import os

Notify.init("Meowndloads")

error_logger = None
texto_thread = ''
estado_logger = ''
descargando_playlist = False
thread_playlist_descargada = 0
class Gui():
	thread = None
	clipboard=Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
	builder = Gtk.Builder()
	URL_actual = ''
	max_descargas = 3 # Oscilar entre 3, 2 y 1
	ruta_app = os.path.dirname(os.path.abspath(__file__))+'/'
	class estados():
		INICIAL = 0
		REC_INFO_IN = 1
		REC_INFO_FIN = 2
		PROC_VIDEO = 3
		INICIA_DESCARGA = 4
		DESCARGANDO = 5
		FIN_DESCARGA = 6
		ERROR_DESCARGA = 7
		ERROR_URL = 8
	class tipo_descarga():
		INDIVIDUAL = 0
		PLAYLIST = 1
	
	config = configuracion()
	prop_can = propiedades_cancion()
	m_desc = modulo_descarga()
	
	actual_estado = estados.INICIAL
	anterior_estado = None
	actual_tab = 'Audio'
	actual_tipo_url = None
	actual_titulo_cancion = ''
	
	cantidad_descargando = 0
	
	threads_arreglo = ['','','']
	video_descargando  = ['','','']
	propiedades  = ['','','']
	progresos  = [0,0,0]
	es_playlist = [False,False,False]
	
	def organizar_estados(self,indice_descarga = 0):
		global estado_logger
		estado_logger = self.actual_estado
		print('Organizar estados')
		btn_url = self.builder.get_object("AceptarURLBtn")
		operacion_actual_label = self.builder.get_object("accion_actual")
		window_descargando = self.builder.get_object("descargando_window")
		progreso = self.builder.get_object("descargando_bar{0}".format(str(indice_descarga)))
		label_url = self.builder.get_object("LabelURLPropiedades")
		propiedades_descarga = self.builder.get_object("propiedades_descarga{0}".format(str(indice_descarga)))
		page_num = self.builder.get_object("Tabs_Seleccion_Formato").get_current_page()
		if (self.actual_tipo_url==self.tipo_descarga.PLAYLIST and page_num!=2) or (self.actual_tipo_url!=self.tipo_descarga.PLAYLIST and page_num==2) or self.URL_actual=='' or self.cantidad_descargando >= self.max_descargas:
			estado_poner = False 
		else:
			estado_poner = True
		if self.actual_estado is self.estados.INICIAL:
			self._boton_descarga.set_sensitive(estado_poner)
			self._boton_descarga.set_label('Descargar '+self.actual_tab+'  '+self.actual_titulo_cancion)
			operacion_actual_label.set_label('No hay operaciones...')
			propiedades_descarga.set_label('Nada a realizar...')
			"""progreso.set_fraction(0)"""
			btn_url.set_sensitive(True)
		elif self.actual_estado is self.estados.REC_INFO_IN:
			self._boton_descarga.set_sensitive(estado_poner)
			btn_url.set_sensitive(False)
			operacion_actual_label.set_label('Obteniendo información del video (puede descargar)...')
			self._boton_descarga.set_label('Descargar '+self.actual_tab+' (Obteniendo info. del video)')
			if self.actual_tipo_url is self.tipo_descarga.INDIVIDUAL:
				label_url.set_label('URL correcta (Tipo individual)')
			else:
				label_url.set_label('URL correcta (Tipo playlist)')
		elif self.actual_estado is self.estados.REC_INFO_FIN:
			self._boton_descarga.set_sensitive(estado_poner)
			self._boton_descarga.set_label('Descargar '+self.actual_tab+' - '+self.actual_titulo_cancion)
			operacion_actual_label.set_label('Detalles obtenidos con éxito, puede verlos en Detalles')
			btn_url.set_sensitive(True)
		elif self.actual_estado is self.estados.PROC_VIDEO:
			self._boton_descarga.set_sensitive(False)
			self._boton_descarga.set_label('Procesando información, sea paciente')
			btn_url.set_sensitive(False)
		elif self.actual_estado is self.estados.INICIA_DESCARGA:
			self.actual_estado = self.estados.DESCARGANDO
			self._boton_descarga.set_sensitive(estado_poner)
			self._boton_descarga.set_label('Descargar '+self.actual_tab+' - '+self.actual_titulo_cancion)
			window_descargando.show()
			progreso.set_fraction(0)
			self.organizar_estados(indice_descarga)
			btn_url.set_sensitive(True)
		elif self.actual_estado is self.estados.DESCARGANDO:
			self._boton_descarga.set_sensitive(estado_poner)
			self._boton_descarga.set_label('Descargar '+self.actual_tab+' - '+self.actual_titulo_cancion)
			operacion_actual_label.set_label('Descargando...')
			btn_url.set_sensitive(True)
		elif self.actual_estado is self.estados.FIN_DESCARGA:
			if self.video_descargando[indice_descarga] == '':
				self.video_descargando[indice_descarga] = 'Archivo'
			self._boton_descarga.set_sensitive(False)
			self._boton_descarga.set_label('Descargar '+self.actual_tab+' - '+self.actual_titulo_cancion)
			operacion_actual_label.set_label('Fin de descarga del archivo '+self.video_descargando[indice_descarga])
			progreso.set_fraction(100)
			propiedades_descarga.set_label('Descarga Terminada...')
			if self.config.devuelve_muestra_notificacion()==True:
				Notify.Notification.new(
					"Descarga terminada!",
					"El archivo "+self.video_descargando[indice_descarga]+" \nse ha descargado con éxito",
					"dialog-information" # dialog-warn, dialog-error
				).show()
			GLib.timeout_add(2000,self.volver_estado_inicial,indice_descarga)
			self.poner_historial(self.video_descargando[indice_descarga])
			btn_url.set_sensitive(True)
		elif self.actual_estado is self.estados.ERROR_DESCARGA:
			self._boton_descarga.set_sensitive(True)
			if self.anterior_estado == self.estados.REC_INFO_IN:
				self._boton_descarga.set_label('Descargar '+self.actual_tab+' - Error obteniendo Título')
			else:
				self._boton_descarga.set_label('Descargar '+self.actual_tab+' - '+self.actual_titulo_cancion)
			operacion_actual_label.set_label('Hubo un error en la descarga, compruebe su conexión')
			progreso.set_fraction(0)
			btn_url.set_sensitive(True)
		elif self.actual_estado is self.estados.ERROR_URL:
			self._boton_descarga.set_sensitive(False)
			self._boton_descarga.set_label('Descargar '+self.actual_tab+' - '+self.actual_titulo_cancion)
			operacion_actual_label.set_label('Error en la URL')
			label_url.set_label('URL incorrecta, compruebe sus datos')
			btn_url.set_sensitive(True)
		self.anterior_estado = self.actual_estado
		
	def organiza_estados_idle(self):
		global error_logger
		global texto_thread,descargando_playlist,thread_playlist_descargada
		operacion_actual_label = self.builder.get_object("accion_actual")
		if self.actual_estado is self.estados.REC_INFO_IN:
			try:
				operacion_actual_label.set_label('Recopilando detalles, '+texto_thread)
			except:
				operacion_actual_label.set_label('Recopilando detalles')
		elif self.actual_estado is self.estados.PROC_VIDEO:
			try:
				operacion_actual_label.set_label(texto_thread)
			except Exception as e:
				operacion_actual_label.set_label('Obteniendo datos de la descarga...')
		if error_logger != None and error_logger != '':			
			if self.actual_estado is self.estados.DESCARGANDO:
				indice = self.threads_arreglo.index(error_logger)
				self.termina_descarga_forzada(indice)
			if self.actual_estado is self.estados.REC_INFO_IN:
				self.builder.get_object("loading_detalles").stop()
				self.builder.get_object("LabelPropiedadesCarga").set_label('Error al obtener los detalles, vuelva a intentarlo')
			self.actual_estado = self.estados.ERROR_DESCARGA
			self.organizar_estados()
			error_logger = None
		if (texto_thread.find('Extracting video information')!=-1 or texto_thread.find('Downloading js player')!=-1) and self.actual_estado==self.estados.REC_INFO_IN:
			if self.cantidad_descargando > 0:
				self.actual_estado = self.estados.DESCARGANDO
			else:
				self.actual_estado = self.estados.REC_INFO_FIN
			self.organizar_estados()
		if thread_playlist_descargada != 0:			
			indice = self.threads_arreglo.index(thread_playlist_descargada)
			self.termina_descarga_forzada(indice)
			self.actual_estado = self.estados.FIN_DESCARGA
			descargando_playlist = False
			self.organizar_estados()
			texto_thread = ''
			thread_playlist_descargada = 0
		if texto_thread==':3puesmiau:3':
			texto_thread = ':3puesmiau:3Nuevo'
			self.actual_estado = self.estados.INICIA_DESCARGA
			self.organizar_estados()
		for x in range(0, 3):
			if self.propiedades[x] != '':
				_propiedades_descarga = self.builder.get_object("propiedades_descarga{0}".format(str(x)))		
				_propiedades_descarga.set_label(self.propiedades[x])
				_bar = self.builder.get_object("descargando_bar{0}".format(str(x)))
				_bar.set_fraction(self.progresos[x])
		
		return True
	def termina_descarga_forzada(self,indice):
		self.builder.get_object("box_carga{0}".format(str(indice))).set_visible(False)
		self.builder.get_object("propiedades_descarga{0}".format(str(indice))).set_visible(False)
		self.threads_arreglo[indice] = ''
		self.video_descargando[indice] = ''
		self.propiedades[indice] = 'Nada para hacer...'
		self.progresos[indice] = 0
		self.es_playlist[indice] = False
		self.cantidad_descargando = self.cantidad_descargando - 1
		
	def volver_estado_inicial(self,indice_descarga):	
		if self.cantidad_descargando > 0:
			self.actual_estado = self.estados.DESCARGANDO
		else:
			self.actual_estado = self.estados.INICIAL
		if self.es_playlist[indice_descarga] == False:
			self.builder.get_object("box_carga{0}".format(str(indice_descarga))).set_visible(False)
			self.builder.get_object("propiedades_descarga{0}".format(str(indice_descarga))).set_visible(False)
		else:
			self.video_descargando[indice_descarga] = 'Playlist'
		self.organizar_estados(indice_descarga)
	
	def poner_historial(self,cancion):
		label = Gtk.Label('Descarga: '+str(cancion))
		self.builder.get_object("BoxHistorial").pack_start(label,True,True,0)
		label.show()
	
	def cierraVentana(self, *args):
		Gtk.main_quit(*args)

	def pegar_texto_btn(self,*args):
		editor = self.builder.get_object("URL_Principal")
		text = self.clipboard.wait_for_text()
		if text != None:
			editor.set_text(text)
		else:
			self.builder.get_object("LabelURLPropiedades").set_label('No hay texto a pegar')		

	def borrar_texto_btn(self,*args):
		editor = self.builder.get_object("URL_Principal")
		editor.set_text('')
	
	def cambio_pagina(self,widget,pagena,page_num,*args):
		if page_num==0:
			self.actual_tab = 'Audio'
		elif page_num == 1:
			self.actual_tab = 'Video'
		elif page_num == 2:
			self.actual_tab = 'Playlist'
		else:
			self.actual_tab = 'None'
		self.organizar_estados()
		if (self.actual_tipo_url==self.tipo_descarga.PLAYLIST and page_num!=2) or (self.actual_tipo_url!=self.tipo_descarga.PLAYLIST and page_num==2) or self.URL_actual=='' or self.cantidad_descargando >= self.max_descargas:
			self._boton_descarga.set_sensitive(False)
		else:
			self._boton_descarga.set_sensitive(True)
	
	def AceptarURLBtn(self,*args):
		self.propiedades_vacias()
		self.actual_titulo_cancion = ''
		forzar_a = self.builder.get_object("preferencias_url").get_active_text()
		tabs = self.builder.get_object("Tabs_Seleccion_Formato")
		editor = self.builder.get_object("URL_Principal")
		self.URL_actual = editor.get_text().strip()
		self.URL_actual = tipo_url.corrige_url(self.URL_actual,forzar_a)
		editor.set_text(self.URL_actual)
		if tipo_url.es_valido(self.URL_actual):
			self.builder.get_object("Url_visualizador").set_label(self.URL_actual)
			self.actual_estado = self.estados.REC_INFO_IN
			if tipo_url.es_playlist(self.URL_actual):
				self.carga_propiedades_playlist()
				tabs.set_current_page(2)
				self.actual_tipo_url = self.tipo_descarga.PLAYLIST
			else:
				self.thread = threading.Thread(
					    target=self.carga_propiedades_individual,
					    args=()
				)
				self.thread.daemon = True
				try:
					self.thread.start()
				except:
					print('Error en Thread')
					self.actual_estado = self.estados.ERROR_DESCARGA
					self.organizar_estados()
				self.actual_tipo_url = self.tipo_descarga.INDIVIDUAL
		else:
			self.builder.get_object("Url_visualizador").set_label('No hay URL válida')
			self.actual_estado = self.estados.ERROR_URL
		self.organizar_estados()
	
	class MyLoggere(object):
		def debug(self, msg):
			global texto_thread,estado_logger,descargando_playlist,thread_playlist_descargada
			if msg.find('Finished downloading playlist')!=-1:
				thread_playlist_descargada = threading.current_thread().ident
			if msg.find('[download]')==-1:
				texto_thread = msg
			elif texto_thread.find(':3puesmiau:3')==-1 and msg.find('[download]')!=-1 and (estado_logger == 3 or descargando_playlist == True):
				texto_thread = ':3puesmiau:3'
			if msg.find('error.URLError')!=-1:
				global error_logger
				error_logger = threading.current_thread().ident
			print('Debug: '+msg)

		def warning(self, msg):
			#global logger_mensaje
			#logger_mensaje = msg
			pass

		def error(self, msg):
			global error_logger
			error_logger = threading.current_thread().ident
			print('Error: '+msg)
	
	def carga_propiedades_individual(self):
		print('Inicia Thread')
		ydl_opts = {
			'format': 'bestvideo+bestaudio/best',
			'logger': self.MyLoggere(),
		}
		self.builder.get_object("loading_detalles").start()
		self.builder.get_object("LabelPropiedadesCarga").set_label('Cargando nueva información, este proceso puede tardar')
		self.prop_can.extraer_propiedades(self.URL_actual,ydl_opts)
		duracion=self.prop_can.retorna_duracion()
		self.builder.get_object("propiedades_duracion").set_label(self.tiempo_formato(duracion))
		self.builder.get_object("propiedades_titulo").set_label(str(self.prop_can.retorna_titulo()))
		self.builder.get_object("propiedades_descripcion").set_label(str(self.prop_can.retorna_descripcion()))
		self.builder.get_object("propiedades_likes").set_label(str(self.prop_can.retorna_likes()))
		self.builder.get_object("propiedades_dislikes").set_label(str(self.prop_can.retorna_dislikes()))
		self.builder.get_object("propiedades_view").set_label(str(self.prop_can.retorna_view()))
		self.builder.get_object("propiedades_autor").set_label('Autor: '+str(self.prop_can.retorna_creador())+', Licencia: '+str(self.prop_can.retorna_licencia()))
		self.actual_titulo_cancion = str(self.prop_can.retorna_titulo())
		#self.organizar_estados()
		#propiedades_imagen
		self.builder.get_object("loading_detalles").stop()
		self.builder.get_object("LabelPropiedadesCarga").set_label('Propiedades Video:')
		#TODO: Agregar excepción cuando se obtiene la imágen desde internet
		try:
			response = urlopen(str(self.prop_can.retorna_thumbnail()))
			input_stream = Gio.MemoryInputStream.new_from_data(response.read(), None) 
			pixbuf = Pixbuf.new_from_stream_at_scale(input_stream, 400, 400, True, None)
			self.builder.get_object("propiedades_imagen").set_from_pixbuf(pixbuf)
		except Exception as e:
			print('Error obteniendo Imágen')
			print(e)
			label = self.builder.get_object("LabelPropiedadesCarga")
			label.set_label(label.get_label()+' - Error al obtener la imagen')
		print('Fin propiedades')
		
	
	def carga_propiedades_playlist(self):
		global texto_thread
		self.builder.get_object("loading_detalles").start()
		self.builder.get_object("LabelPropiedadesCarga").set_label('Cargando, este proceso puede tardar')
		self.propiedades_vacias()
		self.builder.get_object("loading_detalles").stop()
		self.builder.get_object("LabelPropiedadesCarga").set_label('Propiedades Playlist:')
		self.actual_titulo_cancion = 'Playlist'
		texto_thread = 'Extracting video information Playlist'
		
	
	def propiedades_vacias(self):
		self.builder.get_object("propiedades_duracion").set_label('Duración')
		self.builder.get_object("propiedades_titulo").set_label('Título')
		self.builder.get_object("propiedades_descripcion").set_label('Descripción')
		self.builder.get_object("propiedades_likes").set_label('Likes')
		self.builder.get_object("propiedades_dislikes").set_label('DisLikes')
		self.builder.get_object("propiedades_view").set_label('Vistas')
		self.builder.get_object("propiedades_autor").set_label('Autor, Licencia')
		pixbuf = Pixbuf.new_from_file_at_scale (self.ruta_app+'ui/Music-icon.png', 300, 300, True)
		self.builder.get_object("propiedades_imagen").set_from_pixbuf(pixbuf)
	
	def tiempo_formato(self,segundos):
		if segundos/60 > 60:
			horas = int((segundos/60)/60)
			minutos = int((segundos/60)-(horas*60))
		else:
			horas=0
			minutos = int(segundos/60)
		segundos = segundos%60
		return str(horas).rjust(2, "0")+':'+str(minutos).rjust(2, "0")+':'+str(segundos).rjust(2, "0")
	
	
	def ver_preferencias(self,*args):
		self.builder.get_object("Preferencias_window").show()
	
	def cierra_preferencias(self,*args):
		self.builder.get_object("Preferencias_window").hide()
	
	def guardar_preferencias(self,*args):
		ruta =  self.builder.get_object("RutaGuardado").get_filename()
		usuario_youtube = self.builder.get_object("usuario_youtube").get_text()
		contrasena_youtube = self.builder.get_object("contrasena_youtube").get_text()
		guarda_cache = self.builder.get_object("guarda_cache").get_active()
		inicia_sesion_youtube = self.builder.get_object("iniciar_sesion_siempre").get_active()
		Mostrar_Notificacion = self.builder.get_object("Mostrar_Notificacion").get_active()
		self.config.guarda_configuracion(ruta,usuario_youtube,contrasena_youtube,guarda_cache,inicia_sesion_youtube,Mostrar_Notificacion)
		self.cierra_preferencias()
	
	def VerAcercaDe(self,*args):
		self.builder.get_object("AcercaDeVentana").run()
	
	def cierra_about(self,*args):
		self.builder.get_object("AcercaDeVentana").hide()
	
	
	
	def DescargarBtn_accion(self,*args):
		global descargando_playlist
		self.actual_estado = self.estados.PROC_VIDEO
		self.organizar_estados()
		if self.config.devuelve_guarda_cache()==True:
			cache =  self.config.devuelve_directorio_cache()
		else:
			cache = False
		
		if self.config.devuelve_inicia_sesion_youtube()==True:
			usaurio_youtube = self.config.devuelve_usuario_youtube()
			contrasena_youtube = self.config.devuelve_contrasena_youtube()
		else:
			usaurio_youtube = None
			contrasena_youtube = None

		if self.actual_tab == 'Audio':
			descarga_formato = self.builder.get_object("formato_audio").get_active_text()
			descarga_calidad = self.builder.get_object("calidad_audio").get_active_text().replace(' (Mejor)','').replace(' (Peor)','')
			descarga_subtitulos = self.builder.get_object("subtitulos_audio").get_active()
			descarga_thumbnail = self.builder.get_object("thumbnail_audio").get_active()
						
			self.ydl_opciones = {
				'format': 'bestaudio/best',
				'logger': self.MyLoggere(),
				'postprocessors': [{
					'key': 'FFmpegExtractAudio',
					'preferredcodec': descarga_formato,
					'preferredquality': descarga_calidad,
				}],
				'writesubtitles': descarga_subtitulos,
				'writethumbnail': descarga_thumbnail,
				'progress_hooks': [self.descargando_vista],
				'username': usaurio_youtube,
				'password': contrasena_youtube,
				'cachedir': cache,
				"outtmpl": self.config.devuelve_descargas_dir()+"/%(title)s.%(ext)s",
			}
			
			
		if self.actual_tab == 'Video':
			descarga_formato = self.builder.get_object("formato_video").get_active_text()
			descarga_calidad = self.builder.get_object("calidad_video").get_active_text().replace(' (Mejor)','').replace(' (Peor)','')
			descarga_thumbnail = self.builder.get_object("thumbnail_video").get_active()
			descarga_subtitulos = self.builder.get_object("subtitulos_video").get_active()
			
			self.ydl_opciones = {
				'format': descarga_calidad+'/best',
				'logger': self.MyLoggere(),
				'postprocessors': [{
					'key': 'FFmpegVideoConvertor',
					'preferedformat': descarga_formato,
				}],
				'writesubtitles': descarga_subtitulos,
				'writethumbnail': descarga_thumbnail,
				'progress_hooks': [self.descargando_vista],
				'username': usaurio_youtube,
				'password': contrasena_youtube,
				'cachedir': cache,
				"outtmpl": self.config.devuelve_descargas_dir()+"/%(title)s.%(ext)s",
			}
		
		if self.actual_tab == 'Playlist':
			descarga_formato = self.builder.get_object("formato_playlist").get_active_text()
			descarga_calidad = self.builder.get_object("calidad_playlist").get_active_text().replace(' (Mejor)','').replace(' (Peor)','')
			orden_descarga = int(self.builder.get_object("orden_playlist").get_active_id())
			desde_playlist = int(self.builder.get_object("desde_playlist").get_value())
			hasta_playlist = int(self.builder.get_object("hasta_playlist").get_value())
			if desde_playlist > hasta_playlist:
				auxiliar = hasta_playlist
				hasta_playlist = desde_playlist
				desde_playlist = auxiliar
			
			if desde_playlist == -1:
				desde_playlist = False				
			if hasta_playlist == -1:
				hasta_playlist = False
			random = False
			reversa = False
			print(orden_descarga)
			if orden_descarga in ('2',2):
				random == True
				print('Random')
			elif orden_descarga in ('1',1):
				print('Reversa')
				reversa = True
			if descarga_formato in ('3gp','mp4','flv','ogg','webm','mkv','avi'):
				self.ydl_opciones = {
					'format': 'bestaudio+bestvideo/best',
					'logger': self.MyLoggere(),
					'postprocessors': [{
						'key': 'FFmpegVideoConvertor',
						'preferedformat': descarga_formato,
					}],
					'progress_hooks': [self.descargando_vista],
					'username': usaurio_youtube,
					'password': contrasena_youtube,
					'cachedir': cache,
					'playlistreverse': reversa,
					'playlistrandom': random,
					'playliststart': desde_playlist,
					'playlistend': hasta_playlist,
					"outtmpl": self.config.devuelve_descargas_dir()+"/%(title)s.%(ext)s",
				}
			else:
				self.ydl_opciones = {
					'format': 'bestaudio/best',
					'logger': self.MyLoggere(),
					'postprocessors': [{
						'key': 'FFmpegExtractAudio',
						'preferredcodec': descarga_formato,
						'preferredquality': descarga_calidad,
					}],
					'progress_hooks': [self.descargando_vista],
					'username': usaurio_youtube,
					'password': contrasena_youtube,
					'cachedir': cache,
					'playlistreverse': reversa,
					'playlistrandom': random,
					'playliststart': desde_playlist,
					'playlistend': hasta_playlist,
					"outtmpl": self.config.devuelve_descargas_dir()+"/%(title)s.%(ext)s",
				}
			
		if self.cantidad_descargando < self.max_descargas:
			try:
				self.thread = threading.Thread(
						target=self.multi_descargar,
						args=()
				)
				self.thread.daemon = True
				self.thread.start()
				indice = None
				for x in range(0, 3):
					if self.threads_arreglo[x] == '' and indice == None:
						self.threads_arreglo[x] = self.thread.ident
						self.video_descargando[x] = self.actual_titulo_cancion
						self.propiedades[x] = 'Procesando {0}...'.format(self.actual_titulo_cancion)
						self.progresos[x] = 0
						indice = x
						self.poner_campo_descarga(self.thread.ident,indice)
						self.cantidad_descargando = self.cantidad_descargando + 1
						if self.actual_tab == 'Playlist':
							descargando_playlist = True		
							self.es_playlist[x] = True
						else:
							self.es_playlist[x] = False
						pass
			except Exception as e:
				print('Error al iniciar: '+str(e))
		else:
			dialog = Gtk.MessageDialog(self.builder.get_object("meowndloadsWindow"), 0, Gtk.MessageType.INFO,
			Gtk.ButtonsType.OK, "Sobrepasa el límite")
			dialog.format_secondary_text("No se pueden descargar maś de tres videos al tiempo.")
			dialog.run()
			dialog.destroy()
		
	def poner_campo_descarga(self,identif,indice):
		self.builder.get_object("box_carga{0}".format(str(indice))).set_visible(True)
		self.builder.get_object("propiedades_descarga{0}".format(str(indice))).set_visible(True)

	def multi_descargar(self):
		self.m_desc.descargar_url(self.URL_actual,self.ydl_opciones)
		
	
	def descargando_vista(self,d):
		if d['status'] not in ('downloading', 'finished','error'):
			return
		try:
			indice = self.threads_arreglo.index(threading.current_thread().ident)
		except:
			indice = 0
		if d['status'] == 'error':
			print('Error en: '+str(indice))
			return
		if d['status'] == 'finished':
			GLib.timeout_add(2000,self.terminar_descarga,indice)
			print('Terminado')
			return			
		#_bar = self.builder.get_object("descargando_bar{0}".format(str(indice)))
		#_propiedades_descarga = self.builder.get_object("propiedades_descarga{0}".format(str(indice)))		

		if d['status'] != 'finished':
			
			if float(d['total_bytes'])>0 and d['downloaded_bytes']!=None:
				percent = float(d['downloaded_bytes'])/float(d['total_bytes'])
			else:
				percent = 1
			#_bar.set_fraction(percent)
			self.progresos[indice] = percent
			
			try:
				if self.video_descargando[indice] == '' or (self.es_playlist[indice] == True and (self.video_descargando[indice] == 'Playlist' or self.video_descargando[indice] == '')):
					partes = d.get('filename').split('/')
					titulo = partes[len(partes)-1]
					self.video_descargando[indice] = titulo
				else:
					titulo = self.video_descargando[indice]
				titulo = self.video_descargando[indice]
			except Exception as e:
				titulo ='Descargando'
				print(e)
			progreso = self.organiza_bytes(int(d['downloaded_bytes']))+' / '+self.organiza_bytes(int(d['total_bytes']))
			try:
				velocidad = self.organiza_bytes(int(d.get('speed')))+'/s - '+self.tiempo_formato(int(d.get('eta')))+'s eta'
			except:
				velocidad = '--KiB/s'
			texto_descarga = titulo[0:30]+'...   '+progreso+'    '+velocidad
		self.propiedades[indice] = texto_descarga			
		#_propiedades_descarga.set_label(self.texto_descarga)
	
	def organiza_bytes(self,bits):
		arreglo = ['Bi','KiB','MB','GB','TB']
		retorna = bits
		indice = 0
		while retorna>1024:
			retorna = round((retorna / 1024),2) #TODO: cambiar por round(nro,2)
			indice = indice + 1
		return str(retorna)+' '+arreglo[indice]
	
	def terminar_descarga(self,indice):
		print('Hola Mundo')
		self.actual_estado = self.estados.FIN_DESCARGA
		self.organizar_estados(indice)
		if self.es_playlist[indice] == False:
			self.threads_arreglo[indice] = ''
			self.propiedades[indice] = 'Nada para hacer...'
			self.progresos[indice] = 0
			self.video_descargando[indice] = ''
			self.cantidad_descargando = self.cantidad_descargando - 1
		return False
	
	def descargando_cancel_accion(self,*args):
		#TODO: Organizar el stop
		print('Error, función no añadida aún')
	
	def __init__(self):
		#accion_actual
		self.builder.add_from_file(self.ruta_app+"ui/interfaz.ui")
				
		#Ventana Principal
		_window = self.builder.get_object("meowndloadsWindow")
		_window.connect("delete_event", self.cierraVentana)
		_window.set_default_size(930, 330)
		_window.set_position(Gtk.WindowPosition.CENTER)
		self._boton_descarga = self.builder.get_object("DescargarBtn")
		self._boton_descarga.connect("clicked", self.DescargarBtn_accion)
		self._boton_descarga.set_sensitive(False)
		self.builder.get_object("Tabs_Seleccion_Formato").connect("switch-page", self.cambio_pagina)
				
		#ventana acerca de...
		_acerca_de = self.builder.get_object("AcercaDeVentana")
		_acerca_de.connect("delete_event", self.cierra_about)
		
		#Ventana Detalles
		self.builder.get_object("loading_detalles").stop()
		
		#ventana URL		
		self.builder.get_object("PegarBtn").connect("clicked", self.pegar_texto_btn)		
		self.builder.get_object("BorrarBtn").connect("clicked", self.borrar_texto_btn)	
		self.builder.get_object("AceptarURLBtn").connect("clicked", self.AceptarURLBtn)
		
		#Menú de usuario
		self.builder.get_object("AcercaDe_boton").connect("clicked", self.VerAcercaDe)
		self.builder.get_object("Salir_Boton").connect("clicked", self.cierraVentana)
		self.builder.get_object("Preferencias_boton").connect("clicked", self.ver_preferencias)
		
		#ventana descarga
		self.builder.get_object("descargando_cancel").connect("clicked", self.descargando_cancel_accion)
		
		#Ventana Preferencias:
		_preferencias = self.builder.get_object("Preferencias_window")
		_preferencias.connect("delete_event", self.cierra_preferencias)
		_preferencias.set_position(Gtk.WindowPosition.CENTER)
		_preferencias.set_default_size(600, 200)
		self.builder.get_object("Guardar_preferencias").connect("clicked", self.guardar_preferencias)
		self.builder.get_object("Cancelar_preferencias").connect("clicked", self.cierra_preferencias)
		self.builder.get_object("RutaGuardado").set_filename(self.config.devuelve_descargas_dir())
		self.builder.get_object("usuario_youtube").set_text(self.config.devuelve_usuario_youtube())
		self.builder.get_object("guarda_cache").set_active(self.config.devuelve_guarda_cache())
		self.builder.get_object("iniciar_sesion_siempre").set_active(self.config.devuelve_inicia_sesion_youtube())
		self.builder.get_object("Mostrar_Notificacion").set_active(self.config.devuelve_muestra_notificacion())		
		if self.config.existe_contrasena_youtube():
			self.builder.get_object("label_contrasena").set_label('Contraseña (existente)')
		else:
			self.builder.get_object("label_contrasena").set_label('Contraseña (aún no existe)')
		
		#iniciar idle de ejecución de función
		GLib.timeout_add(1000,self.organiza_estados_idle)
		
		#esconder campos de descargar
		for x in range(0, 3):
			self.builder.get_object("box_carga"+str(x)).set_visible(False)
			self.builder.get_object("propiedades_descarga"+str(x)).set_visible(False)
			
		#Vaciar propiedades
		self.propiedades_vacias()
		
		#css
		style_provider = Gtk.CssProvider()
		css = open(self.ruta_app+'ui/estilo.css','rb')
		css_data = css.read()
		css.close()
		style_provider.load_from_data(css_data)
		Gtk.StyleContext.add_provider_for_screen(
			Gdk.Screen.get_default(), style_provider,     
			Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
		)
		_window.show_all()
		Gtk.main()

def start():
	print("aplicación Iniciada")
	gui = Gui()

if __name__ == "__main__":
	start()

# Thanks to <a href='http://dryicons.com/free-icons/music-icons'> Icon by Dryicons </a>


