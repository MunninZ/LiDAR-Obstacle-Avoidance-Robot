#!/usr/bin/env python3
import rospy
from loa_bot.msg import Obstacle
from geometry_msgs.msg import Twist

# Callback method for the obstacle_detector subscriber
def obstacle_avoidace(Obstacle: Obstacle):
    
    #  Output obstacle info to console
    rospy.loginfo("Obstacle distance: " + str(Obstacle.distance) + "m")
    rospy.loginfo("Obstable angle: " + str(Obstacle.angle) + " degrees")

    # Continue traveling forward if object further than 0.25m
    if (Obstacle.distance > 0.25):
        cmd_vel_msg.linear.x = 0.15
        cmd_vel_msg.angular.z = 0.0

    # If the object is less than 0.25m away, stop moving forward and rotate until the object is behind the robot
    elif (Obstacle.distance <= 0.25):
        if (Obstacle.angle > 90 and Obstacle.angle < 270):  # Checks if object is behind
            cmd_vel_msg.linear.x = 0.15
            cmd_vel_msg.angular.z = 0.0
        
        if (Obstacle.angle >= 0 and Obstacle.angle < 90):  # Check if the object is to the left of the robot
            cmd_vel_msg.linear.x = 0.0
            cmd_vel_msg.angular.z = -1

        if (Obstacle.angle > 270 and Obstacle.angle < 360):  # Check if the object is to the right of the robot
            cmd_vel_msg.linear.x = 0.0
            cmd_vel_msg.angular.z = 1
    
    cmd_vel_pub.publish(cmd_vel_msg)  # Publish the updated velocity commands
    

if __name__ == "__main__":
    try:
        rospy.init_node("roaming_controller")
        rospy.loginfo("roaming_controller node is activated")
        
        cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        obstacle_sub = rospy.Subscriber('obstacle_detector', Obstacle, callback=obstacle_avoidace)
        
        cmd_vel_msg = Twist()
        
        rospy.spin()
    except rospy.ROSInterruptException:
        pass