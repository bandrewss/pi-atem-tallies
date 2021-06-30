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

    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    connect = "{}://{}:{}".format(client_conf["protocol"], client_conf["hosts"][0], client_conf["port"])

    _LOG.info("Connecting to tally server: {}".format(connect))
    socket.connect(connect)

    _LOG.info("Subscribing to {}".format(topic))
    socket.setsockopt_string(zmq.SUBSCRIBE, topic)

    camera_on = False
    _LOG.info("[OFF]")
    for current in range(16):
        string = socket.recv_string()

        payload = json.loads(string[len(topic) +1:])

        if payload[client_conf["camera_number"]] != camera_on:
            camera_on = payload[client_conf["camera_number"]]
            
            if camera_on:
                _LOG.info("[ON]")
            else:
                _LOG.info("[OFF]")
            #IF
        #IF
    #FOR

#DEF

if __name__ == "__main__":
    exit(main())
#IF
