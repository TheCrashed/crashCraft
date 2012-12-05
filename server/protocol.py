from twisted.internet.protocol import Protocol
from twisted.internet import reactor

import cStringIO
import os
import numpy
import zlib

from .packet import packets
from .packet import Packet, PartialPacketException, UnknownPacketException, CorruptPacketException
import javatypes
import encryption


class MinecraftProtocol(Protocol):
	def __init__(self, factory):
		self.factory = factory

		self.read_cipher = str
		self.write_cipher = str
		self.read_buffer = cStringIO.StringIO()
		self.partial_packets = 0
		self.partial_threshold = 10

		self.packet_handlers = {
			0x00: lambda x: x,
			0x02: self.on_handshake,
			0xFC: self.on_encryptionkeyresponse,
			0xFE: self.on_serverlist,
		}

	def connectionMade(self):
		print '\t%s connected.' % self.transport.getPeer()

	def connectionLost(self, reason):
		self.factory.unregister(self)
		print '\t%s disconnected: %s' % (self.transport.getPeer(), reason.getErrorMessage())

	def dataReceived(self, data):
		self.read_buffer.seek(0, 2)
		self.read_buffer.write(self.read_cipher(data))
		self.read_buffer.seek(0)
		self.read()

	def clear(self):
		self.partial_packets = 0
		self.read_buffer = cStringIO.StringIO()

	def trim(self):
		data = self.read_buffer.read()
		self.read_buffer = cStringIO.StringIO()
		self.read_buffer.write(data)
		self.read_buffer.seek(0)
		return len(data)

	def read(self):
		#print ' '.join('0x%02X' % ord(x) for x in self.read_buffer.getvalue())

		packets = []
		try:
			while True:
				packets.append(Packet.identify(self.read_buffer))
				self.trim()

		except PartialPacketException:
			self.partial_packets += 1
			#print '\t\t%s PARTIAL PACKET' % self.transport.getPeer()
			if self.partial_packets >= self.partial_threshold:
				#print '\t\t%s PARTIAL PACKET THRESHOLD' % self.transport.getPeer()
				self.clear()

		except (CorruptPacketException, UnknownPacketException), error:
			#print '\t\t%s CORRUPTED STREAM' % self.transport.getPeer()
			self.clear()

		for packet in packets:
			if packet.id in self.packet_handlers:
				self.packet_handlers[packet.id](packet)

	def write(self, data):
		self.transport.write(self.write_cipher(data))

	def write_packet(self, packet):
		self.write(packet.write())


	def on_serverlist(self, packet):
		self.write_packet(packets.Disconnect({'Reason': unichr(0).join([
			unichr(0xA7) + unichr(0x31),
			'49',
			'1.4.5',
			'->MINIGAMES<-',
			str(len(self.factory.registered_clients)),
			str(self.factory.max_clients)
		])}))
		self.transport.loseConnection()

	def on_handshake(self, packet):
		self.username = packet['Username']
		self.verification_token = encryption.generate_bytes(4)

		self.write_packet(packets.EncryptionKeyRequest({
			'ServerID': self.factory.server_id,
			'PublicKey': self.factory.public_key,
			'VerifyToken': self.verification_token
		}))

	def on_encryptionkeyresponse(self, packet):
		verification_token = encryption.decrypt(self.factory.rsa_key, packet['VerifyToken'])

		if verification_token != self.verification_token:
			if token != self.token:
				self.write_packet(packets.Disconnect({'Reason': 'Invalid VerifyToken'}))
				return

		self.shared_secret = encryption.decrypt(self.factory.rsa_key, packet['SharedSecret'])

		self.write_packet(packets.EncryptionKeyResponse({
			'SharedSecret': '',
			'VerifyToken': ''
		}))

		self.read_cipher = encryption.cipher(self.shared_secret).decrypt
		self.write_cipher = encryption.cipher(self.shared_secret).encrypt

		self.factory.register(self)
		self.player = ProxyPlayer(self)
		self.player.username = self.username
		self.player.login()


