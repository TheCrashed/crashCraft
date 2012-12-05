import server
import server.factory

import world


def run():
	factory = server.factory.MinecraftFactory()
	factory.world = world.MinecraftWorld(2, 2)

	factory.world.chunks[0][0].blocks[63,:,:] = 0x02
	factory.world.chunks[0][0].build_data()

	server.reactor.listenTCP(25565, factory)
	server.reactor.run()


if __name__ == '__main__':
	run()
