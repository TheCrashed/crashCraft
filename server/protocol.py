try:
	from cStringIO import StringIO
except ImportError:
	import StringIO

import twisted.internet.protocol

from .packet.packet import Packet
from .packet import PartialPacketException, UnknownPacketException, CorruptPacketException


class Protocol(twisted.internet.protocol.Protocol):
	def __init__(self, factory):
		self.factory = factory
		self.read_buffer = ''
		self.packet_buffer = []
		self.partial_packets = 0
		self.partial_threshold = 4

	def connectionMade(self):
		pass

	def connectionLost(self, reason):
		pass

	def dataReceived(self, data):
		self.read_buffer += data
		self.parse_packets()

	def clear(self):
		self.read_buffer = ''

	def parse_packets(self):
		packets = []

		while len(self.read_buffer):
			try:
				packet, index = Packet.read(self.read_buffer)
				self.read_buffer = self.read_buffer[index:]
				packets.append(packet)
			except PartialPacketException:
				self.partial_packets += 1
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
			print packet.printable()
