#!/usr/bin/python3

import time
import tally_common as tc

def main():
	tc.init_leds()

	while 1:
		tc.PREVIEW_LED.on()
		time.sleep(.2)
		tc.PREVIEW_LED.off()
		time.sleep(.2)
	#FOR
#DEF

if __name__ == "__main__":
	main()
#IF
