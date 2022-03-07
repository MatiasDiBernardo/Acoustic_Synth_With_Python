import threading
import sound_bank
import pyaudio
import numpy as np

class Load():
	def __init__(self):
		self.starting_preset = 0
		self.pluck_sounds = 0
		self.load = False

	def loading(self):
		if not self.load:
			return True
		else:
			return False

	def thread_loading(self, new_preset):
		self.load = False
		self.pluck_sounds = sound_bank.list_sounds(new_preset[0], new_preset[1], new_preset[2], new_preset[3], new_preset[4])
		self.load = True

	def load_sound(self, new_preset_):
		if self.starting_preset != new_preset_:

			x = threading.Thread(target=self.thread_loading, args=(new_preset_,))
			x.start()

			new_preset_ = self.starting_preset

class Play_Sounds():
	def __init__(self, buffer, step, fs):
		'''
		buffer: buffer size
		step: starting sample
		fs: sample rate
		'''

		self.buffer = buffer
		self.step = step
		self.stream = pyaudio.PyAudio().open(
					rate=fs,
					channels=1,
					format=pyaudio.paInt16,
					output=True,
					frames_per_buffer=self.buffer
					)

	def buffer_segmentation(self, complete_audio, note):
		'''
		Takes the original audio and the numbers of notes press and divide it in chuncks of the size of the buffer.
		If two notes were play at the same time it sums the amplitudes of the signals.
		'''

		if len(note) == 1:
			audio = complete_audio[note[0]][0 + self.buffer * self.step: self.buffer + self.buffer * self.step]

		if len(note) > 1:
			audio = 0
			for i in note:
				audio += complete_audio[i][0 + self.buffer * self.step: self.buffer + self.buffer * self.step]
				audio /= (len(note)/2) 

		return audio


	def play(self, audio):
		'''
		Feeds the data from the buffer segmentation to the stream
		'''

		audio = audio * 32767
		audio = np.int16(audio).tobytes()
		self.stream.write(audio)
