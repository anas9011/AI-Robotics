---
sidebar_position: 3
---

# Practical Examples: ROS 2 Basics

This section provides hands-on exercises to practice the core ROS 2 concepts you've learned. These examples are specifically designed for humanoid robot applications.

## Example 1: Simple Publisher-Subscriber Pair

Let's create a simple publisher and subscriber that could represent a sensor (publisher) and controller (subscriber) in a humanoid robot system.

### Publisher Node

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random

class JointSensorPublisher(Node):
    def __init__(self):
        super().__init__('joint_sensor_publisher')
        self.publisher = self.create_publisher(Float32, 'joint_angle', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = Float32()
        # Simulate a joint angle reading with some variation
        msg.data = 45.0 + random.uniform(-5.0, 5.0)  # Base 45 degrees with noise
        self.publisher.publish(msg)
        self.get_logger().info(f'Joint angle: {msg.data:.2f} degrees')

def main(args=None):
    rclpy.init(args=args)
    joint_sensor_publisher = JointSensorPublisher()

    try:
        rclpy.spin(joint_sensor_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        joint_sensor_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Subscriber Node

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class JointControllerSubscriber(Node):
    def __init__(self):
        super().__init__('joint_controller_subscriber')
        self.subscription = self.create_subscription(
            Float32,
            'joint_angle',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        # Simple control logic: if joint angle is above 48 degrees,
        # we might want to adjust it back to desired position
        target_angle = 45.0
        current_angle = msg.data
        error = abs(current_angle - target_angle)

        if error > 2.0:  # If error is greater than 2 degrees
            self.get_logger().info(
                f'Joint adjustment needed: current={current_angle:.2f}, '
                f'target={target_angle}, error={error:.2f}'
            )
        else:
            self.get_logger().info(f'Joint position OK: {current_angle:.2f} degrees')

def main(args=None):
    rclpy.init(args=args)
    joint_controller_subscriber = JointControllerSubscriber()

    try:
        rclpy.spin(joint_controller_subscriber)
    except KeyboardInterrupt:
        pass
    finally:
        joint_controller_subscriber.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Example 2: Service for Robot Commands

Let's create a service that allows other nodes to request specific actions from our humanoid robot.

### Service Server

```python
from example_interfaces.srv import Trigger
import rclpy
from rclpy.node import Node

class RobotActionServer(Node):
    def __init__(self):
        super().__init__('robot_action_server')
        self.srv = self.create_service(
            Trigger,
            'execute_robot_action',
            self.execute_robot_action_callback
        )

    def execute_robot_action_callback(self, request, response):
        self.get_logger().info('Executing robot action')
        response.success = True
        response.message = 'Robot action completed successfully'
        return response

def main(args=None):
    rclpy.init(args=args)
    robot_action_server = RobotActionServer()

    try:
        rclpy.spin(robot_action_server)
    except KeyboardInterrupt:
        pass
    finally:
        robot_action_server.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Exercises

1. **Modify the joint controller**: Change the error threshold in the subscriber example to 1.0 degree instead of 2.0 degrees.

2. **Extend the service**: Add a new action type that takes parameters for more complex robot movements.

## Troubleshooting Common Issues

When working with ROS 2 basics, you may encounter common issues. Here are solutions to typical problems:

### Node Connection Issues
- **Problem**: Nodes cannot communicate with each other
- **Solution**: Check that all nodes are on the same ROS domain ID. Use `echo $ROS_DOMAIN_ID` to verify, or set with `export ROS_DOMAIN_ID=0`

### Topic Communication Problems
- **Problem**: Publishers and subscribers not connecting
- **Solution**: Verify topic names match exactly (including case). Use `ros2 topic list` to see available topics and `ros2 topic echo <topic_name>` to verify data flow

### Service Call Failures
- **Problem**: Service clients get timeouts or errors
- **Solution**: Ensure the service server is running before making client calls. Use `ros2 service list` to verify the service exists

### Python Import Errors
- **Problem**: `ModuleNotFoundError` when importing rclpy or ROS 2 packages
- **Solution**: Make sure ROS 2 is sourced in your environment: `source /opt/ros/humble/setup.bash` (Linux) or `call C:\dev\ros_humble\setup.bat` (Windows)

### Permission Issues
- **Problem**: Cannot create nodes or access ROS 2 resources
- **Solution**: Check that your user is in the correct groups and that there are no permission restrictions on the ROS 2 installation

## Summary

These practical examples demonstrate how to create publisher-subscriber pairs and services for humanoid robot applications.