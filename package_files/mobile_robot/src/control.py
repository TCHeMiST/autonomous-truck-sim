#!/usr/bin/env python

from mobile_robot.srv import *
from mobile_robot.msg import *
import rospy
from geometry_msgs.msg import Twist
import math
WHEEL_DIST_X=0.394
WHEEL_DIST_Y=0.2662
RADIUS=0.111
def client(msg):
	rospy.loginfo("Linear Components: [%f, %f, %f]"%(msg.linear.x, msg.linear.y, msg.linear.z))
	rospy.loginfo("Angular Components: [%f, %f, %f]"%(msg.angular.x, msg.angular.y, msg.angular.z))

	ang = msg.angular.z
	lin = msg.linear.x

	# if (ang and lin):
	# 	try:
	# 		velocity_left = ang*(math.sqrt((lin/ang-WHEEL_DIST_X/2)**2 + (WHEEL_DIST_Y/2)**2))/(math.cos(math.atan2(WHEEL_DIST_Y, ((lin/ang) - (WHEEL_DIST_X/2)))))/RADIUS
	# 		velocity_right = ang*(math.sqrt((lin/ang+WHEEL_DIST_X/2)**2 + (WHEEL_DIST_Y/2)**2))/(math.cos(math.atan2(WHEEL_DIST_Y, ((lin/ang) + (WHEEL_DIST_X/2)))))/RADIUS
	# 	except:
	# 		velocity_left = 0.5/RADIUS
	# 		velocity_right = 0.5/RADIUS
	# else:
	# 	velocity_right = 0.0
	# 	velocity_left = 0.0

	velocity_left=(lin+WHEEL_DIST_X*ang/2)/RADIUS
	velocity_right=(lin-WHEEL_DIST_X*ang/2)/RADIUS

	# velocity_left =  5.92 # left wheel angular speed
	# velocity_right = 3.08 # right wheel angular speed

	rospy.loginfo ("velocity_left = %f rad/sec" %velocity_left)
	rospy.loginfo ("velocity_right = %f rad/sec"%velocity_right)

	

	rospy.wait_for_service('/pioneer3at/back_right_wheel/set_velocity')
	try:
		w_rb = rospy.ServiceProxy('/pioneer3at/back_right_wheel/set_velocity', set_float)
		w_rf = rospy.ServiceProxy('/pioneer3at/front_right_wheel/set_velocity', set_float)
		w_lb = rospy.ServiceProxy('/pioneer3at/back_left_wheel/set_velocity', set_float)
		w_lf = rospy.ServiceProxy('/pioneer3at/front_left_wheel/set_velocity', set_float)
		w_rb_service = w_rb(velocity_right)  
		w_rf_service = w_rf(velocity_right)
		w_lb_service = w_lb(velocity_left)   
		w_lf_service = w_lf(velocity_left)
	except rospy.ServiceException, e:
		rospy.loginfo( "Service call failed: %s"%e)

def main():
#initialize all motors   
	p_rb = rospy.ServiceProxy('/pioneer3at/back_right_wheel/set_position', set_float)
	p_rf = rospy.ServiceProxy('/pioneer3at/front_right_wheel/set_position', set_float)
	p_lb = rospy.ServiceProxy('/pioneer3at/back_left_wheel/set_position', set_float)
	p_lf = rospy.ServiceProxy('/pioneer3at/front_left_wheel/set_position', set_float)
	p_rb_service = p_rb(float("inf"))   
	p_rf_service = p_rf(float("inf"))
	p_lb_service = p_lb(float("inf"))
	p_lf_service = p_lf(float("inf"))
	w_rb = rospy.ServiceProxy('/pioneer3at/back_right_wheel/set_velocity', set_float)
	w_rf = rospy.ServiceProxy('/pioneer3at/front_right_wheel/set_velocity', set_float)
	w_lb = rospy.ServiceProxy('/pioneer3at/back_left_wheel/set_velocity', set_float)
	w_lf = rospy.ServiceProxy('/pioneer3at/front_left_wheel/set_velocity', set_float)
	w_rb_service = w_rb(0)  
	w_rf_service = w_rf(0)
	w_lb_service = w_lb(0)   
	w_lf_service = w_lf(0)

	try:
		rospy.init_node('control_wheel')
		rospy.Subscriber("/cmd_vel", Twist, client)
		rospy.spin()
	except KeyboardInterrupt:
		rospy.signal_shutdown("KeyboardInterrupt")
	raise

if __name__ == '__main__': main()
