# autopep8: off
import time
import rospy
import sys
import os

sys.path.append(os.getcwd())

# change this

import main as picamera2_adapter_node



# change this
_NODE_DELAY = 0.05  # 50ms delay / operation frequency 20Hz


if __name__ == '__main__':
    # change this
    picamera2_adapter_node.ros_node_setup()

    while True:
        if rospy.is_shutdown():
            break

        try:
            # change this
            picamera2_adapter_node.ros_node_loop()

        except rospy.ROSInterruptException:
            break

        time.sleep(_NODE_DELAY)
