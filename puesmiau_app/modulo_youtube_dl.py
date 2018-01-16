#!/usr/bin/env python3
from __future__ import unicode_literals
import gi
import youtube_dl
from gi.repository import GLib


class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

class propiedades_cancion():
	info=''
	def extraer_propiedades(self,url,ydl_opts):		
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			self.info = ydl.extract_info(url, download=False)
			
	def retorna_duracion(self):
		return self.info['duration']
	def retorna_titulo(self):
		return self.info['title']
	def retorna_descripcion(self):
		return self.info['description']
	def retorna_licencia(self):
		return self.info['license']
	def retorna_thumbnail(self):
		return self.info['thumbnail']
	def retorna_likes(self):
		return self.info['like_count']
	def retorna_dislikes(self):
		return self.info['dislike_count']
	def retorna_view(self):
		return self.info['view_count']
	def retorna_creador(self):
		return self.info['creator']

class modulo_descarga():
	def descargar_url(self,url,ydl_opts):
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([url])
		return False
		
"""print(info['filesize'])"""

"""def my_hook(d):
	if d['status'] not in ('downloading', 'finished'):
		return
	if d['status'] == 'finished':
		print('Done downloading, now converting ...')
	percent = float(d['downloaded_bytes'])/float(d['total_bytes']) * 100.0
	print(percent)"""
