import rospy
import std_msgs.msg as ros_std_msgs
import sys
import cv2
import base64
import pickle
from datetime import datetime
from sensor_msgs.msg import NavSatFix
import lib.ros as ros_man
from lib.myDrone import MyDrone


# module config
_NODE_NAME = 'frames_saving_node'

counter = 0
drone=MyDrone()
# ros msgs handlers
def _ros_frame_reader(msg: ros_std_msgs.String):
    global counter
    global drone
    input_bin_stream = msg.data.encode()

    # base64 decode
    decoded_bin_frame = base64.b64decode(input_bin_stream)

    # recover frame from binary stream
    frame = pickle.loads(decoded_bin_frame)

    # decode JPEG frame
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    GPS=NavSatFix()
    GPS=drone.getGPS()
    lat=GPS.latitude
    long=GPS.longitude
    alt=GPS.altitude
    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"saved frame_lat_{lat}_long_{long}_alt_{alt}_{current_timestamp}.jpg")
    cv2.imwrite(f'/home/pi/frames/frame_lat_{lat}_long_{long}_alt_{alt}_{current_timestamp}.jpg', frame)


def ros_node_setup():
    is_init = ros_man.init_node(_NODE_NAME)

    if not is_init:
        sys.exit()

    topic_id = ros_man.compute_topic_id(
        'camera_adapter_node', 'camera_feed')
   
    rospy.Subscriber(topic_id, ros_std_msgs.String, _ros_frame_reader)


def ros_node_loop():
    pass
