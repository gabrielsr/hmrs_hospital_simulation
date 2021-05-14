from morse.builder import *
from turtlebot_hospital_sim.BatterySensor import BatterySensor


PATH = "/".join(__file__.split("/")[:-3])


class Turtlebot(Robot):
    def __init__(self, name="turtlebot", path=f"{PATH}/models/turtlebot.blend"):
        Robot.__init__(self, path, name)
        self.name = name
        self.path = path

    def add_to_simulation(self, x=-19, y=-3, z=0,
                          x_rot=0, y_rot=0, z_rot=0,
                          battery_discharge_rate=0.05):
        self.translate(x, y, z)
        self.rotate(x_rot, y_rot, z_rot)
        self.add_motion_sensor()
        self.add_pose_sensor()
        self.add_lidar_sensor()
        self.add_odometry_sensor()
        self.add_battery_sensor(battery_discharge_rate)

    def add_lidar_sensor(self):
        self.lidar = Hokuyo()
        self.lidar.frequency(10)
        self.append(self.lidar)
        self.lidar.properties(Visible_arc = False)
        self.lidar.properties(laser_range = 15.0)
        self.lidar.properties(resolution = 0.50)
        self.lidar.properties(scan_window = 180.0)
        self.lidar.create_laser_arc()
        self.lidar.add_interface('ros', topic=f"{self.name}/lidar", frame_id=f"base_laser_link")

    def add_motion_sensor(self):
        self.motion = MotionVW()
        self.motion.frequency(10)
        self.append(self.motion)
        self.motion.add_interface('ros', topic=f"{self.name}/cmd_vel")

    def add_pose_sensor(self):
        # Current position
        self.pose = Pose()
        self.pose.frequency(10)
        self.append(self.pose)
        self.pose.add_interface('ros', topic=f"{self.name}/pose", frame_id="map")

    def add_odometry_sensor(self):
        # Displacement since last Blender tick
        self.odometry = Odometry()
        self.odometry.frequency(10)
        self.append(self.odometry)
        self.odometry.add_interface('ros', topic=f"{self.name}/odom", frame_id=f"odom", child_frame_id=f"base_footprint")

    def add_battery_sensor(self, discharge_rate):
        self.battery = BatterySensor(self.name)
        # self.battery = Battery()
        # # self.battery = BatteryRobot(self)
        # self.battery.frequency(1)
        # self.battery.properties(DischargingRate = discharge_rate)
        # self.append(self.battery)
        # self.battery.add_interface('ros', topic=f"{self.name}/battery")
