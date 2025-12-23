---
sidebar_position: 4
---

# rclpy Architecture: Python-ROS Integration

This section illustrates how Python integrates with ROS 2 through the rclpy library.

## rclpy Architecture Overview

The following diagram shows how rclpy fits into the ROS 2 architecture:

```mermaid
graph TB
    subgraph "Python Application"
        A[Python Node]
        B[rclpy Client Library]
    end

    subgraph "ROS 2 Middleware"
        C[rcl Common Client Library]
        D[RMW - ROS Middleware]
        E[DDS Implementation]
    end

    A -- "Python API" --> B
    B -- "C API" --> C
    C -- "Middleware Interface" --> D
    D -- "Transport" --> E
```

### Components Explained:

- **Python Node**: Your Python application code using rclpy
- **rclpy**: Python client library that provides ROS 2 functionality
- **rcl**: Common C client library shared across all ROS 2 client libraries
- **RMW**: ROS Middleware layer that abstracts the underlying transport
- **DDS**: Data Distribution Service that handles message transport

## Node Lifecycle with rclpy

This diagram shows the lifecycle of a Python node using rclpy:

```mermaid
stateDiagram-v2
    [*] --> Init: rclpy.init()
    Init --> CreateNode: Node()
    CreateNode --> Spin: rclpy.spin()
    Spin --> [*]: Node execution
    Spin --> Cleanup: KeyboardInterrupt
    Cleanup --> DestroyNode: node.destroy_node()
    DestroyNode --> Shutdown: rclpy.shutdown()
    Shutdown --> [*]: Complete
```

## Summary

The rclpy architecture enables clean separation between application logic and ROS 2 middleware with consistent API across different DDS implementations.