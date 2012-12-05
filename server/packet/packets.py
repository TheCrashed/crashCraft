from collections import OrderedDict

from . import Packet
from javatypes import *


class KeepAlive(Packet):
	id = 0x00
	members = OrderedDict([
		('ID', INT),
	])

class LoginRequest(Packet):
	id = 0x01
	members = OrderedDict([
		('EntityID', INT),
		('LevelType', UNICODE),
		('GameMode', BYTE),
		('Dimension', BYTE),
		('Difficulty', BYTE),
		('NotUsed', BYTE),
		('MaxPlayers', BYTE)
	])

class ChatMessage(Packet):
	id = 0x03
	members = OrderedDict([
		('Message', UNICODE)
	])

class Handshake(Packet):
	id = 0x02
	members = OrderedDict([
		('ProtocolVersion', BYTE),
		('Username', UNICODE),
		('ServerHost', UNICODE),
		('ServerPort', INT)
	])

class TimeUpdate(Packet):
	id = 0x04
	members = OrderedDict([
		('AgeOfWorld', LONG),
		('TimeOfDay', LONG)
	])

class EntityEquipment(Packet):
	id = 0x05
	members = OrderedDict([
		('EID', INT),
		('Slot', SHORT),
		('Item', SHORT)
	])

class SpawnPosition(Packet):
	id = 0x06
	members = OrderedDict([
		('X', INT),
		('Y', INT),
		('Z', INT)
	])

class Player(Packet):
	id = 0x0A
	members = OrderedDict([
		('OnGround', BOOLEAN)
	])

class PlayerPosition(Packet):
	id = 0x0B
	members = OrderedDict([
		('X', DOUBLE),
		('Y', DOUBLE),
		('Stance', DOUBLE),
		('Z', DOUBLE),
		('OnGround', BOOLEAN)
	])

class PlayerLook(Packet):
	id = 0x0C
	members = OrderedDict([
		('Yaw', FLOAT),
		('Pitch', FLOAT),
		('OnGround', BOOLEAN)
	])

class PlayerPositionAndLook(Packet):
	id = 0x0D
	members = OrderedDict([
		('X', DOUBLE),
		('Y', DOUBLE),
		('Stance', DOUBLE),
		('Z', DOUBLE),
		('Yaw', FLOAT),
		('Pitch', FLOAT),
		('OnGround', BOOLEAN)
	])

class PlayerDigging(Packet):
	id = 0x0E
	members = OrderedDict([
		('Status', BYTE),
		('X', INT),
		('Y', BYTE),
		('Z', INT),
		('Face', BYTE)
	])

class SpawnNamedEntity(Packet):
	id = 0x14
	members = OrderedDict([
		('EID', INT),
		('Name', UNICODE),
		('X', INT),
		('Y', INT),
		('Z', INT),
		('Yaw', BYTE),
		('Pitch', BYTE),
		('CurrentItem', SHORT),
		('Metadata', UBYTE),
		('Payload', UBYTE),
		('EndMetadata', UBYTE)
	])

class SpawnDroppedItem(Packet):
	id = 0x15
	members = OrderedDict([
		('EID', INT),
		('ItemID', SHORT),
		('ItemCount', BYTE),
		('ItemDamage', SHORT),
		('ItemData', SHORT),
		('X', INT),
		('Y', INT),
		('Z', INT),
		('Rotation', BYTE),
		('Pitch', BYTE),
		('Roll', BYTE)
	])

class Entity(Packet):
	id = 0x1E
	members = OrderedDict([
		('EID', INT)
	])

class EntityRelativeMove(Packet):
	id = 0x1F
	members = OrderedDict([
		('EID', INT),
		('dX', BYTE),
		('dY', BYTE),
		('dZ', BYTE)
	])

class EntityLook(Packet):
	id = 0x20
	members = OrderedDict([
		('EID', INT),
		('Yaw', UBYTE),
		('Pitch', UBYTE)
	])

class EntityLookAndRelativeMove(Packet):
	id = 0x21
	members = OrderedDict([
		('EID', INT),
		('dX', BYTE),
		('dY', BYTE),
		('dZ', BYTE),
		('Yaw', UBYTE),
		('Pitch', UBYTE)
	])

class EntityTeleport(Packet):
	id = 0x22
	members = OrderedDict([
		('EID', INT),
		('X', INT),
		('Y', INT),
		('Z', INT),
		('Yaw', UBYTE),
		('Pitch', UBYTE)
	])

class EntityHeadLook(Packet):
	id = 0x23
	members = OrderedDict([
		('EID', INT),
		('Yaw', UBYTE)
	])

class ChunkData(Packet):
	id = 0x33
	members = OrderedDict([
		('X', INT),
		('Z', INT),
		('GroundUp', BOOLEAN),
		('PrimaryBitMap', USHORT),
		('AddBitMap', USHORT),
		('CompressedSize', INT),
		('CompressedData', BYTEARRAY)
	])

class BlockChange(Packet):
	id = 0x35
	members = OrderedDict([
		('X', INT),
		('Y', BYTE),
		('Z', INT),
		('Type', SHORT),
		('Metadata', BYTE)
	])

class PlayerListItem(Packet):
	id = 0xC9
	members = OrderedDict([
		('Name', UNICODE),
		('Online', BOOLEAN),
		('Ping', SHORT)
	])

class ClientSettings(Packet):
	id = 0xCC
	members = OrderedDict([
		('Locale', STRING),
		('ViewDistance', BYTE),
		('ChatFlags', BYTE),
		('Difficulty', BYTE),
		('ShowCape', BOOLEAN)
	])

class ClientStatuses(Packet):
	id = 0xCD
	members = OrderedDict([
		('Payload', BYTE)
	])

class EncryptionKeyResponse(Packet):
	id = 0xFC
	members = OrderedDict([
		('SharedSecret', STRING),
		('VerifyToken', STRING)
	])

class EncryptionKeyRequest(Packet):
	id = 0xFD
	members = OrderedDict([
		('ServerID', UNICODE),
		('PublicKey', STRING),
		('VerifyToken', STRING)
	])

class ServerListPing(Packet):
	id = 0xFE
	members = OrderedDict([
		('Magic', BYTE),
	])

class Disconnect(Packet):
	id = 0xFF
	members = OrderedDict([
		('Reason', UNICODE),
	])
