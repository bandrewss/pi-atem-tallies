#!/usr/bin/python3

#builtin
import time
import random
import json

# third party
import zmq
import PyATEMMax

# local
import tally_common as tc


def create_tally_payload(switcher, max_cameras):
    payload = [tc.IN_THE_HOLE] * (max_cameras + 1)

    if tc.ARGS.demo:
        program_cam = random.randrange(1, len(payload))
        preview_cam = random.randrange(1, len(payload))
    else:
        program_cam = switcher.programInput[0].videoSource.value
        preview_cam = switcher.previewInput[0].videoSource.value
    #IF


    if preview_cam < len(payload):
       payload[preview_cam] = tc.ON_DECK
    #IF

    if program_cam < len(payload):
        payload[program_cam] = tc.AT_BAT
    #IF

    tc.LOGGER.debug("Active Camera: {}".format(program_cam))
    tc.LOGGER.debug("Preview Camera {}".format(preview_cam))

    
    return payload

#DEF

def main():
    tc.init()

    server_conf = tc.CONFIG["server"]
    topic = server_conf["topic"]
    max_cameras = server_conf["max_cameras"]
    sleep_time = server_conf["sleep"]
    switcher_host = server_conf["switcher_host"]

    tc.LOGGER.info("Current libzmq version is: {}".format(zmq.zmq_version()))
    tc.LOGGER.info("Current pyzmq version is: {}".format(zmq.__version__))

    if tc.ARGS.demo:
        tc.LOGGER.debug("Running in demo mode")
        switcher = None
    else:
        tc.LOGGER.info("Connecting to switcher at {}".format(switcher_host))
        switcher = PyATEMMax.ATEMMax()
        switcher.connect(switcher_host)
        switcher.waitForConnection()
    #IF

    context = zmq.Context()
    socket = context.socket(zmq.PUB)

    bind = "{}://{}:{}".format(server_conf["protocol"], server_conf["host"], server_conf["port"])
    tc.LOGGER.debug("ZMQ binding to {}".format(bind))
    socket.bind(bind)

    while 1:
        payload = create_tally_payload(switcher, max_cameras)

        socket.send_string("{} {}".format(topic, json.dumps(payload)))

        tc.LOGGER.debug("==SLEEP== [{}]".format(sleep_time))
        time.sleep(sleep_time)
    #WHILE

    return 1
#DEF


if __name__ == "__main__":
    exit(main())
#IF
