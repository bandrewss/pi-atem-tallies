
# built in
import argparse
import json
import logging
import socket
from logging.handlers import RotatingFileHandler

# camera op didn't understand code
# I didn't understand camera
# we could agree on baseball
IN_THE_HOLE = 0 # No Tally
ON_DECK = 1     # Preview Tally
AT_BAT = 2      # Program Tally

PROGRAM_LED_NUM = 24
PREVIEW_LED_NUM = 23


def init():
    init_leds()
    load_args()
    load_config()
    load_logger()
#DEF

def init_leds():
    global ON_PI
    global PROGRAM_LED
    global PREVIEW_LED

    try:
        from gpiozero import LED
        PROGRAM_LED = LED(PROGRAM_LED_NUM)
        PREVIEW_LED = LED(PREVIEW_LED_NUM)
        ON_PI = True
    except ModuleNotFoundError:
        ON_PI = False
    #TRY
#DEF

def load_args():
    global ARGS

    parser = argparse.ArgumentParser(description="Tally Light Controller")

    parser.add_argument("config_file", help="The location of the config file",
            nargs="?")
    parser.add_argument("--demo", help="Run in demo mode",
            action="store_true", default=False)

    ARGS = parser.parse_args()

    if ARGS.config_file is None:
        ARGS.config_file = "config.json"
    #IF

#DEF

def load_config():
    global CONFIG

    with open(ARGS.config_file) as json_file:
        print("AM HERE")
        CONFIG = json.load(json_file)
    #WITH
#DEF

def load_logger():
    global LOGGER

    log_config = CONFIG["logging"]

    try:
        hostname = socket.gethostname()
    except:
        hostname = "tally"
    #TRY

    LOGGER = logging.getLogger(hostname)
    LOGGER.setLevel(logging.DEBUG)


    log_format = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")

    stdout = logging.StreamHandler()
    stdout.setFormatter(log_format)

    rotating_file = RotatingFileHandler(log_config["filename"], mode="a",
            maxBytes=log_config["filesize"], backupCount=1)
    rotating_file.setFormatter(log_format)

    LOGGER.addHandler(stdout)
    LOGGER.addHandler(rotating_file)
#DEF

def set_led(state):
    if not ON_PI:
        return
    #IF

    PROGRAM_LED.off()
    PREVIEW_LED.off()

    if state == AT_BAT:
        PROGRAM_LED.on()
    elif state == ON_DECK:
        PREVIEW_LED.on()
    #IF
#DEF
