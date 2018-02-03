from pydub import AudioSegment
sound = AudioSegment.from_file("/home/ciro/Documentos/EDEQ/Juego2/sprites/sonidos/andar.mp3", format="mp3")

# simple export
file_handle = sound.export("/home/ciro/Documentos/EDEQ/Juego2/sprites/sonidos/andar.ogg", format="ogg")
