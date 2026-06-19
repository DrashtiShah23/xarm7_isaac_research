from xarm.wrapper import XArmAPI

ROBOT_IP = "192.168.1.202"

def main():
    arm = XArmAPI(ROBOT_IP)

    print("Connected:", arm.connected)

    state_code, state = arm.get_state()
    print("State return code:", state_code)
    print("Robot state:", state)

    error_code, error_info = arm.get_err_warn_code()
    print("Error return code:", error_code)
    print("Error and warning info:", error_info)

    position_code, position = arm.get_position()
    print("Position return code:", position_code)
    print("TCP position:", position)

    angle_code, angles = arm.get_servo_angle()
    print("Joint angle return code:", angle_code)
    print("Joint angles:", angles)

    arm.disconnect()

if __name__ == "__main__":
    main()
