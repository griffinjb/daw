#########################################################################
# Author: 	Josh Griffin
# Date: 	3/22/2019
#########################################################################
# Audio Synthesis Workstation
#########################################################################


#########################################################################
# Imports
#########################################################################
from sounddevice import Stream
import numpy as np
from numpy import pi
import matplotlib.pyplot as plt
import asyncio


#########################################################################
# Main Audio Class
#########################################################################
class daw:

	l_inputs = []
	Fs = 44100
	bufferSize = 1000
	output_gen = []


	def __init__(self):
		print('DAW initialized')
		self.output_gen = self.test1()


	def run(self):
		self.play()



#########################################################################
# Audio Synthesis
#########################################################################

	#####################################################################
	# Chained Modules
	#####################################################################
	def test1(self):
		s1 = self.singen(f=330)
		s2 = self.singen(f=440)
		s3 = self.singen(f=100)
		su = self.gensum(s1,s2,s3)
		au = self.autolimiter(su)
		for v in au:
			yield(v)


	#####################################################################
	# Building Blocks
	#####################################################################
	def singen(self,f=440):
		x = np.linspace(0,1,self.Fs)
		y = np.sin(f*2*pi*x)
		while True:
			for v in y:
				yield(v)

	def autolimiter(self,gen,recoveryRate=1):
		gain = 1
		for v in gen:
			gain *= recoveryRate
			if abs(v*gain) > 1:
				gain = 1/abs(v)
			yield(gain*v)

	def gensum(self,*args):
		while True:
			o = 0
			for gen in args:
				o += gen.__next__()
			yield(o)

	def gain(self,gen,gain):
		for v in g:
			yield(gain*v)

	def fir(self):
		print('temp fir')


	def delay(self):
		print('temp delay')

#########################################################################
# Device Interface
#########################################################################
	def callback(self,indata, outdata, frames, time, status):
		if status:
			print(status)
		outdata[:,0:2] = np.transpose(np.array([self.output_gen.__next__() for _ in range(self.bufferSize)],ndmin=2).repeat(2,axis=0))

	def play(self):
		with Stream(samplerate=44100, blocksize=self.bufferSize,callback=self.callback):
			print('#' * 80)
			print('press Return to quit')
			print('#' * 80)
			input()


if __name__ == '__main__':
	d = daw()
	d.run()



