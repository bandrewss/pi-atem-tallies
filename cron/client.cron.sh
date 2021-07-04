#!/bin/sh

CONFIG=$1

REPO='/home/pi/pi-atem-tallies'

${REPO}/src/start_signal.py

${REPO}/src/tally_client.py ${CONFIG}

${REPO}/src/crash_signal.py
