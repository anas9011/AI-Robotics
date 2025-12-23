---
sidebar_position: 5
---

# Parameter Management in ROS 2

Parameters in ROS 2 allow you to configure nodes at runtime without recompiling. This is particularly useful for humanoid robots where you might need to adjust control parameters based on the robot's configuration or environment.

## Basic Parameter Example

Here's a simple example of a node that uses parameters:

```python
import rclpy
from rclpy.node import Node

class HumanoidControllerWithParams(Node):
    def __init__(self):
        super().__init__('humanoid_controller_with_params')

        # Declare parameters with default values
        self.declare_parameter('max_joint_speed', 1.0)  # radians/second
        self.declare_parameter('control_loop_rate', 50)  # Hz
        self.declare_parameter('enable_safety_limits', True)

        # Get parameter values
        self.max_speed = self.get_parameter('max_joint_speed').value
        self.control_rate = self.get_parameter('control_loop_rate').value
        self.safety_enabled = self.get_parameter('enable_safety_limits').value

        self.get_logger().info(f'Max speed: {self.max_speed} rad/s')
        self.get_logger().info(f'Control rate: {self.control_rate} Hz')

def main(args=None):
    rclpy.init(args=args)
    controller = HumanoidControllerWithParams()

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

## Working with Parameters from Command Line

You can work with parameters from the command line:

```bash
# List all parameters of a node
ros2 param list

# Get a specific parameter
ros2 param get /humanoid_controller_with_params max_joint_speed

# Set a parameter
ros2 param set /humanoid_controller_with_params max_joint_speed 2.0
```

## Summary

Parameter management in ROS 2 provides a flexible way to configure nodes at runtime. For humanoid robots, this allows you to adjust control parameters without restarting nodes and configure robot-specific settings.