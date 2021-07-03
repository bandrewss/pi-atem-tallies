#!/usr/bin/python3

# builtin
import sys
import json

# third party
import zmq

# local
import tally_common as tc

def state_action(state):
    if state == tc.AT_BAT:
        tc.LOGGER.info("Camera Tally [PROGRAM]")
    elif state == tc.ON_DECK:
        tc.LOGGER.info("Camera Tally [PREVIEW]")
    else:
        tc.LOGGER.info("Camera Tally [OFF]")
    #IF
#DEF

def main():
    tc.init()

    client_conf = tc.CONFIG["client"]
    topic = client_conf["topic"]

    tc.LOGGER.info("Current libzmq version is: {}".format(zmq.zmq_version()))
    tc.LOGGER.info("Current pyzmq version is: {}".format(zmq.__version__))
    tc.LOGGER.info("Configured for Camera {}".format(client_conf["camera_number"]))

    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    connect = "{}://{}:{}".format(client_conf["protocol"], client_conf["host"], client_conf["port"])

    tc.LOGGER.info("Connecting to tally server: {}".format(connect))
    socket.connect(connect)

    tc.LOGGER.info("Subscribing to {}".format(topic))
    socket.setsockopt_string(zmq.SUBSCRIBE, topic)

    current_state = -1
    while 1:
        string = socket.recv_string()

        payload = json.loads(string[len(topic) +1:])
        state = payload[client_conf["camera_number"]]

        if state == current_state:
            continue
        #IF

        state_action(state)

        current_state = state
    #FOR

#DEF

if __name__ == "__main__":
    exit(main())
#IF
