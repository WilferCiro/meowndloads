#!/usr/bin/env python3
class tipo_url():
	def corrige_url(url,forzar_a):
		if url.find('&list=')!=-1:
			partes = url.split('&list=')
			if forzar_a=='Playlist':
				url = 'https://www.youtube.com/playlist?list='+partes[1]
			else:
				url = partes[0]
		if url.find('&t=')!=-1:
			partes = url.split('&t=')
			url = partes[0]
			
		if url.find('?t=')!=-1:
			partes = url.split('?t=')
			url = partes[0]
		
		if url.find('&index=')!=-1:
			partes = url.split('&index=')
			url = partes[0]
		return url
	def es_valido(url):
		if url.find(" ")!=-1 or (url.startswith('https://www.youtube.com')==False and url.startswith('https://youtu.be/')==False and url.startswith('https://www.udemy.com/')==False):
			return False
		else:
			return True
	
	def es_playlist(url):
		if url.startswith('https://www.youtube.com/playlist?list=')==True or url.startswith('https://www.youtube.com/user/')==True or url.find("playlist")!=-1:
			return True
		else:
			return False
