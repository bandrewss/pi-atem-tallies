
# built in
import argparse
import json
import logging
from logging.handlers import RotatingFileHandler

def get_args():
    parser = argparse.ArgumentParser(description="Tally Light Controller")

    parser.add_argument("config_file", help="The location of the config file",
            nargs="?")

    args = parser.parse_args()

    if args.config_file is None:
        args.config_file = "config.json"
    #IF

    return args
#DEF

def get_config(config_file):
    with open(config_file) as json_file:
        config = json.load(json_file)
    #WITH

    return config
#DEF
    
def get_logger(log_config):
    logger = logging.getLogger(log_config["name"])
    logger.setLevel(logging.DEBUG)

    log_format = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")

    stdout = logging.StreamHandler()
    stdout.setFormatter(log_format)

    rotating_file = RotatingFileHandler(log_config["filename"], mode="a",
            maxBytes=log_config["filesize"], backupCount=1)
    rotating_file.setFormatter(log_format)


    logger.addHandler(stdout)
    logger.addHandler(rotating_file)

    return logger
#DEF
