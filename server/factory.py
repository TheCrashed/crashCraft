from twisted.internet.protocol import ServerFactory

from .protocol import MinecraftProtocol
import encryption


class MinecraftFactory(ServerFactory):
	def startFactory(self):
		print 'MinecraftFactory started.'

		self.rsa_key = encryption.generate_key_pair()
		self.public_key = self.rsa_key.publickey().exportKey('DER')
		self.server_id = encryption.generate_server_id(10)

		self.registered_clients = []
		self.max_clients = 20

	def stopFactory(self):
		print 'MinecraftFactory stopped.'

	def buildProtocol(self, address):
		return MinecraftProtocol(self)

	def register(self, client):
		if not client in self.registered_clients:
			self.registered_clients.append(client)

	def unregister(self, client):
		if client in self.registered_clients:
			self.registered_clients.remove(client)

	def broadcast_packet(self, packet, exclude=[]):
		for client in self.registered_clients:
			if client in exclude:
				continue

			client.write_packet(packet)
