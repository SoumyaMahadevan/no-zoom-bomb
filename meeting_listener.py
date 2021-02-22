#!/usr/local/bin/python3

import json
import subprocess
import time

ON_MSG = {"color": "#FF00FF"}
OFF_MSG = {"pattern": "~off"}
LOOKBACK = 2


def meeting_alert():
    start_time = int(time.time()) - LOOKBACK
    proc_op = subprocess.run(
        [
            "log",
            "show",
            "--start",
            "@{}".format(start_time),
            "--style",
            "json",
            "--predicate",
            "subsystem == 'com.apple.VDCAssistant' && eventMessage contains 'Post event kCamera'",
        ],
        capture_output=True,
    )
    logs = proc_op.stdout.decode("utf-8")
    events = json.loads(logs)
    if not len(events):
        return
    last_event = events[len(events) - 1]
    if "kCameraStreamStart" in last_event["eventMessage"]:
        print(json.dumps(ON_MSG))
    elif "kCameraStreamStop" in last_event["eventMessage"]:
        print(json.dumps(OFF_MSG))


if __name__ == "__main__":
    meeting_alert()