class ProxyPlayer():
	def __init__(self, protocol):
		self.id = javatypes.struct.unpack('H', os.urandom(2))[0]
		self.protocol = protocol

		self.x = 0
		self.y = 0
		self.z = 0
		self.yaw = 0
		self.pitch = 0
		self.daytime = 0
		self.agetime = 0

	def broadcast(self, packet, all=False):
		exclude = []
		if not all:
			exclude = [self.protocol]
		self.protocol.factory.broadcast_packet(packet, exclude)

	def ping(self):
		self.daytime += 20
		self.agetime += 20
		#self.protocol.write_packet(packets.TimeUpdate({'AgeOfWorld': self.agetime, 'TimeOfDay': self.daytime}))
		self.protocol.write_packet(packets.KeepAlive({'ID': self.agetime / 20}))
		reactor.callLater(1.0, self.ping)

	def on_clientstatus(self, packet):
		if packet['Payload'] == 0:
			self.protocol.write_packet(packets.PlayerPositionAndLook({
				'X': 8,
				'Y': 68,
				'Stance': 0.9,
				'Z': 8,
				'Yaw': 0,
				'Pitch': 0,
				'OnGround': False
			}))

			self.broadcast(packets.SpawnNamedEntity({
				'EID': self.id,
				'Name': self.username,
				'X': 8 * 32,
				'Y': 68 * 32,
				'Z': 8 * 32,
				'Yaw': 45,
				'Pitch': 45,
				'CurrentItem': 0,
				'Metadata': 0,
				'Payload': 0,
				'EndMetadata': 0x7F
			}))

			self.broadcast(packets.PlayerListItem({
				'Name': self.username,
				'Online': True,
				'Ping': 1
			}), all=True)

			for client in self.protocol.factory.registered_clients:
				if client == self.protocol:
					continue

				reactor.callLater(0.1, self.protocol.write_packet, packets.SpawnNamedEntity({
					'EID': client.player.id,
					'Name': client.player.username,
					'X': client.player.x * 32,
					'Y': client.player.y * 32,
					'Z': client.player.z * 32,
					'Yaw': 45,
					'Pitch': 45,
					'CurrentItem': 0,
					'Metadata': 0,
					'Payload': 0,
					'EndMetadata': 0x7F
				}))

				reactor.callLater(0.1, self.protocol.write_packet, packets.PlayerListItem({
					'Name': client.player.username,
					'Online': True,
					'Ping': 1
				}))

			self.broadcast(packets.ChatMessage({
				'Message': '<Server> %s has joined.' % self.username
			}), all=True)

			self.protocol.packet_handlers[0x03] = self.on_chat
			self.protocol.packet_handlers[0x0A] = self.on_player
			self.protocol.packet_handlers[0x0B] = self.on_player
			self.protocol.packet_handlers[0x0C] = self.on_player
			self.protocol.packet_handlers[0x0D] = self.on_player
			self.protocol.packet_handlers[0x0E] = self.on_dig

			reactor.callLater(0, self.ping)

	def on_chat(self, packet):
		packet['Message'] = '<%s> %s' % (self.username, packet['Message'][:100])
		self.broadcast(packet, all=True)

	def on_dig(self, packet):
		'''
		self.protocol.write_packet(packets.BlockChange({
			'X': packet['X'],
			'Y': packet['Y'],
			'Z': packet['Z'],
			'Type': 0x02,
			'Metadata': 0
		}))
		'''
		self.send_chunks()

	def on_player(self, packet):
		def degree_to_byte(degree, fix=0):
			degree += fix
			while degree >= 360:
				degree -= 360
			while degree < 0:
				degree += 360

			return int((degree * 256.0 / 360.0))

		'''
		if packet.id == 0x0A:
			return
			self.broadcast(packets.Entity({
				'EID': self.id
			}))

		elif packet.id == 0x0B:
			self.x, self.y, self.z = packet['X'], packet['Y'], packet['Z']

			self.broadcast(packets.EntityTeleport({
				'EID': self.id,
				'X': packet['X'] * 32,
				'Y': packet['Y'] * 32,
				'Z': packet['Z'] * 32,
				'Yaw': degree_to_byte(self.yaw),
				'Pitch': degree_to_byte(-self.pitch)
			}))

		elif packet.id == 0x0C:
			self.yaw, self.pitch = packet['Yaw'], packet['Pitch']

			self.broadcast(packets.EntityLook({
				'EID': self.id,
				'Yaw': degree_to_byte(packet['Yaw']),
				'Pitch': degree_to_byte(-packet['Pitch'])
			}))

		elif packet.id == 0x0D:
			self.x, self.y, self.z, self.yaw, self.pitch = packet['X'], packet['Y'], packet['Z'], packet['Yaw'], packet['Pitch']

			self.broadcast(packets.EntityTeleport({
				'EID': self.id,
				'X': packet['X'] * 32,
				'Y': packet['Y'] * 32,
				'Z': packet['Z'] * 32,
				'Yaw': degree_to_byte(packet['Yaw']),
				'Pitch': degree_to_byte(-packet['Pitch'])
			}))
		'''

		if packet.id == 0x0A:
			return
		if packet.id in (0x0B, 0x0D):
			self.x, self.y, self.z = packet['X'], packet['Y'], packet['Z']
		if packet.id in (0x0C, 0x0D):
			self.yaw, self.pitch = packet['Yaw'], packet['Pitch']

		self.broadcast(packets.EntityTeleport({
			'EID': self.id,
			'X': self.x * 32,
			'Y': self.y * 32,
			'Z': self.z * 32,
			'Yaw': degree_to_byte(self.yaw),
			'Pitch': degree_to_byte(self.pitch)
		}))

		self.broadcast(packets.EntityHeadLook({
			'EID': self.id,
			'Yaw': degree_to_byte(self.yaw)
		}))

	def login(self):
		self.protocol.write_packet(packets.LoginRequest({
			'EntityID': self.id,
			'LevelType': 'minigames',
			'GameMode': 0,
			'Dimension': 0,
			'Difficulty': 0,
			'NotUsed': 0,
			'MaxPlayers': 16
		}))

		self.protocol.write_packet(packets.SpawnPosition({
			'X': 0,
			'Y': 128,
			'Z': 0
		}))

		self.send_chunks()

		self.protocol.packet_handlers[0xCD] = self.on_clientstatus

	def send_chunks(self):
		for x in xrange(-1, 2):
			for z in xrange(-1, 2):
				blocks = numpy.zeros((256, 16, 16), numpy.uint8)
				block_metadata = numpy.zeros((128, 16, 16), numpy.uint8)
				block_light = numpy.zeros((128, 16, 16), numpy.uint8)
				skylights = numpy.zeros((128, 16, 16), numpy.uint8)

				if x == 0 and z == 0:
					blocks[63,:,:] = 0x02

				blocks = blocks.reshape((16, 16, 256))
				block_light[:] = 0xFF
				skylights[:] = 0xFF

				compressed = zlib.compress(blocks.tostring() + block_metadata.tostring() + block_light.tostring() + skylights.tostring())

				self.protocol.write_packet(packets.ChunkData({
					'X': x,
					'Z': z,
					'GroundUp': True,
					'PrimaryBitMap': 0xFFFF,
					'AddBitMap': 0x0000,
					'CompressedSize': len(compressed),
					'CompressedData': compressed
				}))
