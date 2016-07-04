#!/bin/bash
echo "Loading..."
/usr/local/bin/docker-compose -f /home/grid/THE-GRID/docker-compose.yml run grid python grid.py
