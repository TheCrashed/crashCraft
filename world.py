import numpy
import zlib


class MinecraftWorld():
	def __init__(self, chunk_width=4, chunk_length=4):
		self.width = chunk_width * 2 + 1
		self.length = chunk_length * 2 + 1

		self.chunks = [[Chunk(x, z) for z in xrange(-chunk_length, chunk_length + 1)] for x in xrange(-chunk_width, chunk_width + 1)]


class Chunk():
	def __init__(self, x, z):
		self.x = x
		self.z = z
		self.dirty = True
		self.data = None

		self.blocks = numpy.zeros((256, 16, 16), numpy.uint8)
		self.block_metadata = numpy.zeros((128, 16, 16), numpy.uint8)
		self.block_light = numpy.zeros((128, 16, 16), numpy.uint8)
		self.skylights = numpy.zeros((128, 16, 16), numpy.uint8)

		self.block_light[:] = 0xFF
		self.skylights[:] = 0xFF

		self.build_data()

	def get_data(self):
		if self.dirty:
			self.build_data()

		return self.data

	def build_data(self):
		self.data = self.blocks.reshape((16, 16, 256)).tostring() + \
					self.block_metadata.reshape((16, 16, 128)).tostring() + \
					self.block_light.reshape((16, 16, 128)).tostring() + \
					self.skylights.reshape((16, 16, 128)).tostring()

		self.data = zlib.compress(self.data)
		self.dirty = False
