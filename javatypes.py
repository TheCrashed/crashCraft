import struct


BIG_ENDIAN = '!'
LITTLE_ENDIAN = '<'
DEFAULT_ENDIAN = BIG_ENDIAN

SIGNED = True
UNSIGNED = False


class JavaType():
	size = None
	format = None
	endian = DEFAULT_ENDIAN
	sign = SIGNED

	def __call__(self, data, *args):
		if hasattr(data, 'read'):
			return self.read(data, *args)
		return self.write(data, *args)

	def read(self, stream):
		return struct.unpack(self.get_struct_format(), stream.read(self.size))[0]

	def write(self, value):
		return struct.pack(self.get_struct_format(), value)

	def get_struct_format(self):
		return self.endian + (self.format.lower() if self.sign else self.format.upper())


class Byte(JavaType):
	size = 1
	format = 'b'

class UByte(Byte):
	sign = UNSIGNED

class Boolean(UByte):
	pass

class Short(JavaType):
	size = 2
	format = 'h'

class UShort(Short):
	sign = UNSIGNED

class Int(JavaType):
	size = 4
	format = 'i'

class UInt(Int):
	sign = UNSIGNED

class Long(JavaType):
	size = 8
	format = 'q'

class ULong(Long):
	sign = SIGNED

class Float(JavaType):
	size = 4
	format = 'f'

class UFloat(Float):
	sign = UNSIGNED

class Double(JavaType):
	size = 8
	format = 'd'

class UDouble(Double):
	sign = UNSIGNED

class ByteArray(JavaType):
	@staticmethod
	def read(stream, length):
		return stream.read(length)

	@staticmethod
	def write(value):
		return value

class String(ByteArray):
	@staticmethod
	def read(stream):
		return BYTEARRAY(stream, SHORT(stream))

	@staticmethod
	def write(value):
		return SHORT(len(value)) + value

class Unicode(ByteArray):
	@staticmethod
	def read(stream):
		return unicode(BYTEARRAY(stream, SHORT(stream) * 2), encoding='UTF-16-BE')

	@staticmethod
	def write(value):
		return SHORT(len(value)) + value.encode('UTF-16-BE')


BYTE = Byte()
UBYTE = UByte()
BOOLEAN = Boolean()
SHORT = Short()
USHORT = UShort()
INT = Int()
UINT = UInt()
LONG = Long()
ULONG = ULong()
FLOAT = Float()
UFLOAT = UFloat()
DOUBLE = Double()
UDOUBLE = UDouble()
BYTEARRAY = ByteArray()
STRING = String()
UNICODE = Unicode()
