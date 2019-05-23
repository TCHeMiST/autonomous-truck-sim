#include "ros/ros.h"

#include <sensor_msgs/PointCloud.h>
#include <sensor_msgs/PointCloud2.h>
#include <sensor_msgs/point_cloud_conversion.h>

ros::Subscriber sub_lidar_scan;
ros::Publisher pub_lidar_scan;

void lidarCallback(const sensor_msgs::PointCloud &scan)
{
    sensor_msgs::PointCloud2 point_cloud2;
    sensor_msgs::convertPointCloudToPointCloud2(scan, point_cloud2);

    pub_lidar_scan.publish(point_cloud2);
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "read_pc", ros::init_options::AnonymousName);
    ros::NodeHandle n;

    sensor_msgs::PointCloud point_cloud;

    sub_lidar_scan = n.subscribe("/autonomous_truck/Velodyne_VLP_16/point_cloud", 10, lidarCallback);
    pub_lidar_scan = n.advertise<sensor_msgs::PointCloud2>("/autonomous_truck/Velodyne_VLP_16/point_cloud2", 1);

    ros::spin();
}