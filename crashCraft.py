import server
import server.factory

import world

def run():
	world = world.World()
	factory = server.factory.MinecraftFactory()
	factory.world = world

	server.reactor.listenTCP(25565, factory)
	server.reactor.run()


if __name__ == '__main__':
	run()
