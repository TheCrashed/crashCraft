from cStringIO import StringIO
from collections import OrderedDict

from ...util.javatypes import *
from . import PartialPacketException, UnknownPacketException, CorruptPacketException


class Packet(object):
	id = None
	members = None
	attributes = None
	handlers = None

	def __init__(self, values={}):
		self.attributes = OrderedDict()

		for name in self.members.keys():
			if name in values:
				self.attributes[name] = values[name]
			else:
				self.attributes[name] = None

	@staticmethod
	def read(buffer):
		if not hasattr(buffer, 'read'):
			if not len(buffer):
				raise EOFError

			buffer = StringIO(buffer)

		try:
			id = UByte.frombuffer(buffer)
		except:
			raise CorruptPacketException

		try:
			handler = Packet.get_handler(id)
		except KeyError:
			raise UnknownPacketException(id)

		packet = handler()
		try:
			packet.frombuffer(buffer)
			return packet, buffer.tell()
		except EOFError:
			raise PartialPacketException(id)

	@staticmethod
	def get_handler( id):
		if not Packet.handlers:
			Packet.build_handlers()

		return Packet.handlers[id]

	@staticmethod
	def build_handlers():
		Packet.handlers = {}

		for subclass in Packet.__subclasses__():
			Packet.handlers[subclass.id] = subclass

	def __getitem__(self, attr):
		return self.attributes[attr]

	def __setitem__(self, attr, value):
		self.attributes[attr] = value

	def frombuffer(self, buffer):
		self.attributes = OrderedDict()

		for name, datatype in self.members.items():
			self.attributes[name] = datatype.frombuffer(buffer)

	def tostring(self):
		packed = UByte.tostring(self.id)
		for name, datatype in self.members.items():
			packed += datatype.tostring(self.attributes[name])
		return packed

	def printable(self):
		output = '<[0x%02X] %s ' % (self.id, self.__class__.__name__)
		output += ', '.join('%s: %s' % (name, self.attributes[name]) for name, datatype in self.members.items())
		output += '>'
		return output
