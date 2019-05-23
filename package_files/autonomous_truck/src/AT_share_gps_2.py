#!/usr/bin/env python

import socket
import pickle
import rospy
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix, Imu
import math
from tf.transformations import euler_from_quaternion

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

                orientation_list = [orientation_data.orientation.x, orientation_data.orientation.y, orientation_data.orientation.z, orientation_data.orientation.w]
                (roll, pitch, yaw) = euler_from_quaternion (orientation_list)

                x_cart = math.cos(math.radians(gps_data.longitude))*math.cos(math.radians(gps_data.latitude))
                y_cart = math.sin(math.radians(gps_data.longitude))*math.cos(math.radians(gps_data.latitude))
                z_cart = math.sin(math.radians(gps_data.latitude))

                x_cart = (-1) * (x_cart + 2*0.00002855802)
                y_cart = y_cart - 2*0.000024051
                z_cart = (1) * (z_cart)

                new_latitude = math.degrees(math.asin(z_cart)) 
                new_longitude = math.degrees(math.atan2(y_cart, x_cart))
                
                data_string = (str(new_latitude) + " " + str(new_longitude-37) + " "
			            + str(roll) + " " + str(pitch) + " " + str(yaw))
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
