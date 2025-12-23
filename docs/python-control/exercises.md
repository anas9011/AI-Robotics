---
sidebar_position: 5
---

# Exercises: Python Control Implementation

This section provides exercises to reinforce your understanding of Python-based ROS 2 control for humanoid robots.

## Exercise 1: Simple Publisher-Subscriber System

Create a publisher that publishes joint angle commands and a subscriber that receives and logs these commands.

**Requirements:**
- Create a publisher node that sends joint angle commands every 0.5 seconds
- Create a subscriber node that receives and logs the commands
- Use the `std_msgs/Float64MultiArray` message type for joint angles

## Exercise 2: PID Controller Implementation

Implement a PID controller for a single joint that maintains a desired position.

**Requirements:**
- Implement the PID control algorithm
- Subscribe to current joint position
- Publish control commands to reach desired position
- Add safety limits to prevent excessive commands

## Exercise 3: Parameter-Based Controller

Create a controller that adjusts its behavior based on ROS 2 parameters.

**Requirements:**
- Use parameters to configure control gains
- Allow runtime adjustment of control parameters
- Implement parameter validation to ensure safe values

## Exercise 4: Service-Based Control

Implement a service that accepts movement requests and executes them.

**Requirements:**
- Create a service that accepts movement parameters
- Implement the service callback to execute the movement
- Return success/failure status

## Project: Simple Walking Controller

Combine all concepts to create a simple walking controller:

1. Use multiple joints to create a walking gait
2. Implement PID control for each joint
3. Add parameters to adjust walking speed and step height
4. Implement safety checks to prevent falls