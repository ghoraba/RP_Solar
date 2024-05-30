import rospy
import std_msgs.msg as ros_std_msgs
import sys
import pickle
import base64
import time
import cv2

from picamera2 import Picamera2

import lib.ros as ros_man
import lib.settings as set_man


# Module config and state
_NODE_NAME = 'camera_adapter_node'
_cam_feed_pub = None
_settings_obj = None
picam2 = None  # Declare picam2 globally


def ros_node_setup():
    global picam2, _settings_obj

    # ROS node initialization (using ros_man)
    is_init = ros_man.init_node(_NODE_NAME)
    if not is_init:
        sys.exit()

    # Load settings (using set_man)
    _settings_obj = set_man.get_settings()

    # Configure ROS publisher (using ros_man)
    topic_id = ros_man.create_topic_id('camera_feed')
    q_size = _settings_obj['ros']['msg_queue_size']
    _cam_feed_pub = rospy.Publisher(topic_id, ros_std_msgs.String, queue_size=q_size)
   
    # Initialize the picamera2
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"size": (400, 400)})  # Resize to 400x400 directly
    picam2.configure(camera_config)
    picam2.start()


def ros_node_loop():
    c = 0
    # read frame
    global picam2, _cam_feed_pub
    
    # Capture frame with picamera2
    frame = picam2.capture_array('main')

    # save the image to ~/images
    picam2.save_image('main', '/home/ubuntu/images', f'image_{c}.jpg')
    c+=1

    # Compress frame
    _, compressed_frame = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])

    # Rest of your frame processing (pickle, base64 encoding)
    bin_frame = pickle.dumps(compressed_frame, pickle.HIGHEST_PROTOCOL)

    # Base64 encode frame
    encoded_bin_frame = base64.b64encode(bin_frame).decode()

    # Publish frame in ROS
    _cam_feed_pub.publish(encoded_bin_frame)
