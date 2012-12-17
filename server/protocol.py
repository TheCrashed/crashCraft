import zlib
import twisted.internet.protocol

from .packet import Packet, packets
from .packet import PartialPacketException, UnknownPacketException, CorruptPacketException
from ..util.event import Event
from ..util import encryption
from ..util.math import degree_to_byte


class BaseProtocol(twisted.internet.protocol.Protocol):
	def __init__(self, factory):
		self.factory = factory
		self.read_buffer = ''
		self.packet_buffer = []
		self.partial_packets = 0
		self.partial_threshold = 4
		self.local_handlers = {}
		self.write_cipher = str
		self.read_cipher = str

	def connectionMade(self):
		pass

	def connectionLost(self, reason):
		pass

	def dataReceived(self, data):
		self.read_buffer += self.read_cipher(data)
		self.parse_packets()

	def dataWrite(self, data):
		self.transport.write(self.write_cipher(data))

	def clear(self):
		self.read_buffer = ''

	def write_packet(self, packet):
		self.dataWrite(packet.tostring())

	def parse_packets(self):
		packets = []

		while len(self.read_buffer):
			try:
				packet, index = Packet.read(self.read_buffer)
				self.read_buffer = self.read_buffer[index:]
				packets.append(packet)
			except PartialPacketException:
				self.partial_packets += 1
				print 'Partial Packet!'
				if self.partial_packets >= self.partial_threshold:
					print 'Partial Packet Threshold!'
					self.clear()
				break
			except UnknownPacketException, error:
				print 'Unknown Packet: 0x%02X' % error.args[0]
				self.clear()
				break
			except CorruptPacketException:
				print 'Corrupted Packet!'
				self.clear()
				break

		self.packet_buffer += packets
		self.handle_packets()

	def handle_packets(self):
		while len(self.packet_buffer):
			packet = self.packet_buffer.pop(0)
			#print ''.join(c for c in packet.printable() if ord(c) > 31 or ord(c) == 9)
			self.factory.server.packet_handlers[packet.id](self, packet)

			try:
				self.local_handlers[packet.id](packet)
			except KeyError:
				pass


class Protocol(BaseProtocol):
	def __init__(self, *args, **kwrds):
		BaseProtocol.__init__(self, *args, **kwrds)

		self.local_handlers[0x02] = self.on_handshake
		self.local_handlers[0xFE] = self.on_server_list_ping

	def send_disconnect(self, reason):
		self.write_packet(packets.Disconnect({'Reason': 
			reason
		}))

		self.transport.loseConnection()

	def on_server_list_ping(self, packet):
		self.send_disconnect(
			unichr(0).join([
				unichr(0xA7) + unichr(0x31),
				str(self.factory.server.protocol),
				self.factory.server.version,
				self.factory.server.description,
				str(len(self.factory.server.clients)),
				str(self.factory.server.max_clients)
			])
		)

	def on_handshake(self, packet):
		self.username = packet['Username']
		self.verify_token = encryption.generate_bytes(4)

		self.send_encryption_key_request()

	def send_encryption_key_request(self):
		self.write_packet(packets.EncryptionKeyRequest({
			'ServerID': self.factory.server.server_id,
			'PublicKey': self.factory.server.public_key,
			'VerifyToken': self.verify_token
		}))

		self.local_handlers[0xFC] = self.on_encryption_key_response

	def on_encryption_key_response(self, packet):
		response_token = encryption.decrypt(self.factory.server.rsa_key, packet['VerifyToken'])

		if response_token != self.verify_token:
			self.send_disconnect('Invalid VerifyToken!')
			return

		shared_secret = encryption.decrypt(self.factory.server.rsa_key, packet['SharedSecret'])

		self.send_encryption_key_response()
		Player(self.factory, self.transport, self.username, shared_secret)

	def send_encryption_key_response(self):
		self.write_packet(packets.EncryptionKeyResponse({
			'SharedSecret': '',
			'VerifyToken': ''
		}))


