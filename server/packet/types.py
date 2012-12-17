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
	def __init__(self, data):
		self.data = data

	def frombuffer(self, buffer):
		id = Short.frombuffer(buffer)

		if id == -1:
			return None

		count = Byte.frombuffer(buffer)
		damage = Short.frombuffer(buffer)
		data_length = Short.frombuffer(buffer)

		return OrderedDict(
			ID = id,
			Count = count,
			Damage = damage,
			Data = None
		)

	def tostring(self):
		data = self.data

		if data == -1:
			return Byte.tostring(-1)

		ID, Count, Damage = data

		return ''.join((
			Short.tostring(ID),
			Byte.tostring(Count),
			Short.tostring(Damage),
			Short.tostring(-1)
		))
