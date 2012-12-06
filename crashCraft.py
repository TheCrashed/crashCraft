import server
import server.factory
import server.packet
from server.packet import packets

import world

import random


class crashCraft():
	def __init__(self):
		self.factory = server.factory.MinecraftFactory()
		self.world = world.MinecraftWorld()
		self.world.root = self

		self.factory.world = self.world

		chunk = self.world.chunks[0][0]
		chunk.blocks[63,:,:] = 0x02
		chunk.build_data()

		server.reactor.listenTCP(25565, self.factory)
		server.reactor.run()

	def generate_block(self):
		self.blocks.append([random.randint(0, 15), 64 + 20, random.randint(0, 15)])

	def start_skyisfalling(self):
		self.players = []
		for client in self.factory.registered_clients:
			self.players.append(client)
		self.factory.broadcast_packet(packets.ChatMessage({'Message': '<Server> Sky Is Falling is starting, %i players: %s' % (len(self.players), ''.join(c.player.username for c in self.players))}))

		self.blocks = []

		for _ in xrange(random.randint(10, 16)):
			self.generate_block()

		for block in self.blocks:
			self.world.chunks[0][0].blocks[block[1], block[0], block[2]] = 0x01

		server.reactor.callLater(0.5, self.tick_skyisfalling)

	def tick_skyisfalling(self):
		for _ in xrange(random.randint(2, 16)):
			self.generate_block()

		for block in self.blocks:
			if self.world.chunks[0][0].blocks[block[1] - 1, block[0], block[2]] == 0x00:
				self.world.chunks[0][0].blocks[block[1], block[0], block[2]] = 0x00
				block[1] -= 1
				self.world.chunks[0][0].blocks[block[1], block[0], block[2]] = 0x01
				self.world.chunks[0][0].dirty = True

				for client in self.factory.registered_clients:
					client.player.send_chunk(0, 0)

					if client in self.players:
						if client.player.x > block[2] and client.player.x < block[2] + 1:
							if client.player.z > block[0] and client.player.z < block[0] + 1:
								if client.player.y >= block[1] - 1 and client.player.y < block[1]:
									self.factory.broadcast_packet(packets.ChatMessage({'Message': '<Server> %s WAS SQUISHED!' % client.player.username}))
									self.players.remove(client)
			else:
				self.blocks.remove(block)

		if len(self.players) == 0:
			self.factory.broadcast_packet(packets.ChatMessage({'Message': '<Server> NO WINNER!'}))
		elif len(self.players) == 1:
			self.factory.broadcast_packet(packets.ChatMessage({'Message': '<Server> %s IS THE WINNER!' % self.players[0].player.username}))
			self.blocks = []

		if len(self.blocks):
			server.reactor.callLater(0.5, self.tick_skyisfalling)



if __name__ == '__main__':
	crashCraft()
