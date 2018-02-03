import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from pydub import AudioSegment
sound = AudioSegment.from_file("/home/ciro/Documentos/EDEQ/Juego2/sprites/sonidos/pop.mp3", format="mp3")
samples = np.array(sound.get_array_of_samples())*0.001
print (len(samples))

pa = patches.Rectangle(
	(0.1, 0.1),   # (x,y)
	len(samples), # width
	100,          # height
	alpha=0.2
)

pos1 = 0
pos2 = len(samples)
actual_barra = 0

class DraggableRectangle:	
	nu = None
	def __init__(self, rect,nro):
		self.rect = rect
		self.press = None
		self.nu = nro

	def connect(self):
		'connect to all the events we need'
		self.cidpress = self.rect.figure.canvas.mpl_connect(
			'button_press_event', self.on_press)
		self.cidrelease = self.rect.figure.canvas.mpl_connect(
			'button_release_event', self.on_release)
		self.cidmotion = self.rect.figure.canvas.mpl_connect(
			'motion_notify_event', self.on_motion)

	def on_press(self, event):
		global pos1,pos2,actual_barra
		'on button press we will see if the mouse is over us and store some data'
		if event.inaxes != self.rect.axes: return

		contains, attrd = self.rect.contains(event)
		if not contains: return
		#print('event contains', self.rect.xy)
		x0, y0 = self.rect.xy
		self.press = x0, y0, event.xdata, event.ydata
		if x0 <= (pos1+2) and x0 >= (pos1-2):
			actual_barra = 1
		else:
			actual_barra = 2
		
	def on_motion(self, event):
		global pos1,pos2,actual_barra
		'on motion we will move the rect if the mouse is over us'
		if self.press is None: return
		if event.inaxes != self.rect.axes: return
		x0, y0, xpress, ypress = self.press
		dx = event.xdata - xpress
		dy = event.ydata - ypress
		if self.nu==3:
			self.rect.set_y(y0+dy)
			pa.set_height(y0+dy)
		else:
			self.rect.set_x(x0+dx)
			if actual_barra == 2:
				pos2 = x0+dx
			else:
				pos1 = x0+dx
						
			pa.set_width(pos2-pos1)
			pa.set_x(pos1)
		self.rect.figure.canvas.draw()
		print('event contains', pos1, pos2)
		print(self)


	def on_release(self, event):
		'on release we reset the press data'
		self.press = None
		self.rect.figure.canvas.draw()

	def disconnect(self):
		'disconnect all the stored connection ids'
		self.rect.figure.canvas.mpl_disconnect(self.cidpress)
		self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
		self.rect.figure.canvas.mpl_disconnect(self.cidmotion)

fig = plt.figure()
ax = fig.add_subplot(111)
rects = ax.bar((0,len(samples)), 100)
drs = []
for rect in rects:
    dr = DraggableRectangle(rect,1)
    dr.connect()
    drs.append(dr)

rects2 = ax.barh((100), len(samples))
drs2 = []
for rect2 in rects2:
    dr2 = DraggableRectangle(rect2,3)
    dr2.connect()
    drs2.append(dr2)


t = np.arange(0.0, 100.0, 0.01)
s1 = 3*np.sin(2*np.pi*t)

plt.figure(1)
plt.plot(samples)


ax.add_patch(pa)

plt.show()
