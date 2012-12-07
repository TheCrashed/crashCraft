from twisted.internet import reactor

from .factory import Factory


class Server():
	def __init__(self, port=25565):
		self.port = port
		self.factory = Factory(self)

	def Run(self):
		reactor.listenTCP(self.port, self.factory)
		reactor.run()

	def Stop(self):
		reactor.stop()
