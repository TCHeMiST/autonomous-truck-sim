#!/usr/bin/env python

import socket, pickle
import rospy
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix
import math

def main():
    s = socket.socket()          
    print "Socket successfully created"
    port = 12345

    s.bind(('', port))         
    print "socket binded to %s" %(port)

    s.listen(5)      
    print "socket is listening"   

    try:
        rospy.init_node('share_gps')      

        rospy.wait_for_service('/autonomous_truck/gps/enable')
        try:
            print("service catched")
            # rospy.Subscriber("/autonomous_truck/gps/values", NavSatFix, callback, (s))
            # variable = Location()
            while(True):
                data = rospy.wait_for_message("/autonomous_truck/gps/values", NavSatFix, timeout=1)
                c, addr = s.accept()      
                print 'Got connection from', addr 

                # variable = Location()
                # variable.latitude = data.latitude
                # variable.longitude = data.longitude
                # variable.altitude = data.altitude

                # variable = {
                #     "latitude": data.latitude,
                #     "longitude": data.longitude,
                #     "altitude": data.altitude
                # }

                # data_string = pickle.dumps(variable)
                new_latitude = data.latitude/111111
                new_longitude = data.longitude/(111111*(math.cos(data.longitude)))

                data_string = (str(new_latitude) + " " + str(new_longitude))
                print(data_string)
                
                c.send(data_string)

            c.close()

        except rospy.ServiceException, e:
            print "Service call failed: %s"%e
        
        # rospy.spin()
        
    except KeyboardInterrupt:
        # s.close()
        rospy.signal_shutdown("KeyboardInterrupt")
        raise

if __name__ == '__main__': main()