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
            
    It should pick pieces in order of B -> KN -> R -> Q -> K
    All winning moves should be done with the King(K)
    """
    
    # specific gripper angles are needed to hold each piece
    GRIPPER_ANGLES = {
        'R': 176,   # Rook
        'B': 170,   # Bishop
        'KN': 170,  # Knight
        'Q': 170,   # Queen
        'K': 170,   # King
    }
    
    def __init__(self):
        self.arm = Arm_Device()
    
    def pick_up_piece(self, piece: str):
        """
        function to pick up piece from original position on the side
        """
        angle = self.GRIPPER_ANGLES.get(piece, 170)
        # move arm to position
        # TBC
        # move gripper
        self.arm.Arm_serial_servo_write(6, angle, 1000)
        time.sleep(1)
