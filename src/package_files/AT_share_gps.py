#!/usr/bin/env python

import socket
import pickle
import rospy
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix, Imu
import math
from tf.transformations import euler_from_quaternion

# def callback(data, args):
#     sock = args
#     # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.longitude)

#     print("heloo")
#     c, addr = sock.accept()
#     print 'Got connection from', addr
#     print(str(data.longitude))

#     c.send(str(data.longitude))
#     # c.close()

# class Location:
#     def __init__(self):
#         self.latitude = 0
#         self.longitude = 0
#         self.altitude = 0


def main():
    s = socket.socket()
    print "Socket successfully created"
    port = 12345

    s.bind(('', port))
    print "socket binded to %s" % (port)

    s.listen(5)
    print "socket is listening"

    try:
        rospy.init_node('share_truck_data')

        rospy.wait_for_service('/autonomous_truck/gps/enable')
        rospy.wait_for_service('/autonomous_truck/inertial_unit/enable')
        try:
            print("service catched")
            # rospy.Subscriber("/autonomous_truck/gps/values", NavSatFix, callback, (s))
            # variable = Location()
            while(True):
                gps_data = rospy.wait_for_message(
                    "/autonomous_truck/gps/values", NavSatFix, timeout=1)
                orientation_data = rospy.wait_for_message(
                    "/autonomous_truck/inertial_unit/roll_pitch_yaw", Imu, timeout=1)

                c, addr = s.accept()
                print 'Got connection from', addr

                new_latitude = (gps_data.latitude+103)*0.0000142
                new_longitude = (gps_data.longitude-229)*0.0000142
                    # (111111*math.degrees((math.cos(gps_data.longitude))))

                orientation_list = [orientation_data.orientation.x, orientation_data.orientation.y, orientation_data.orientation.z, orientation_data.orientation.w]
                (roll, pitch, yaw) = euler_from_quaternion (orientation_list)

                data_string = (str(new_latitude) + " " + str(new_longitude) + " " + str(roll) + " " + str(
                    pitch) + " " + str(yaw))
                print(data_string)

                c.send(data_string)

            c.close()

        except rospy.ServiceException, e:
            print "Service call failed: %s" % e

        # rospy.spin()

    except KeyboardInterrupt:
        # s.close()
        rospy.signal_shutdown("KeyboardInterrupt")
        raise


if __name__ == '__main__':
    main()
