# THE-GRID
A Cyberpunk MUD!

to run yourself, `docker-compose run grid python grid.py`

To run it on a server, as I do, create a `grid` user account, and make their login shell either `grid.py` or `login.sh`. `login.sh` spawns a new docker container for each login. It's about 20MB per login overhead for peace of mind.
