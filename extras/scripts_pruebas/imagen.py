import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf
from urllib.request import urlopen
from gi.repository import Gio 

window = Gtk.Window()
window.connect("delete-event", Gtk.main_quit)


url = 'https://t1.ea.ltmcdn.com/es/images/7/1/2/img_cuidados_de_gatos_cachorros_21217_600.jpg'
response = urlopen(url)
input_stream = Gio.MemoryInputStream.new_from_data(response.read(), None) 
pixbuf = Pixbuf.new_from_stream(input_stream, None) 
image = Gtk.Image() 
image.set_from_pixbuf(pixbuf)


window.add(image)
window.show_all()
Gtk.main()
