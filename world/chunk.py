import numpy

from . import CHUNK_WIDTH, CHUNK_HEIGHT, CHUNK_LENGTH


class Chunk():
	def __init__(self, x=None, z=None):
		if x != None and z != None:
			self.Init(x, z)

	def Init(self, x=0, z=0):
		self.X = x
		self.Z = z

		self.Blocks = numpy.zeros((CHUNK_HEIGHT, CHUNK_LENGTH, CHUNK_WIDTH), numpy.ubyte)
		self.Block_Metadata = numpy.zeros((CHUNK_HEIGHT, CHUNK_LENGTH, CHUNK_WIDTH), numpy.ubyte)
		self.Block_Light = numpy.zeros((CHUNK_HEIGHT, CHUNK_LENGTH, CHUNK_WIDTH), numpy.ubyte)
		self.Skylight = numpy.zeros((CHUNK_HEIGHT, CHUNK_LENGTH, CHUNK_WIDTH), numpy.ubyte)
		self.Biomes = numpy.zeros((CHUNK_LENGTH, CHUNK_WIDTH), numpy.ubyte)
