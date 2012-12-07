import twisted.internet.protocol

from .protocol import Protocol


class Factory(twisted.internet.protocol.ServerFactory):
	def __init__(self, server):
		self.server = server

	def startFactory(self):
		self.protocol = Protocol

	def stopFactory(self):
		pass

	def buildProtocol(self, address):
		return self.protocol(self)