class Player(BaseProtocol):
	def __init__(self, factory, transport, username, shared_secret):
		BaseProtocol.__init__(self, factory)

		self.username = username
		self.shared_secret = shared_secret

		self.id = encryption.generate_id()
		self.x = self.factory.server.spawn_location[0]
		self.y = self.factory.server.spawn_location[1]
		self.z = self.factory.server.spawn_location[2]
		self.yaw = 0
		self.pitch = 0

		self.read_cipher = encryption.cipher(self.shared_secret).decrypt
		self.write_cipher = encryption.cipher(self.shared_secret).encrypt

		self.transport = transport
		self.transport.protocol = self

		self.factory.server.AddClient(self)


		self.local_handlers[0xCD] = self.on_client_status

		self.local_handlers[0x0A] = self.on_player
		self.local_handlers[0x0B] = self.on_player
		self.local_handlers[0x0C] = self.on_player
		self.local_handlers[0x0D] = self.on_player
		self.local_handlers[0x0E] = self.on_digging

		self.local_handlers[0x12] = self.on_animation
		self.local_handlers[0x13] = self.on_action

		self.local_handlers[0x03] = self.on_chat
		self.local_handlers[0xFF] = self.on_quit

		self.half_view = 3

		self.send_login()

	def connectionLost(self, *args, **kwrds):
		self.factory.server.RemoveClient(self)

		BaseProtocol.connectionLost(self, *args, **kwrds)

	def send_login(self):
		self.write_packet(packets.LoginRequest({
			'ID': self.id,
			'LevelType': 'minigames',
			'GameMode': 0,
			'Dimension': 0,
			'Difficulty': 0,
			'NotUsed': 0,
			'MaxPlayers': self.factory.server.max_clients
		}))

		self.send_chunks()

	def on_client_status(self, packet):
		self.write_packet(packets.SpawnPosition({
			'X': self.factory.server.spawn_location[0],
			'Y': self.factory.server.spawn_location[1],
			'Z': self.factory.server.spawn_location[2],
		}))

		self.write_packet(packets.PlayerPositionAndLook({
			'X': self.factory.server.spawn_location[0],
			'Y': self.factory.server.spawn_location[1],
			'Stance': 0.9,
			'Z': self.factory.server.spawn_location[2],
			'Yaw': 0,
			'Pitch': 0,
			'OnGround': False
		}))

	def send_chunks(self):
		for x in xrange(-self.half_view, self.half_view * 2 + 1):
			for z in xrange(-self.half_view, self.half_view * 2 + 1):
				self.send_chunk(self.factory.server.world.GetChunk(x, z))

	def send_chunk(self, chunk):
		if not chunk:
			return

		compressed = zlib.compress(''.join([
			chunk.Blocks.reshape((16, 16, 256)).tostring(),
			chunk.Block_Metadata[:128,:,:].reshape((16, 16, 128)).tostring(),
			chunk.Block_Light[:128,:,:].reshape((16, 16, 128)).tostring(),
			chunk.Skylight[:128,:,:].reshape((16, 16, 128)).tostring()
		]))

		self.write_packet(packets.ChunkData({
			'X': chunk.X,
			'Z': chunk.Z,
			'GroundUp': True,
			'PrimaryBitMap': 0xFFFF,
			'AddBitMap': 0x0000,
			'CompressedSize': len(compressed),
			'CompressedData': compressed
		}))

	def on_digging(self, packet):
		if packet['Status'] in (2,):
			self.send_chunk(self.factory.server.world.GetChunk(packet['X'] / 32, packet['Z'] / 32))

	def on_animation(self, packet):
		if packet['ID'] != self.id:
			return

		self.factory.server.broadcast(packet, [self])

	def on_action(self, packet):
		if packet['ID'] != self.id:
			return

		metadata = '\x00'
		if packet['ActionID'] == 1:
			metadata = '\x02'
		elif packet['ActionID'] == 4:
			metadata = '\x08'

		self.factory.server.broadcast(packets.EntityMetadata({
			'ID': self.id,
			'Metadata': '\x00%s\x7F' % metadata
		}), [self])

	def on_player(self, packet):
		if packet.id == 0x0A:
			return
		if packet.id in (0x0B, 0x0D):
			self.x, self.y, self.z = packet['X'], packet['Y'], packet['Z']
		if packet.id in (0x0C, 0x0D):
			self.yaw, self.pitch = packet['Yaw'], packet['Pitch']

		self.factory.server.broadcast(packets.EntityTeleport({
			'ID': self.id,
			'X': self.x * 32,
			'Y': self.y * 32,
			'Z': self.z * 32,
			'Yaw': degree_to_byte(self.yaw),
			'Pitch': degree_to_byte(self.pitch)
		}), [self])

		self.factory.server.broadcast(packets.EntityHeadLook({
			'ID': self.id,
			'Yaw': degree_to_byte(self.yaw)
		}), [self])

	def on_chat(self, packet):
		self.factory.server.broadcast(packets.ChatMessage({
			'Message': '<%s> %s' % (self.username, packet['Message']),
		}))

	def on_quit(self, packet):
		self.transport.loseConnection()
