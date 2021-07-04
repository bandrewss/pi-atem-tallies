#!/usr/bin/python3

import time
import tally_common as tc

def main():
	tc.init_leds()

	for i in range(3):
		tc.PROGRAM_LED.on()
		time.sleep(.5)
		tc.PROGRAM_LED.off()
		time.sleep(.5)
	#FOR
#DEF

if __name__ == "__main__":
	main()
#IF
