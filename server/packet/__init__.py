import struct
from collections import OrderedDict

import javatypes


class PartialPacketException(Exception):
	pass

class UnknownPacketException(Exception):
	pass

class CorruptPacketException(Exception):
	pass


class Packet(object):
	id = None
	handlers = None

	name = None
	members = OrderedDict()
	attributes = OrderedDict()

	def __init__(self, values={}):
		self.attributes = OrderedDict()

		for name in self.members.keys():
			if name in values:
				self.attributes[name] = values[name]
			else:
				self.attributes[name] = None

	def __getitem__(self, attr):
		return self.attributes[attr]

	def __setitem__(self, attr, value):
		self.attributes[attr] = value

	def values(self):
		return tuple(self.attributes.values())

	def read(self, stream):
		for name in self.members.keys():
			self.attributes[name] = self.members[name](stream)

	def write(self):
		data = javatypes.UBYTE(self.id)

		for name in self.members.keys():
			data += self.members[name](self.attributes[name])

		return data

	@staticmethod
	def identify(stream):
		if not stream:
			return None

		if Packet.handlers == None:
			Packet.refresh_packet_handlers()

		try:
			id = javatypes.UBYTE(stream)
		except:
			raise CorruptPacketException

		if not id in Packet.handlers:
			raise UnknownPacketException(id)

		try:
			packet = Packet.handlers[id]()
			packet.read(stream)
			return packet
		except struct.error:
			raise PartialPacketException
		except:
			raise CorruptPacketException

	@staticmethod
	def refresh_packet_handlers():
		Packet.handlers = {}

		for subclass in Packet.__subclasses__():
			Packet.handlers[subclass.id] = subclass

	def debug(self, header='', prefix='', footer=''):
		if header:
			print header

		print prefix + 'Packet <%s <0x%02X>>' % (self.__class__.__name__, self.id)
		if len(self.attributes.keys()):
			for name in self.attributes.keys():
				print prefix + '\t%s:  %s' % (name, self.attributes[name])
		else:
			for name in self.members.keys():
				print prefix + '\t%s: TYPE %i' % (name, self.members[name])
		if prefix:
			print prefix,
		for x in self.write():
			print '\\x%02X' % ord(x),
		print ''
		if footer:
			print footer


from . import packets