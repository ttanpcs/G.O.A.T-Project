import motor
import math

class Arm:

    def __init__(self, arm1, arm2, board_size, cam_fov, rel_x, rel_y): 
        self.arm1 = arm1
        self.arm2 = arm2
        self.board_size = board_size
        # next four lines are up for lots of change, have Roy ask me wtf is going on
        # Motor(range of motion, minimum duty, maximum duty, power port, hertz)
        self.theta_motor = Motor(180, 2, 12, 0, 50)
        self.base_motor = Motor(180, 2, 12, 11, 50)
        self.elbow_motor = Motor(180, 2, 12, 13, 50)
        self.dropper_motor = Motor(180, 2, 12, 15, 50)
        self.cam_fov = cam_fov
        self.rel_x = rel_x
        self.rel_y = rel_y

    def rotate_theta(self, angle):
        self.theta_motor.set_angle(angle)

    def reset(self):
        pass

    def calculate_min_height(self):
        angle = self.cam_fov / 2
        opposite = self.board_size / 2
        angle = math.radians(angle)
        tan = math.tan(angle)
        adjacent = opposite / tan
        return adjacent * 1.2

    def move_position(self, x, y, z):
        theta_angle = 180 - math.degrees(math.atan(y/x))
        self.theta_motor.set_angle(theta_angle)

        base_distance = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
        base_angle_p1 = math.atan(z/base_distance)
        total_distance = math.sqrt(math.pow(base_distance, 2) + math.pow(z, 2))
        base_angle_p2 = loc_angle(self.arm2, self.arm1, total_distance)
        base_angle = base_angle_p1 + base_angle_p2
        self.base_motor.set_angle(base_angle)

        elbow_angle = loc_angle(total_distance, self.arm1, self.arm2)
        self.elbow_motor.set_angle(elbow_angle)

    def drop_piece(self):
        self.dropper_motor.set_angle(180)
        self.dropper_motor.stall(0.5)
        self.dropper_motor.set_angle(0)


def loc_angle(c, a, b):
    numerator = math.pow(c, 2) - math.pow(a, 2) - math.pow(b, 2)
    denominator = -2*a*b
    frac = numerator / denominator
    result = math.acos(frac)
    return math.degrees(result)


        