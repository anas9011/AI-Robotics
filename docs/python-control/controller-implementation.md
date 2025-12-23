---
sidebar_position: 3
---

# Controller Implementation with rclpy

This section covers how to implement controllers for humanoid robots using Python and rclpy. Controllers are essential for managing the robot's behavior and responding to sensor inputs.

## Basic Joint Controller

Here's a simple joint position controller implementation:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState

class JointController(Node):
    def __init__(self):
        super().__init__('joint_controller')

        # Publisher for joint commands
        self.joint_cmd_publisher = self.create_publisher(
            Float64MultiArray,
            '/joint_commands',
            10
        )

        # Timer for control loop
        self.control_timer = self.create_timer(0.02, self.control_loop)  # 50 Hz

        # Desired joint positions
        self.desired_positions = [0.0, 0.5, -0.5]  # Example for 3 joints
        self.get_logger().info('Joint Controller initialized')

    def control_loop(self):
        """Main control loop that sends commands"""
        commands = Float64MultiArray()
        commands.data = self.desired_positions
        self.joint_cmd_publisher.publish(commands)

def main(args=None):
    rclpy.init(args=args)
    controller = JointController()

    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        pass
    finally:
        controller.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## PID Controller Implementation

A more sophisticated controller using PID control:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

class SimplePIDController:
    def __init__(self, kp=1.0, ki=0.0, kd=0.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.previous_error = 0
        self.integral = 0

    def compute(self, setpoint, measured_value):
        error = setpoint - measured_value
        self.integral += error
        derivative = error - self.previous_error

        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.previous_error = error
        return output

class HumanoidPIDController(Node):
    def __init__(self):
        super().__init__('humanoid_pid_controller')

        # Create PID controller
        self.pid = SimplePIDController(kp=2.0, ki=0.1, kd=0.05)

        # Publisher for commands
        self.command_publisher = self.create_publisher(Float64, '/joint_command', 10)

        # Timer for control loop
        self.control_timer = self.create_timer(0.01, self.control_loop)  # 100 Hz

        self.current_position = 0.0
        self.desired_position = 1.57  # 90 degrees
        self.get_logger().info('PID Controller initialized')

    def control_loop(self):
        """Compute control output and publish command"""
        output = self.pid.compute(self.desired_position, self.current_position)

        cmd_msg = Float64()
        cmd_msg.data = output
        self.command_publisher.publish(cmd_msg)

def main(args=None):
    rclpy.init(args=args)
    controller = HumanoidPIDController()

    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        pass
    finally:
        controller.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Best Practices for Controller Implementation

1. **Safety First**: Always implement safety checks and limits
2. **Proper Tuning**: Tune PID parameters for your specific robot
3. **Error Handling**: Implement proper error handling and recovery

## Summary

Controller implementation in ROS 2 with Python provides flexible development of control algorithms and clear separation of control logic from hardware interfaces.