#!/usr/bin/env python3
import rospy
from loa_bot.msg import Obstacle
from sensor_msgs.msg import LaserScan

if __name__ == "__main__":
    try:
        rospy.init_node("obstacle_detector")
        rospy.loginfo("obstacle_detector node is activated")
        
        obstacle_posistion_pub = rospy.Publisher('obstacle_data', Obstacle, queue_size=1)
        obstacle_posistion_msg = Obstacle()

        #  Continuously recieve LiDar data and publish Obstacle data
        while not rospy.is_shutdown():
            scan = rospy.wait_for_message('scan', LaserScan)  # Wait for LiDAR to complete a 360 scan
            lidar_distances = list(scan.ranges)  # Convert the scan array to a list for index manipulation

            # Loop through the list and replace any zero errors with a large number
            for i in range(len(lidar_distances)):
                if (lidar_distances[i] < 0.01):
                    lidar_distances[i] = 9
        
            obstacle_posistion_msg.distance = min(lidar_distances)
            obstacle_posistion_msg.angle = lidar_distances.index(obstacle_posistion_msg.distance)

            obstacle_posistion_pub.publish(obstacle_posistion_msg)  # Publish obstacle data
    
    except rospy.ROSInterruptException:
        pass