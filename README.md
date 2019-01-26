# Autonomous truck simulation

<p align="center">
  Autonomous truck simulation on Webots fully controlled by ROS
  <br/>
</p>

## Install Webots 

First, install the latest Webots version [here](https://cyberbotics.com/#download)

### Download NUParking world

Copy ```parking_new.wbt``` file anywhere and open it through File-Open World.

Try runnning simulation. If everything is ok, proceed to next step.

## Install ROS

Use following commands:
```
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116
sudo apt-get update
sudo apt-get install ros-melodic-desktop-full
sudo apt-get install ros-melodic-sensor-msgs
sudo rosdep init
rosdep update
```

### Create catkin workspace

```
source /opt/ros/<distro>/setup.bash
mkdir -p catkin_ws/src
cd catkin_ws/src
catkin_init_workspace
```

Once your workspace is set, you have to copy the ```webots_ros``` folder located in "projects/languages/ros" in the ```src``` folder of your catkin workspace. You will also need to copy the list of services and messages definitions of the ```webots_ros``` package. Simply copy the ```srv``` and ```msg``` folders located in "projects/default/controllers/ros/include" into the ```src/webots_ros folder``` of your catkin workspace. 

Run

```
cd catkin_ws
catkin_make
```

### Editing package

To ```catkin_ws/src/webots_ros/src``` folder add ```autonomous_truck.cpp``` file from this repository.

Then open ```catkin_ws/src/webots_ros/CMakeLists.txt``` file and append following code:

```
#instructions for autonomous_truck node

add_executable(autonomous_truck src/autonomous_truck.cpp)

add_dependencies(autonomous_truck webots_ros_generate_messages_cpp)

target_link_libraries(autonomous_truck
    ${catkin_LIBRARIES}
)
```

Run 
```
catkin_make
```
in ```catkin_ws``` folder again

## Final check

Now, after everything is set up, open NUParking world again, then run:

```
source devel/setup.bash
roscore
```

Run simulation, and check console in Webots. Following lines should be printed:
```
[ros] [ INFO] [1548498557.090277465]: Robot's unique name is autonomous_truck.
[ros] [ INFO] [1548498557.094787086]: The controller is now connected to the ROS master.
```

After that run following command:

```
rosrun webots_ros autonomous_truck
```

which should print following lines:
```
[ INFO] [1548401753.473330674]: Controller #1: autonomous_truck.
[ INFO] [1548401753.478264625]: Position set to INFINITY for motor left_front_wheel.
[ INFO] [1548401753.489046002]: Velocity set to 0.0 for motor left_front_wheel.
[ INFO] [1548401753.509613928]: Position set to INFINITY for motor right_front_wheel.
[ INFO] [1548401753.581517864]: Velocity set to 0.0 for motor right_front_wheel.
[ INFO] [1548401753.623677354]: Position set to INFINITY for motor left_rear_wheel.
[ INFO] [1548401753.670758794]: Velocity set to 0.0 for motor left_rear_wheel.
[ INFO] [1548401753.685806912]: Position set to INFINITY for motor right_rear_wheel.
[ INFO] [1548401753.700127472]: Velocity set to 0.0 for motor right_rear_wheel.
[ INFO] [1548401753.766025461]: Lidar enabled.
[ INFO] [1548401753.800863296]: Topic for lidar initialized.
[ INFO] [1548401753.976200228]: Topic for lidar scan connected.
[ INFO] [1548401754.177210231]: GPS enabled.
[ INFO] [1548401754.378461715]: Inertial unit enabled.
[ INFO] [1548401754.463950387]: You can now start the creation of the map using 'rosrun gmapping slam_gmapping scan:=/autonomous_truck/Sick_LMS_291/laser_scan/layer0 _xmax:=30 _xmin:=-30 _ymax:=30 _ymin:=-30 _delta:=0.2'.
[ INFO] [1548401754.463989991]: You can now visualize the sensors output in rqt using 'rqt'.
```

If everything is as above everything is done!!

Now you can control your truck through ROS Services and receive information from sensors using ROS Topics.

Try running following command to make your truck ride:
```
rosservice call /autonomous_truck/right_front_wheel/set_velocity 1
rosservice call /autonomous_truck/left_front_wheel/set_velocity 1
```
 This is it!