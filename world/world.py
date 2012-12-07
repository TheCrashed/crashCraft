from .chunk import Chunk


class World():
	def __init__(self):
		self.Init()

	def Init(self):
		self.Chunks = []
		self.Chunk_Map = {}

	def Create(self, width, length):
		self.Init()

		for x in xrange(width[0], width[1]):
			for z in xrange(length[0], length[1]):
				self.CreateChunk(x, z)

	def CreateChunk(self, x, z):
		self.SetChunk(Chunk(x, z))

	def GetChunk(self, x, z):
		try:
			return self.Chunk_Map[x, z]
		except KeyError:
			return None

	def SetChunk(self, chunk):
		if (chunk.X, chunk.Z) in self.Chunk_Map:
			self.Chunks.remove(self.Chunk_Map[chunk.X, chunk.Z])

		self.Chunk_Map[chunk.X, chunk.Z] = chunk
		self.Chunks.append(chunk)
