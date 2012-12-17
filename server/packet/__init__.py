class PartialPacketException(Exception):
	pass

class UnknownPacketException(Exception):
	pass

class CorruptPacketException(Exception):
	pass


from .packet import Packet
from . import packets
from . import types
