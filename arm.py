import motor
import math

class Arm:

    def __init__(self, arm1, arm2, board_size, cam_fov, rel_x, rel_y, rel_z, dropper_offset): 
        self.arm1 = arm1
        self.arm2 = arm2
        self.board_size = board_size
        # next four lines are up for lots of change, have Roy ask me wtf is going on
        # Motor(range of motion, minimum duty, maximum duty, power port, hertz, flipped?)
        self.theta_motor = motor.Motor(180, 2, 12, 15, 50, 90)
        self.base_motor = motor.Motor(180, 2, 12, 11, 50, 90)
        self.elbow_motor = motor.Motor(180, 2, 12, 13, 50, 45)
        self.dropper_motor = motor.Motor(180, 2, 12, 16, 50, 0)
        self.cam_fov = cam_fov
        self.rel_x = rel_x
        self.rel_y = rel_y
        self.rel_z = rel_z
        self.dropper_offset = dropper_offset

    def reset(self):
        default_x = 9 * self.board_size / 18 + self.rel_x
        default_y = 9 * self.board_size / 18 + self.rel_y
        self.move_position_offset(default_x, default_y, self.calculate_min_height, 0)

    def calculate_min_height(self):
        angle = self.cam_fov / 2
        opposite = self.board_size / 2
        angle = math.radians(angle)
        tan = math.tan(angle)
        adjacent = opposite / tan
        return adjacent * 1.2

    def move_position_offset(self, x, y, z, offset):
        if (x == 0):
            theta_angle = 90
        else:
            tan_angle = math.degrees(math.atan(y/x))
            print(str(tan_angle) + "tan")
            if (tan_angle < 0):
                tan_angle = tan_angle + 180
            theta_angle = tan_angle
        
        base_distance = math.sqrt(math.pow(x, 2) + math.pow(y, 2)) - offset
        base_angle_p1 = math.degrees(math.atan(z/base_distance))
        total_distance = math.sqrt(math.pow(base_distance, 2) + math.pow(z, 2))
        base_angle_p2 = loc_angle(self.arm2, self.arm1, total_distance)
        base_angle = base_angle_p1 + base_angle_p2
        
        elbow_angle = loc_angle(total_distance, self.arm1, self.arm2)
        elbow_motor_angle = 360 - (90 + base_angle) - elbow_angle

        self.theta_motor.set_angle_with_stall(theta_angle + 3, self.base_motor)
        if (self.base_motor.angle < 60 and base_angle > 60):
            self.base_motor.set_angle_with_stall(60, self.elbow_motor)
        elif (self.base_motor.angle > 60 and base_angle < 60):
            self.base_motor.set_angle_with_stall(60, self.elbow_motor)
        else:
            self.base_motor.set_angle_with_stall(base_angle, self.elbow_motor)

        
        self.elbow_motor.set_angle_with_stall(elbow_motor_angle, self.base_motor)
        self.base_motor.set_angle_with_stall(base_angle, self.elbow_motor)
        
        print(str(base_distance))
        print(str(total_distance))
        print(str(theta_angle))
        print(str(base_angle))
        print(str(elbow_motor_angle))

    def set_motor_angles(self, theta_angle, base_angle, elbow_angle):

        self.theta_motor.set_angle_with_stall(theta_angle, self.base_motor)
        if (self.base_motor.angle < 60 and base_angle > 60):
            self.base_motor.set_angle_with_stall(60, self.elbow_motor)
        elif (self.base_motor.angle > 60 and base_angle < 60):
            self.base_motor.set_angle_with_stall(60, self.elbow_motor)
        else:
            self.base_motor.set_angle_with_stall(base_angle, self.elbow_motor)

        
        self.elbow_motor.set_angle_with_stall(elbow_angle, self.base_motor)
        self.base_motor.set_angle_with_stall(base_angle, self.elbow_motor)

    def drop_piece(self):
        self.base_motor.stall(4)
        self.dropper_motor.rotate_to_angle_increment_with_stall(180, self.base_motor)
        self.base_motor.stall(3)

    def close_dropper(self):
        self.dropper_motor.rotate_to_angle_increment_with_stall(0, self.base_motor)

    def move_to_board_coord(self, x, y):
        total_x = x * self.board_size / 18 + self.rel_x
        total_y = y * self.board_size / 18 + self.rel_y
        self.move_position_offset(total_x, total_y, self.rel_z, self.dropper_offset)

    def standard_cycle(self, x, y):
        self.move_to_board_coord(x, y)
        self.drop_piece()
        self.reset()
        self.close_dropper()

def loc_angle(c, a, b):
    numerator = math.pow(c, 2) - math.pow(a, 2) - math.pow(b, 2)
    denominator = -2*a*b
    frac = numerator / denominator
    result = math.acos(frac)
    return math.degrees(result)


        