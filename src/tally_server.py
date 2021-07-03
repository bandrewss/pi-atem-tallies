#!/usr/bin/python3

#builtin
import time
import random
import json

# third party
import zmq
import PyATEMMax

# local
from tally_common import *

_LOG = None

IP = "192.168.250.240"


def create_tally_payload(active_cam):
    payload = [False] * 8
    payload[active_cam] = True

    _LOG.debug("Active Camera: {}".format(active_cam))
    
    return payload

#DEF

def main():
    global _LOG

    args = get_args()
    config = get_config(args.config_file)
    _LOG = get_logger(config["logging"])

    server_conf = config["server"]
    topic = server_conf["topic"]

    _LOG.info("Current libzmq version is: {}".format(zmq.zmq_version()))
    _LOG.info("Current pyzmq version is: {}".format(zmq.__version__))

    switcher = PyATEMMax.ATEMMax()
    switcher.connect(IP)
    switcher.waitForConnection()

    context = zmq.Context()
    socket = context.socket(zmq.PUB)

    bind = "{}://{}:{}".format(server_conf["protocol"], server_conf["host"], server_conf["port"])
    _LOG.debug("Binding to {}".format(bind))
    socket.bind(bind)

    while 1:
        #payload = create_tally_payload(random.randrange(0, 7))
        payload = [IN_THE_HOLE] * 8
        program_cam = switcher.programInput[0].videoSource.value
        preview_cam = switcher.previewInput[0].videoSource.value

        if preview_cam < len(payload):
           payload[preview_cam] = ON_DECK
        #IF

        if program_cam < len(payload):
            payload[program_cam] = AT_BAT
        #IF

        _LOG.debug("Active Camera: {}".format(program_cam))
        _LOG.debug("Preview Camera {}".format(preview_cam))

        socket.send_string("{} {}".format(topic, json.dumps(payload)))

        # get the next active camera
        _LOG.debug("sleep 1")
        time.sleep(0.1)
    #WHILE

    return 0
#DEF


if __name__ == "__main__":
    exit(main())
#IF
