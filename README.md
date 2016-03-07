# THE-GRID
A Cyberpunk MUD!

Inspiration:
 - http://www.libraryofbabel.info
 - No Man's Sky

THE GRID is an infinite matrix of areas, or rooms. There may be a practical limit on Python 3's integers of 9,223,372,036,854,775,807. Square that number to get the maximum number of rooms, and...

> 85070591730234615847396907784232501249

I don't think players are limited in choice! If a player explored one room per second, it would take (much: 2e20x) longer than the age of the universe to explore everything!

Database constrains us to 2^32 rooms (which would take 136.2 years to explore), however one can always add more databases.

To run yourself, `docker-compose run grid python grid.py`

To run it on a server, as I do, create a `grid` user account, and make their login shell either `grid.py` or `login.sh`. `login.sh` spawns a new docker container for each login. It's about 20MB per login overhead for peace of mind.
