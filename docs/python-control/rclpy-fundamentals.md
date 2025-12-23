---
sidebar_position: 2
---

# rclpy Fundamentals: Python-ROS Integration

The `rclpy` package provides Python bindings for the ROS 2 client library. It allows you to write ROS 2 nodes in Python, which is often preferred for rapid prototyping and ease of use in robotics applications.

## Understanding rclpy

`rclpy` is the Python client library for ROS 2. It provides node creation, publisher/subscriber functionality, services, and parameter handling.

## Creating Your First rclpy Node

Here's the basic structure of an rclpy node:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World'
        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()

    try:
        rclpy.spin(minimal_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        minimal_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Publishers and Subscribers

### Publisher Example

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class HumanoidCommandPublisher(Node):
    def __init__(self):
        super().__init__('humanoid_command_publisher')
        self.publisher = self.create_publisher(String, 'humanoid_commands', 10)

    def send_command(self, command):
        msg = String()
        msg.data = command
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing: {command}')

def main(args=None):
    rclpy.init(args=args)
    publisher = HumanoidCommandPublisher()

    # Send a command
    publisher.send_command('walk_forward')

    # Keep the node alive briefly to allow message to be sent
    import time
    time.sleep(1)

    publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Best Practices for rclpy

1. **Always handle shutdown properly**: Use try/finally blocks to ensure nodes are properly destroyed
2. **Log important events**: Use `self.get_logger().info/warn/error` for debugging
3. **Parameterize your nodes**: Use parameters for configurable behavior

## Troubleshooting Common Issues

When working with rclpy and Python-ROS integration, you may encounter common issues. Here are solutions to typical problems:

### Import Errors
- **Problem**: `ModuleNotFoundError: No module named 'rclpy'`
- **Solution**: Make sure ROS 2 is sourced in your environment and Python paths are set correctly: `source /opt/ros/humble/setup.bash` (Linux) or `call C:\dev\ros_humble\setup.bat` (Windows)

### Node Initialization Problems
- **Problem**: `rclpy.init()` fails or node doesn't start
- **Solution**: Ensure `rclpy.init()` is called before creating any nodes, and check that ROS 2 environment is properly sourced

### Publisher/Subscriber Issues
- **Problem**: Messages not being sent or received
- **Solution**: Verify that QoS profiles match between publisher and subscriber, and that topic names are identical (including case)

### Memory Management
- **Problem**: Nodes not shutting down properly or memory leaks
- **Solution**: Always call `node.destroy_node()` and `rclpy.shutdown()` in a finally block to ensure proper cleanup

### Threading Issues
- **Problem**: Threading-related errors when using rclpy in multi-threaded applications
- **Solution**: Use `rclpy.spin_once()` or similar non-blocking alternatives instead of `rclpy.spin()` in multi-threaded contexts

## Summary

rclpy provides a clean, Pythonic interface to ROS 2 functionality, particularly useful for rapid prototyping and testing.