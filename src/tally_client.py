#!/usr/bin/python3

# builtin
import sys
import json

# third party
import zmq

# local
from tally_common import *

def main():
    global _LOG

    args = get_args()
    config = get_config(args.config_file)
    _LOG = get_logger(config["logging"])

    client_conf = config["client"]
    topic = client_conf["topic"]

    _LOG.info("Current libzmq version is: {}".format(zmq.zmq_version()))
    _LOG.info("Current pyzmq version is: {}".format(zmq.__version__))
    _LOG.info("Configured for Camera {}".format(client_conf["camera_number"]))

    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    connect = "{}://{}:{}".format(client_conf["protocol"], client_conf["hosts"][0], client_conf["port"])

    _LOG.info("Connecting to tally server: {}".format(connect))
    socket.connect(connect)

    _LOG.info("Subscribing to {}".format(topic))
    socket.setsockopt_string(zmq.SUBSCRIBE, topic)

    current_state = -1
    while 1:
        string = socket.recv_string()

        payload = json.loads(string[len(topic) +1:])
        state = payload[client_conf["camera_number"]]

        if state == current_state:
            continue
        #IF

        if state == AT_BAT:
            _LOG.info("Camera Tally [PROGRAM]")
        elif state == ON_DECK:
            _LOG.info("Camera Tally [PREVIEW]")
        else:
            _LOG.info("Camera Tally [OFF]")
        #IF

        current_state = state
    #FOR

#DEF

if __name__ == "__main__":
    exit(main())
#IF
