---
sidebar_position: 2
---

# Nodes, Topics, and Services

In ROS 2, the communication between different parts of your robot system happens through a distributed architecture. Understanding the core communication concepts is essential for controlling humanoid robots effectively.

## Nodes

A **node** is a process that performs computation. Nodes are the fundamental building blocks of a ROS 2 program. In the context of humanoid robotics, you might have nodes for:

- Joint controllers
- Sensor data processing
- Motion planning
- High-level decision making

### Creating a Node

Here's a basic example of a ROS 2 node in Python:

```python
import rclpy
from rclpy.node import Node

class HumanoidController(Node):
    def __init__(self):
        super().__init__('humanoid_controller')
        self.get_logger().info('Humanoid Controller node started')

def main(args=None):
    rclpy.init(args=args)
    controller = HumanoidController()

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

## Topics and Message Passing

**Topics** enable asynchronous message passing between nodes using a publish/subscribe pattern. This is ideal for continuous data streams like sensor readings or joint positions.

### Publisher Example

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class HumanoidTalker(Node):
    def __init__(self):
        super().__init__('humanoid_talker')
        self.publisher = self.create_publisher(String, 'robot_status', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Humanoid robot status: {self.i}'
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    talker = HumanoidTalker()

    try:
        rclpy.spin(talker)
    except KeyboardInterrupt:
        pass
    finally:
        talker.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Subscriber Example

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class HumanoidListener(Node):
    def __init__(self):
        super().__init__('humanoid_listener')
        self.subscription = self.create_subscription(
            String,
            'robot_status',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    listener = HumanoidListener()

    try:
        rclpy.spin(listener)
    except KeyboardInterrupt:
        pass
    finally:
        listener.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Services

**Services** provide synchronous request/response communication, which is useful for actions that require a response, such as requesting robot calibration or executing a specific movement.

### Service Server Example

```python
from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node

class MinimalService(Node):
    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'Incoming request\na: {request.a}, b: {request.b}')
        return response

def main(args=None):
    rclpy.init(args=args)
    minimal_service = MinimalService()

    try:
        rclpy.spin(minimal_service)
    except KeyboardInterrupt:
        pass
    finally:
        minimal_service.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Actions (Advanced Topic)

For long-running tasks with feedback, ROS 2 provides **actions**. This is particularly useful for humanoid robot movements that take time and need to report progress.

## Summary

- **Nodes** are the basic computational elements that perform specific functions
- **Topics** enable asynchronous communication through publish/subscribe patterns
- **Services** provide synchronous request/response communication
- **Actions** handle long-running tasks with progress feedback