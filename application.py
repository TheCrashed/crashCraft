


class Application():
	def __init__(self):
		self.world = None
		self.server = None

		self.Init()

	def Init(self):
		pass

	def Run(self):
		self.server.Run()

	def Stop(self):
		self.server.Stop()
