

player = registerlogin()

update_world()



main loop
	world = getworld()
	world, player, output = update_world(world, player, input)
	world.save
	player.save
	print(output)


