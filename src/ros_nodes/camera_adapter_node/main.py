import rospy
import std_msgs.msg as ros_std_msgs
import sys
import cv2
import pickle
import base64
import time
import lib.ros as ros_man



# module config
_NODE_NAME = 'camera_adapter_node'

# module state
_camera_adapter = cv2.VideoCapture(0)
#time.sleep(2)
#if not _camera_adapter.isOpened():
#        print("Error: Could not open camera.")

#_camera_adapter.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Important for some camera modules
#_camera_adapter.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'RGB3'))
#_camera_adapter.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))  # Set MJPEG codec

# Get and print supported resolutions
#width = _camera_adapter.get(cv2.CAP_PROP_FRAME_WIDTH)
#height = _camera_adapter.get(cv2.CAP_PROP_FRAME_HEIGHT)
#print(f"Default resolution: {width}x{height}")

# Try setting a supported resolution (adjust as needed)
#_camera_adapter.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#_camera_adapter.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
#_camera_adapter.set(cv2.CAP_PROP_FPS, 15)

print("adapter set")
ret, frame = _camera_adapter.read()
print(frame.shape)
_cam_feed_pub: rospy.Publisher = None
_settings_obj: dict = None


def ros_node_setup():
    global _cam_feed_pub
    global _cam_live_feed_pub

    is_init = ros_man.init_node(_NODE_NAME)

    if not is_init:
        sys.exit()


    topic_id = ros_man.create_topic_id('camera_feed')
    topic_id_live = ros_man.create_topic_id("camera_live_feed")
    q_size: int = 10

    _cam_feed_pub = rospy.Publisher(
        topic_id, ros_std_msgs.String, queue_size=q_size)
    _cam_live_feed_pub = rospy.Publisher(topic_id_live, ros_std_msgs.String, queue_size=q_size)


def ros_node_loop():
    # read frame
    print("loop")
    cap_success, frame = _camera_adapter.read()
    print(cap_success)
    print(frame.shape)

    if not cap_success:
        return
    # frame = cv2.resize(frame, (400, 400))
    
    # compress frame
    _, compressed_frame = cv2.imencode(
        '.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])

    # convert frame to binary data
    bin_frame = pickle.dumps(compressed_frame, pickle.HIGHEST_PROTOCOL)

    # base64 encode frame
    encoded_bin_frame = base64.b64encode(bin_frame).decode()

    # publish frame in ROS
    _cam_feed_pub.publish(encoded_bin_frame)

    # compress frame
    _, compressed_frame = cv2.imencode(
        '.jpg', cv2.resize(frame, (400,400)), [cv2.IMWRITE_JPEG_QUALITY, 90])

    # convert frame to binary data
    bin_frame = pickle.dumps(compressed_frame, pickle.HIGHEST_PROTOCOL)

    # base64 encode frame
    encoded_bin_frame = base64.b64encode(bin_frame).decode()

    # publish frame in ROS
    _cam_live_feed_pub.publish(encoded_bin_frame)
