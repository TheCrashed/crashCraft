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

	def __init__(self, size, format, endian=DEFAULT_ENDIAN, sign=SIGNED):
		self.size = size
		self.format = format
		self.endian = endian
		self.sign = sign

	def frombuffer(self, buffer):
		return self.fromstring(buffer.read(self.size))

	def tobuffer(self, value, buffer):
		buffer.write(self.tostring(value))

	def fromstring(self, value):
		if len(value) < self.size:
			raise EOFError
		return struct.unpack(self.get_struct_format(), value)[0]

	def tostring(self, value):
		return struct.pack(self.get_struct_format(), value)

	def get_struct_format(self):
		return self.endian + (self.format.lower() if self.sign else self.format.upper())

class ByteArray_Type(JavaType):
	def __init__(self):
		pass

	def frombuffer(self, buffer, size):
		self.size = size
		return self.fromstring(buffer.read(size))

	def fromstring(self, value):
		if len(value) < size:
			raise EOFError
		return value

	def tobuffer(self, value, buffer):
		buffer.write(self.tostring(value))

	def tostring(self, value):
		return value

class String_Type(ByteArray_Type):
	encoding = 'ascii'

	def frombuffer(self, buffer):
		self.size = Short.frombuffer(buffer)
		return self.fromstring(buffer.read(self.size))

	def fromstring(self, value):
		if len(value) < self.size:
			raise EOFError
		return value[:self.size]

	def tobuffer(self, value, buffer):
		buffer.write(self.tostring(value))

	def tostring(self, value):
		return Short.tostring(len(value)) + value

class Unicode_Type(String_Type):
	encoding = 'UTF-16-BE'

	def frombuffer(self, buffer):
		self.size = Short.frombuffer(buffer) * 2
		return self.fromstring(buffer.read(self.size))

	def fromstring(self, value):
		if len(value) < self.size:
			raise EOFError

		return unicode(value[:self.size], encoding=self.encoding)

	def tobuffer(self, value, buffer):
		buffer.write(self.tostring(value))

	def tostring(self, value):
		return Short.tostring(len(value)) + value.encode(self.encoding)


Byte = JavaType(
	size = 1,
	format = 'b'
)

UByte = JavaType(
	size = Byte.size,
	format = Byte.format,
	sign = UNSIGNED
)

Boolean = JavaType(
	size = UByte.size,
	format = UByte.format,
	sign = UByte.sign
)

Short = JavaType(
	size = 2,
	format = 'h'
)

UShort = JavaType(
	size = Short.size,
	format = Short.format,
	sign = UNSIGNED
)

Int = JavaType(
	size = 4,
	format = 'i'
)

Uint = JavaType(
	size = Int.size,
	format = Int.format,
	sign = UNSIGNED
)

Long = JavaType(
	size = 8,
	format = 'q'
)

ULong = JavaType(
	size = Long.size,
	format = Long.format,
	sign = UNSIGNED
)

Float = JavaType(
	size = 4,
	format = 'f'
)

UFloat = JavaType(
	size = Float.size,
	format = Float.format,
	sign = UNSIGNED
)

Double = JavaType(
	size = 8,
	format = 'd'
)

UDouble = JavaType(
	size = Double.size,
	format = Double.format,
	sign = UNSIGNED
)

ByteArray = ByteArray_Type()
String = String_Type()
Unicode = Unicode_Type()
