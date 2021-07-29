import json
import rospy
import geometry_msgs.msg
from morse.builder import *
from threading import Timer
from std_msgs.msg import String
from turtlebot_hospital_sim.BatterySensor import BatterySensor
from turtlebot_hospital_sim.ItemExchanger import ItemExchanger
# import tf_conversions
import numpy as np

PATH = "/".join(__file__.split("/")[:-3])

def formatlog(severity, who, loginfo, skill, params):
    return ('['+severity+'],'+
               who+','+
               loginfo+','+
               skill+','+
               params)

def euler_from_quaternion(quaternion):
    """
    Converts quaternion (w in last place) to euler roll, pitch, yaw
    quaternion = [x, y, z, w]
    Bellow should be replaced when porting for ROS 2 Python tf_conversions is done.
    """
    x = quaternion.x
    y = quaternion.y
    z = quaternion.z
    w = quaternion.w

    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    roll = np.arctan2(sinr_cosp, cosr_cosp)

    sinp = 2 * (w * y - z * x)
    pitch = np.arcsin(sinp)

    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)
    yaw = np.arctan2(siny_cosp, cosy_cosp)

    return roll, pitch, yaw

class Turtlebot(Pioneer3DX):
    def __init__(self, name="turtlebot", path=f"{PATH}/models/turtlebot.blend"):
        Pioneer3DX.__init__(self, name)
        self.name = name
        self.path = path
        self.item_exchanger = ItemExchanger(name=name, obj="sphere")
        self.curr_pose = geometry_msgs.msg.PoseStamped()
        self.pose_sub = rospy.Subscriber(f"/{self.name}/pose", geometry_msgs.msg.PoseStamped, self.save_pose)
        self.log_pub = rospy.Publisher(f"/log", String, queue_size=1)

        self.thr_timer = Timer(30, self.set_ros_timer)
        self.thr_timer.start()

    def set_ros_timer(self):
        while rospy.get_time() == 0:
            rospy.logwarn(f"{self.name} waiting for clock...")
        rospy.logwarn(f"{self.name} setting up battery module...")
        self.timer = rospy.Timer(rospy.Duration(15), self.log_robot_pose)

    def log_robot_pose(self, event):
        quaternion = (
            self.curr_pose.pose.orientation.x,
            self.curr_pose.pose.orientation.y,
            self.curr_pose.pose.orientation.z,
            self.curr_pose.pose.orientation.w)
        _, _, yaw = euler_from_quaternion(self.curr_pose.pose.orientation)
        # roll = euler[0]
        # pitch = euler[1]
        # yaw = euler[2]
        # robot_pose = "(x=%.2f;y=%.2f;yaw=%.2f)"%(self.curr_pose.pose.position.x,
        #                                        self.curr_pose.pose.position.y,
        #                                        yaw)
        robot_pose = {
            'x': '{:02.2f}'.format(self.curr_pose.pose.position.x),
            'y': '{:02.2f}'.format(self.curr_pose.pose.position.y),
            'yaw': '{:02.2f}'.format(yaw)
        }
        log = String()
        # log.data = formatlog('debug',
        #     self.name,
        #     'simulation',
        #     'robot-pose',
        #     robot_pose)
        logdata = {
                'level': 'info',
                'entity': self.name,
                'content': robot_pose
            }
        log.data = json.dumps(logdata)
        self.log_pub.publish(log)

    def add_to_simulation(self, x=-19, y=-3, z=0,
                          x_rot=0, y_rot=0, z_rot=0,
                          battery_discharge_rate=0.05,
                          batt_init_state=1.0):
        self.translate(x, y, z)
        self.rotate(x_rot, y_rot, z_rot)
        self.add_motion_sensor()
        self.add_pose_sensor()
        self.add_lidar_sensor()
        self.add_odometry_sensor()
        self.add_battery_sensor(battery_discharge_rate, batt_init_state)
        self.properties(Influence = 0.1, Friction = 5,
                        WheelFLName = "Wheel_L", WheelFRName = "Wheel_R",
                        WheelRLName = "None", WheelRRName = "None",
                        CasterWheelName = "CasterWheel", 
                        FixTurningSpeed = 0.52)

    def save_pose(self, msg):
        self.curr_pose = msg

    def add_lidar_sensor(self):
        self.lidar = Hokuyo()
        self.lidar.frequency(10)
        self.lidar.translate(x=0.0, z=0.252)
        self.append(self.lidar)
        self.lidar.properties(Visible_arc = False)
        self.lidar.properties(laser_range = 10.0)
        self.lidar.properties(resolution = 1)
        self.lidar.properties(scan_window = 360.0)
        self.lidar.create_laser_arc()
        self.lidar.add_interface('ros', topic=f"{self.name}/lidar", frame_id=f"{self.name}/base_footprint")

    def add_motion_sensor(self):
        # self.motion = MotionVW()
        self.motion = MotionVWDiff()
        # self.motion.frequency(10)
        self.append(self.motion)
        self.motion.add_interface('ros', topic=f"{self.name}/cmd_vel")

    def add_pose_sensor(self):
        # Current position
        self.pose = Pose()
        # self.pose.frequency(20)
        self.append(self.pose)
        self.pose.add_interface('ros', topic=f"{self.name}/pose", frame_id="map")

    def add_odometry_sensor(self):
        # Displacement since last Blender tick
        self.odometry = Odometry()
        # self.odometry.frequency(20)
        self.append(self.odometry)
        self.odometry.add_interface('ros', topic=f"{self.name}/odom", frame_id=f"{self.name}/odom", child_frame_id=f"{self.name}/base_footprint")

    def add_battery_sensor(self, discharge_rate, init_state):
        self.battery = BatterySensor(self.name, 
            discharge_rate_percentage=discharge_rate,
            initial_percentage=init_state)
        # self.battery = Battery()
        # self.battery = BatteryRobot(self)
        # self.battery.frequency(10)
        # self.battery.properties(DischargingRate = discharge_rate)
        # self.append(self.battery)
        # self.battery.add_interface('ros', topic=f"{self.name}/battery")
