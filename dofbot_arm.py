from Arm_Lib import Arm_Device
import time

class DofBotArm:
    """
    class to control the dofbot arm
    
    Rook -> R
    Bishop -> B
    Knight -> KN
    Queen -> Q
    King -> K
            
    It should pick pieces in order of B -> KN -> R -> Q -> K when playing
    All winning moves should be done with the King(K)
    """
    
    SERVO_ANGLE_LIMITS = {
        1: (0, 180),  # base rotation
        2: (0, 180),  # shoulder up/down
        3: (0, 180),  # elbow up/down
        4: (0, 180),  # wrist up/down
        5: (0, 270),  # gripper rotation
        6: (0, 180),  # gripper open/close  
    }
    
    # specific gripper angles are needed to hold each piece
    GRIPPER_ANGLES = {
        'R': 176,   # Rook
        'B': 170,   # Bishop
        'KN': 170,  # Knight
        'Q': 170,   # Queen
        'K': 170,   # King
    }
    
    def __init__(self):
        # create the robotic arm object
        self.arm = Arm_Device()
        # define variables for servos
    
        # always reset position on init
        self.reset_position()


    def move_servo(self, servo_id, angle, time_ms):
        if servo_id < 0 or servo_id > 6:
            print('servo_id must be 0-6 | Given value is {servo_id}')
            return
        
        if time_ms < 2000:
            print('time must be >= 2000ms | Given value is {time_ms}')
            return
        
        min_angle, max_angle = self.SERVO_ANGLE_LIMITS.get(servo_id, (0, 180))
        if angle < min_angle or angle > max_angle:
            print(f'angle for servo {servo_id} must be {min_angle}-{max_angle} | Given value is {angle}')
            return
        
        self.arm.Arm_serial_servo_write(servo_id, angle, time_ms)
        time.sleep( (time_ms / 1000) + 0.2)  # wait for the movement to complete plus a small buffer
    
    
    def move_servo_all(self, angles: list, time_ms: int):
        if len(angles) != 6:
            print("angles list must have 6 elements")
            return
        
        if time_ms < 4000:
            print('time must be >= 4000ms | Given value is {time_ms}')
            return
        
        for servo_id in range(6):
            min_angle, max_angle = self.SERVO_ANGLE_LIMITS.get(servo_id + 1, (0, 180))
            if angles[servo_id] < min_angle or angles[servo_id] > max_angle:
                print(f'angle for servo {servo_id + 1} must be {min_angle}-{max_angle} | Given value is {angles[servo_id]}')
                return
        
        self.arm.Arm_serial_servo_write6(angles[0], angles[1], angles[2], angles[3], angles[4], angles[5], time_ms)
        time.sleep( (time_ms / 1000) + 0.2)  # wait for movement and add buffer
        
        
    def reset_position(self):
        """
        function to reset dofbot arm to initial position to see the board and all pieces
        default time is 6000ms to move it slowly
        """
        self.move_servo_all([90, 90, 90, 90, 90, 90], 5000)
        self.move_servo_all([90, 155, 0, -12, 90, 90], 4000)
    
        
    
    def pick_up_piece(self, piece: str, coordinates: tuple):
        """
        function to pick up piece from original position on the side
        """
        if coordinates is None or len(coordinates) != 4:
            print("bad coordinates")
            return
        # get the gripper angle for the piece
        angle = self.GRIPPER_ANGLES.get(piece, 170)
        # open gripper more than needed
        self.move_servo(6, angle + 20, 1000)
        # rotate gripper upside down to avoid hitting other pieces with black box below
        self.move_servo(5, 270, 3000)
        # move arm to position of piece
        
        
        # hold piece
        self.move_servo(6, angle, 1000)
        time.sleep(1)
