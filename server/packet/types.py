from collections import OrderedDict

from ...util.javatypes import *


class CustomType():
	def frombuffer(self, buffer):
		pass

	def tobuffer(self, value, buffer):
		pass

	def fromstring(self, value):
		pass

	def tostring(self, value):
		pass


class Slot(CustomType):
	@staticmethod
	def frombuffer(self, buffer):
		id = javatypes.Short.frombuffer(buffer)
		if id == -1:
			return None

		count = javatypes.Byte.frombuffer(buffer)
		damage = javatypes.Short.frombuffer(buffer)
		data_length = javatypes.Short.frombuffer(buffer)

		return OrderedDict(
			ID = id,
			Count = count,
			Damage = damage,
			Data = None
		)
