#########################################################################
# Author: 	Josh Griffin
# Date: 	3/22/2019
#########################################################################
# Audio Synthesis Workstation
#########################################################################

#########################################################################
# Todo
#########################################################################
# increase yield size of gens to meet time constraint

#########################################################################
# Imports
#########################################################################
from sounddevice import Stream
import numpy as np
from numpy import pi
import matplotlib.pyplot as plt
import asyncio
from time import sleep
from queue import Queue
from scipy.io import wavfile
from collections import deque
from os import listdir,getcwd

#########################################################################
# Main Audio Class
#########################################################################
class daw:

	l_inputs = []
	Fs = 44100
	bufferSize = 100
	output_gen = []
	buf = np.linspace(-1,1,bufferSize)
	inQ = Queue()

	def __init__(self):
		for i in range(20*self.Fs):
			self.inQ.put(0)
		print('DAW initialized')
		# self.output_gen = self.test1()
		# self.output_gen = self.test2()
		self.output_gen = self.test3()

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
		# dw = self.displayWindow(au)
		for v in dw:
			yield(v)

	def test2(self):
		i = self.inputGen()
		for v in i:
			yield(v)

	def test3(self):
		dg = self.dirGen('testwavs')
		lg = self.autolimiter(dg)
		for v in lg:
			yield(v)

	#####################################################################
	# Building Blocks
	#####################################################################
	def displayWindow(self,g):
		ctr = 0
		for v in g:
			if not ctr % int(self.Fs/3000):
				self.buf = np.roll(np.copy(self.buf),-1)
				self.buf[-1] = v
			if not ctr % int(self.Fs):
				np.save('buf.npy',self.buf)

			yield(v)
			ctr += 1

	def dirGen(self,path):
		wd = getcwd()
		fns = [f for f in listdir(path)]
		gens = [self.fileGen(wd+'/'+path+'/'+fn) for fn in fns]
		while True:
			v = 0
			for g in gens:
				v += g.__next__()
			yield(v)

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

	def windowedSinc(self,g,width=3):
		kernel = np.sin(np.linspace(-width,width,2*width+1))/np.linspace(-width,width,2*width+1)
		kernel[width] = 1

		buf = deque()
		for i in range(width*2+1):
			buf.append(0)

		for v in g:
			buf.append(v)
			out = buf.popleft()
			yield(sum(buf*kernel))


	def fir(self):
		print('temp fir')


	def sdelay(self,g,delay=1000,decay=.5):
		dline = deque()
		for i in range(delay):
			dline.append(0)
		for v in g:
			dval = dline.popleft()
			v += (dval * decay)
			dline.append(v)
			yield(v)

	def inputGen(self):
		while True:
			v = self.inQ.get()
			if v:
				yield(v)

	def fileGen(self,fn):
		a = wavfile.read(fn)[1]
		while True:
			for v in a[:,0]:
				yield(v)


#########################################################################
# Device Interface
#########################################################################
	def callback(self,indata, outdata, frames, time, status):
		if status:
			print(status)
		# for dat in np.sum(indata[:,:],axis=1):
		# 	self.inQ.put(dat)
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



