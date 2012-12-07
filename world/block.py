


class Block():
	__slots__ = ('id', 'name')

	id = None
	name = None

	def __init__(self, id, name):
		self.id = id
		self.name = name


class Blocks():
	Air = Block(0x0000, 'Air')
	Stone = Block(0x0001, 'Stone')
	Grass = Block(0x0002, 'Grass')
	Dirt = Block(0x0003, 'Dirt')
	Cobblestone = Block(0x0004, 'Cobblestone')
	WoodenPlanks = Block(0x0005, 'Wooden Planks')
	Saplings = Block(0x0006, 'Saplings')
	Bedrock = Block(0x0007, 'Bedrock')
	Water = Block(0x0008, 'Bedrock')
	StationaryWater = Block(0x0009, 'Stationary Water')
	Lava = Block(0x000A, 'Lava')
	StationaryLava = Block(0x000B, 'Stationary Lava')
	Sand = Block(0x000C, 'Sand')
	Gravel = Block(0x000D, 'Gravel')
	GoldOre = Block(0x000E, 'Gold Ore')
	IronOre = Block(0x000F, 'Iron Ore')
	CoalOre = Block(0x0010, 'Coal Ore')
	Wood = Block(0x0011, 'Wood')
	Leaves = Block(0x0012, 'Leaves')
	Sponge = Block(0x0013, 'Sponge')
	Glass = Block(0x0014, 'Glass')
	LapisLazuliOre = Block(0x0015, 'Lapis Lazuli Ore')
	LapisLazuliBlock = Block(0x0016, 'Lapis Lazuli Block')
	Dispenser = Block(0x0017, 'Dispenser')
	Sandstone = Block(0x0018, 'Sandstone')
	NoteBlock = Block(0x0019, 'Note Block')
	Bed = Block(0x001A, 'Bed')
	PoweredRail = Block(0x001B, 'Powered Rail')
	DetectorRail = Block(0x001C, 'Detector Rail')
	StickyPiston = Block(0x001D, 'Sticky Piston')
	Cobweb = Block(0x001E, 'Cobweb')
	TallGrass = Block(0x001F, 'TaillGrass')
	DeadBush = Block(0x0020, 'Dead Bush')
	Piston = Block(0x0021, 'Piston')
	PistonExtension = Block(0x0022, 'Piston Extension')
	Wool = Block(0x0023, 'Wool')
	PistonBlockMoved = Block(0x0024, 'Piston Block Moved')
