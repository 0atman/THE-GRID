def command_parser(grid, *args):
    commands = {
        'help': help,
        'status': grid.world.get
    }
    command = args[0]
    if commands.get(command):
        return commands[command](*args[1:])
    else:
        return "{}: command not found".format(command)
