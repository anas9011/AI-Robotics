---
sidebar_position: 4
---

# ROS 2 Architecture Diagrams

This section illustrates the core architecture of ROS 2 systems using diagrams to visualize how components interact in humanoid robot applications.

## Node Communication Architecture

The following diagram shows how nodes communicate in a ROS 2 system:

```mermaid
graph LR
    A[Humanoid Controller Node] -->|Commands| B((Joint Command Topic))
    C[Sensor Processing Node] -->|Sensor Data| B
    B --> D[Actuator Control Node]
    B --> E[State Estimation Node]

    F[Robot Action Server] --> G{Action Request}
    G --> H[Movement Planner]
    G --> I[Balance Controller]

    J[High-Level Planner] -.-> F
    D -.-> J
    E -.-> J
```

### Key Components:

- **Nodes**: Individual processes that perform computation (rectangles)
- **Topics**: Communication channels for asynchronous message passing (ovals)
- **Services/Actions**: Synchronous communication for specific requests (diamonds)
- **Communication Links**: Data flow between components (arrows)

## Humanoid Robot Control Architecture

This diagram shows a typical control architecture for a humanoid robot:

```mermaid
graph TB
    subgraph "High-Level Control"
        A[Behavior Planner]
        B[Path Planner]
    end

    subgraph "Mid-Level Control"
        C[Walk Controller]
        D[Balance Controller]
        E[Arm Controller]
    end

    subgraph "Low-Level Control"
        F[Joint Controllers]
        G[Sensor Processors]
    end

    subgraph "Hardware"
        H[Actuators]
        I[Sensors]
        J[Robot Platform]
    end

    A --> C
    A --> D
    A --> E
    B --> C
    C --> F
    D --> F
    E --> F
    G --> D
    G --> C
    F --> H
    G --> I
    H --> J
    I --> J
```

## Publisher-Subscriber Pattern

This diagram illustrates the publisher-subscriber communication pattern:

```mermaid
graph LR
    A[Sensor Publisher] -->|"Joint Angles<br/>sensor_msgs/JointState"| B((Topic<br/>/joint_states))
    C[State Estimator] -->|"Joint Angles"| B
    D[Controller] -->|"Joint Angles"| B
    B --> E[Logger]

    style A fill:#cde4ca
    style C fill:#e4cdda
    style D fill:#e4cdda
    style E fill:#f9d71c
```

### Legend:
- Green: Publishers (produce data)
- Purple: Subscribers (consume data)
- Yellow: Tools (special subscribers)

## Service Architecture

This diagram shows the service request-response pattern:

```mermaid
sequenceDiagram
    participant C as Controller Node
    participant S as Service Server
    C->>S: Request (Move to position X,Y)
    S->>S: Process request
    S->>C: Response (Success/Failure)
```

## Publisher-Subscriber Workflow

This sequence diagram shows the detailed workflow of the publisher-subscriber pattern:

```mermaid
sequenceDiagram
    participant P as Publisher Node
    participant RMW as RMW Layer
    participant S1 as Subscriber 1
    participant S2 as Subscriber 2

    P->>RMW: Publish message to /topic_name
    RMW->>S1: Deliver message
    RMW->>S2: Deliver message
    S1->>S1: Process message
    S2->>S2: Process message
```

## Service Request-Response Pattern

This sequence diagram shows the service request-response communication pattern:

```mermaid
sequenceDiagram
    participant C as Client Node
    participant S as Service Server
    participant RMW as RMW Layer

    C->>RMW: Service request
    RMW->>S: Forward request
    S->>S: Process request
    S->>RMW: Send response
    RMW->>C: Return response
    C->>C: Process response
```

## Summary

These diagrams illustrate the distributed nature of ROS 2 systems where:
- Nodes run independently and communicate through topics, services, and actions
- Multiple nodes can subscribe to the same topic (broadcasting)
- Topics enable loose coupling between nodes
- Services provide direct request-response communication
- The architecture supports both real-time control and high-level planning