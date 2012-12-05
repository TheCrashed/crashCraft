import os
from twisted.internet import reactor

from .packet import packets
import javatypes


class Player():
	def __init__(self, protocol):
		self.id = javatypes.struct.unpack('H', os.urandom(2))[0]
		self.protocol = protocol

		self.x = 0
		self.y = 0
		self.z = 0
		self.yaw = 0
		self.pitch = 0

	def get_world(self):
		return self.protocol.factory.world

	def broadcast(self, packet, all=False):
		exclude = []
		if not all:
			exclude = [self.protocol]
		self.protocol.factory.broadcast_packet(packet, exclude)

	def ping(self):
		self.protocol.write_packet(packets.KeepAlive({'ID': 0}))
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
		self.protocol.write_packet(packets.BlockChange({
			'X': packet['X'],
			'Y': packet['Y'],
			'Z': packet['Z'],
			'Type': 0x02,
			'Metadata': 0
		}))

	def on_player(self, packet):
		def degree_to_byte(degree, fix=0):
			degree += fix
			while degree >= 360:
				degree -= 360
			while degree < 0:
				degree += 360

			return int((degree * 256.0 / 360.0))

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
		for x in xrange(self.get_world().width):
			for z in xrange(self.get_world().length):
				data = self.get_world().chunks[x][z].get_data()

				self.protocol.write_packet(packets.ChunkData({
					'X': x,
					'Z': z,
					'GroundUp': True,
					'PrimaryBitMap': 0xFFFF,
					'AddBitMap': 0x0000,
					'CompressedSize': len(data),
					'CompressedData': data
				}))
