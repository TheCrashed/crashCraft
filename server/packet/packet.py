from cStringIO import StringIO
from collections import OrderedDict

from ...util.javatypes import *
from . import types
from . import PartialPacketException, UnknownPacketException, CorruptPacketException


class Packet(object):
	id = None
	members = None
	attributes = None
	handlers = None

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
		except EOFError:
			raise PartialPacketException(id)
		else:
			return packet, buffer.tell()

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


	def frombuffer(self, buffer):
		self.attributes = OrderedDict()

		for name, datatype in self.members.items():
			self.attributes[name] = datatype.frombuffer(buffer)

	def tostring(self):
		packed = ''
		for name, datatype in self.members.items():
			packed += datatype.tostring(self.attributes[name])
		return packed

	def printable(self):
		output = '<[0x%02X] %s' % (self.id, self.__class__.__name__)
		for name, datatype in self.members.items():
			output += ' %s: %s' % (name, self.attributes[name])
		output += '>'
		return output



class Packets():
	class KeepAlive(Packet):
		id = 0x00
		members = OrderedDict([
			('ID', Byte)
		])

	class LoginRequest(Packet):
		id = 0x01
		members = OrderedDict([
			('ID', Int),
			('LevelType', Unicode),
			('GameMode', Byte),
			('Dimension', Byte),
			('Difficulty', Byte),
			('NotUsed', Byte),
			('MaxPlayers', Byte)
		])

	class Handshake(Packet):
		id = 0x02
		members = OrderedDict([
			('ProtocolVersion', Byte),
			('Username', Unicode),
			('ServerHost', Unicode),
			('ServerPort', Int)
		])

	class ChatMessage(Packet):
		id = 0x03
		members = OrderedDict([
			('Message', Unicode)
		])

	class TimeUpdate(Packet):
		id = 0x04
		members = OrderedDict([
			('WorldAge', Long),
			('DayTime', Long)
		])

	class EntityEquipment(Packet):
		id = 0x05
		members = OrderedDict([
			('ID', Int),
			('Slot', Short),
			('Item', types.Slot)
		])

	class SpawnPosition(Packet):
		id = 0x06
		members = OrderedDict([
			('X', Int),
			('Y', Int),
			('Z', Int)
		])

	class UseEntity(Packet):
		id = 0x07
		members = OrderedDict([
			('UserID', Int),
			('TargetID', Int),
			('MouseButton', Boolean)
		])

	class UpdateHealth(Packet):
		id = 0x08
		members = OrderedDict([
			('Health', Short),
			('Food', Short),
			('FoodSaturation', Float)
		])

	class Respawn(Packet):
		id = 0x09
		members = OrderedDict([
			('Dimension', Int),
			('Difficulty', Byte),
			('GameMode', Byte),
			('WorldHeight', Short),
			('LevelType', Unicode)
		])

	class Player(Packet):
		id = 0x0A
		members = OrderedDict([
			('OnGround', Boolean)
		])

	class PlayerPosition(Packet):
		id = 0x0B
		members = OrderedDict([
			('X', Double),
			('Y', Double),
			('Stance', Double),
			('Z', Double),
			('OnGround', Boolean)
		])

	class PlayerLook(Packet):
		id = 0x0C
		members = OrderedDict([
			('Yaw', Float),
			('Pitch', Float),
			('OnGround', Boolean)
		])

	class PlayerPositionAndLook(Packet):
		id = 0x0D
		members = OrderedDict([
			('X', Double),
			('Y', Double),
			('Stance', Double),
			('Z', Double),
			('Yaw', Float),
			('Pitch', Float),
			('OnGround', Boolean)
		])

	class PlayerDigging(Packet):
		id = 0x0E
		members = OrderedDict([
			('Status', Byte),
			('X', Int),
			('Y', Byte),
			('Z', Int),
			('Face', Byte)
		])

	class PlayerBlockPlacement(Packet):
		id = 0x0F
		members = OrderedDict([
			('X', Int),
			('Y', UByte),
			('Z', Int),
			('Direction', Byte),
			('Item', types.Slot),
			('OnGround', Boolean),
			('CursorX', Byte),
			('CursorY', Byte),
			('CursorZ', Byte)
		])

	class HeldItemChange(Packet):
		id = 0x10
		members = OrderedDict([
			('SlotID', Short)
		])

	class ServerListPing(Packet):
		id = 0xFE
		members = OrderedDict([
			('Magic', Byte)
		])
