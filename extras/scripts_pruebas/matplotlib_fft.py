import matplotlib.pyplot as plt

from pydub import AudioSegment
sound = AudioSegment.from_file("/home/ciro/Música/Craig Chaquico - Bad Woman.wav")

data = sound.get_array_of_samples()

plt.plot(data)
plt.show()
#print(data)
