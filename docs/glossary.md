---
sidebar_position: 100
---

# Glossary of ROS 2 Terms and Concepts

This glossary provides definitions for key terms and concepts used throughout the ROS 2 Humanoid Robotics Book.

## A

**Action** - A communication pattern in ROS 2 that allows for long-running tasks with feedback, goals, and results. Actions are built on top of services and provide more sophisticated communication for tasks that may take time to complete.

## C

**Client** - A node that sends requests to a service and receives responses. In the publisher-subscriber model, clients are part of the service-client communication pattern.

**Command and Query Responsibility Segregation (CQRS)** - A pattern used in ROS 2 where commands (requests for action) are separated from queries (requests for information), similar to the distinction between topics and services.

## D

**DDS (Data Distribution Service)** - The middleware that ROS 2 uses for communication between nodes. DDS provides the underlying infrastructure for ROS 2's publish-subscribe and client-service communication patterns.

## J

**Joint** - In URDF, a connection between two links that allows relative motion. Common joint types include revolute (rotational), prismatic (linear), and fixed (no motion).

## L

**Launch File** - An XML or Python file that defines how to start multiple ROS 2 nodes with specific parameters and configurations simultaneously.

**Link** - In URDF, a rigid body that represents a part of the robot structure. Links contain visual, collision, and inertial properties.

## M

**Middleware** - Software that provides common services and capabilities to applications beyond what's offered by the operating system. In ROS 2, the middleware is based on DDS.

## N

**Node** - A process that performs computation in ROS 2. Nodes are the fundamental building blocks of a ROS 2 application and communicate with other nodes through topics, services, and actions.

## P

**Parameter** - A configuration value that can be set for a node at runtime. Parameters allow for flexible configuration without recompiling code.

**Publisher** - A node that sends messages to a topic. Multiple publishers can send messages to the same topic.

## R

**rclpy** - The Python client library for ROS 2. It provides the Python API for creating nodes, publishers, subscribers, and other ROS 2 entities.

**ROS 2 (Robot Operating System 2)** - The next generation of the Robot Operating System, designed for production environments with improved security, real-time capabilities, and multi-robot systems.

**ROS Domain** - A namespace that allows multiple ROS 2 systems to operate on the same network without interfering with each other.

## S

**Service** - A communication pattern in ROS 2 that allows nodes to send requests and receive responses. Services provide synchronous request-response communication.

**Subscriber** - A node that receives messages from a topic. Multiple subscribers can receive messages from the same topic.

## T

**Topic** - A named bus over which nodes exchange messages. Topics enable the publish-subscribe communication pattern in ROS 2.

**TF (Transform)** - A package that keeps track of coordinate frames in a tree structure over time, allowing for coordinate transformations between different reference frames.

## U

**URDF (Unified Robot Description Format)** - An XML format used to describe robots, including their physical structure, joints, and kinematic properties.

## X

**Xacro** - An XML macro language that extends URDF, allowing for parameterization, reusability, and modularity in robot descriptions.