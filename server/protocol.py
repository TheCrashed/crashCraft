from twisted.internet.protocol import Protocol
from twisted.internet import reactor

import cStringIO
import os
import numpy
import zlib

from .packet import packets
from .packet import Packet, PartialPacketException, UnknownPacketException, CorruptPacketException

import player
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
		self.player = player.Player(self)
		self.player.username = self.username
		self.player.login()
