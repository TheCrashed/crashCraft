from collections import OrderedDict

from ...util.javatypes import *
from . import types
from . import Packet


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
	id = 0x0FFF
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

class Animation(Packet):
	id = 0x12
	members = OrderedDict([
		('ID', Int),
		('Animation', Byte)
	])

class EntityAction(Packet):
	id = 0x13
	members = OrderedDict([
		('ID', Int),
		('ActionID', Byte)
	])

class SpawnNamedEntity(Packet):
	id = 0x14
	members = OrderedDict([
		('ID', Int),
		('Username', Unicode),
		('X', Int),
		('Y', Int),
		('Z', Int),
		('Yaw', Byte),
		('Pitch', Byte),
		('Item', Short),
		('Metadata', ByteArray)
	])

class SpawnObject(Packet):
	id = 0x17
	members = OrderedDict([
		('ID', Int),
		('Type', Byte),
		('X', Int),
		('Y', Int),
		('Z', Int),
		('ObjectData', ByteArray),
	])

class SpawnMob(Packet):
	id = 0x18
	members = OrderedDict([
		('ID', Int),
		('Type', Byte),
		('X', Int),
		('Y', Int),
		('Z', Int),
		('Yaw', Byte),
		('Pitch', Byte),
		('HeadYaw', Byte),
		('VelocityX', Int),
		('VelocityY', Int),
		('VelocityZ', Int),
		('Metadata', ByteArray)
	])

class Entity(Packet):
	id = 0x1E
	members = OrderedDict([
		('ID', Int)
	])

class EntityRelativeMove(Packet):
	id = 0x1F
	members = OrderedDict([
		('ID', Int),
		('dX', Byte),
		('dY', Byte),
		('dZ', Byte)
	])

class EntityLook(Packet):
	id = 0x20
	members = OrderedDict([
		('ID', Int),
		('Yaw', UByte),
		('Pitch', UByte)
	])

class EntityLookAndRelativeMove(Packet):
	id = 0x21
	members = OrderedDict([
		('ID', Int),
		('dX', Byte),
		('dY', Byte),
		('dZ', Byte),
		('Yaw', UByte),
		('Pitch', UByte)
	])

class EntityTeleport(Packet):
	id = 0x22
	members = OrderedDict([
		('ID', Int),
		('X', Int),
		('Y', Int),
		('Z', Int),
		('Yaw', UByte),
		('Pitch', UByte)
	])

class EntityHeadLook(Packet):
	id = 0x23
	members = OrderedDict([
		('ID', Int),
		('Yaw', UByte)
	])

class EntityStatus(Packet):
	id = 0x26
	members = OrderedDict([
		('ID', Int),
		('Status', Byte)
	])

class EntityMetadata(Packet):
	id = 0x28
	members = OrderedDict([
		('ID', Int),
		('Metadata', ByteArray)
	])

class EntityEffect(Packet):
	id = 0x29
	members = OrderedDict([
		('ID', Int),
		('EffectID', Byte),
		('Amplifier', Byte),
		('Duration', Short)
	])

class RemoveEntityEffect(Packet):
	id = 0x2A
	members = OrderedDict([
		('ID', Int),
		('EffectID', Byte)
	])

class SetExperience(Packet):
	id = 0x2B
	members = OrderedDict([
		('ExperienceBar', Float),
		('Level', Short),
		('TotalExperience', Short)
	])

class ChunkData(Packet):
	id = 0x33
	members = OrderedDict([
		('X', Int),
		('Z', Int),
		('GroundUp', Boolean),
		('PrimaryBitMap', UShort),
		('AddBitMap', UShort),
		('CompressedSize', Int),
		('CompressedData', ByteArray)
	])

class BlockChange(Packet):
	id = 0x35
	members = OrderedDict([
		('X', Int),
		('Y', UByte),
		('Z', Int),
		('BlockType', Short),
		('BlockMetadata', Byte),
	])

class SoundOrParticleEffect(Packet):
	id = 0x3D
	members = OrderedDict([
		('ID', Int),
		('X', Int),
		('Y', Byte),
		('Z', Int),
		('Data', Int),
		('DisableRelativeVolume', Boolean),
	])

class NamedSoundEffect(Packet):
	id = 0x3E
	members = OrderedDict([
		('SoundName', Unicode),
		('X', Int),
		('Y', Int),
		('Z', Int),
		('Volume', Float),
		('Pitch', Byte),
	])

class ClientSettings(Packet):
	id = 0xCC
	members = OrderedDict([
		('Locale', Unicode),
		('ViewDistance', Byte),
		('ChatFlags', Byte),
		('Difficulty', Byte),
		('ShowCape', Boolean)
	])

class PlayerAbilities(Packet):
	id = 0xCA
	members = OrderedDict([
		('Flags', Byte),
		('FlyingSpeed', Byte),
		('WalkingSpeed', Byte),
	])

class ClientStatuses(Packet):
	id = 0xCD
	members = OrderedDict([
		('Payload', Byte)
	])

class EncryptionKeyResponse(Packet):
	id = 0xFC
	members = OrderedDict([
		('SharedSecret', String),
		('VerifyToken', String)
	])

class EncryptionKeyRequest(Packet):
	id = 0xFD
	members = OrderedDict([
		('ServerID', Unicode),
		('PublicKey', String),
		('VerifyToken', String)
	])

class ServerListPing(Packet):
	id = 0xFE
	members = OrderedDict([
		('Magic', Byte)
	])

class Disconnect(Packet):
	id = 0xFF
	members = OrderedDict([
		('Reason', Unicode)
	])
