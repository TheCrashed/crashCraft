from twisted.internet import reactor

from .factory import Factory
from .packet import packets
from ..util import encryption
from ..util.event import Event


class Server():
	protocol = 49
	version = '1.4.5'
	rsa_key = encryption.generate_key_pair()
	public_key = rsa_key.publickey().exportKey('DER')
	server_id = encryption.generate_server_id()

	def __init__(self, port=25565):
		self.port = port
		self.factory = Factory(self)

		self.description = '-> MINIGAMES <-'
		self.clients = []
		self.max_clients = 20

		self.spawn_location = [0, 0, 0]

		self.packet_handlers = {}
		for index in xrange(256):
			self.packet_handlers[index] = Event()

	def AddClient(self, protocol):
		if not protocol in self.clients:
			self.clients.append(protocol)

			self.broadcast(packets.SpawnNamedEntity({
				'ID': protocol.id,
				'Username': protocol.username,
				'X': protocol.x * 32,
				'Y': protocol.y * 32,
				'Z': protocol.z * 32,
				'Yaw': protocol.yaw,
				'Pitch': protocol.pitch,
				'Item': 0,
				'Metadata': '\x00\x00\x7F'
			}), exclude=[protocol])

			for client in self.clients:
				if client == protocol:
					continue

				reactor.callLater(1.0, protocol.write_packet, packets.SpawnNamedEntity({
					'ID': client.id,
					'Username': client.username,
					'X': 0,
					'Y': 0,
					'Z': 0,
					'Yaw': 0,
					'Pitch': 0,
					'Item': 0,
					'Metadata': '\x00\x00\x7F'
				}))

			self.broadcast(packets.ChatMessage({
				'Message': '<Server> %s has joined the server!' % protocol.username
			}))

	def RemoveClient(self, protocol):
		if protocol in self.clients:
			self.clients.remove(protocol)

			self.broadcast(packets.SpawnNamedEntity({
				'ID': protocol.id,
				'Username': protocol.username,
				'X': 0,
				'Y': -1,
				'Z': 0,
				'Yaw': 0,
				'Pitch': 0,
				'Item': 0,
				'Metadata': '\x00\x00\x7F'
			}))

			self.broadcast(packets.ChatMessage({
				'Message': '<Server> %s has left the server!' % protocol.username
			}))

	def Run(self):
		reactor.listenTCP(self.port, self.factory)
		reactor.run()

	def Stop(self):
		reactor.stop()

	def broadcast(self, packet, exclude=[]):
		for client in self.clients:
			if client in exclude:
				continue
			client.write_packet(packet)

	def broadcast_buffer(self, buffer, exclude=[]):
		for client in self.clients:
			if client in exclude:
				continue
			client.dataWrite(buffer)
