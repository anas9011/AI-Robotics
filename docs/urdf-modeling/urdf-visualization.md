---
sidebar_position: 4
---

# URDF Structure and Visualization

This section illustrates the structure of URDF files and how they represent robot models in ROS 2.

## URDF XML Hierarchy

The following diagram shows the hierarchical structure of a URDF file:

```mermaid
graph TD
    A[Robot] --> B[Links]
    A --> C[Joints]
    A --> D[Materials]

    B --> B1[base_link]
    B --> B2[upper_arm]
    B --> B3[lower_arm]

    B1 --> B1a[Visual]
    B1 --> B1b[Collision]
    B1 --> B1c[Inertial]

    C --> C1[shoulder_joint]
    C --> C2[elbow_joint]

    C1 --> C1a[Parent: base_link]
    C1 --> C1b[Child: upper_arm]
    C1 --> C1c[Type: revolute]
    C1 --> C1d[Limit]

    C2 --> C2a[Parent: upper_arm]
    C2 --> C2b[Child: lower_arm]
    C2 --> C2c[Type: revolute]
    C2 --> C2d[Limit]
```

### Key Components:

- **Robot**: Root element that contains the entire robot description
- **Links**: Rigid bodies that make up the robot structure
- **Joints**: Connections between links that define how they can move relative to each other
- **Materials**: Visual properties like color and texture

## Robot Kinematic Structure

This diagram shows how links and joints form the kinematic chain of a robot:

```mermaid
graph LR
    A[torso] -->|left_hip_joint| B[left_upper_leg]
    B -->|left_knee_joint| C[left_lower_leg]
    C -->|left_ankle_joint| D[left_foot]

    A -->|right_hip_joint| E[right_upper_leg]
    E -->|right_knee_joint| F[right_lower_leg]
    F -->|right_ankle_joint| G[right_foot]

    A -->|left_shoulder_joint| H[left_upper_arm]
    H -->|left_elbow_joint| I[left_lower_arm]

    A -->|right_shoulder_joint| J[right_upper_arm]
    J -->|right_elbow_joint| K[right_lower_arm]
```

## URDF to Robot Model Pipeline

This flowchart shows how URDF files are processed in ROS 2:

```mermaid
flowchart LR
    A[URDF File] --> B[Robot State Publisher]
    B --> C[TF Tree]
    C --> D[RViz Visualization]
    C --> E[Physics Simulation]
    C --> F[Motion Planning]

    style A fill:#cde4ca
    style D fill:#dae4ca
    style E fill:#e4cdda
    style F fill:#f9d71c
```

## Common URDF Elements

### Link Structure
```
<link name="link_name">
  <visual>
    <geometry>
      <cylinder length="0.1" radius="0.05"/>
    </geometry>
    <material name="red"/>
  </visual>
  <collision>
    <geometry>
      <cylinder length="0.1" radius="0.05"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="1.0"/>
    <inertia ixx="0.1" ixy="0" ixz="0" iyy="0.1" iyz="0" izz="0.1"/>
  </inertial>
</link>
```

### Joint Structure
```
<joint name="joint_name" type="revolute">
  <parent link="parent_link"/>
  <child link="child_link"/>
  <origin xyz="0 0 0.1" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>
  <limit lower="-1.57" upper="1.57" effort="10" velocity="1"/>
</joint>
```

## URDF Validation Process

This diagram shows the process for validating URDF files:

```mermaid
flowchart TD
    A[Write URDF] --> B[Syntax Check]
    B --> C{Valid XML?}
    C -->|No| D[Fix Syntax Errors]
    C -->|Yes| E[Semantic Check]
    E --> F{Valid URDF?}
    F -->|No| G[Fix URDF Errors]
    F -->|Yes| H[Load in ROS 2]
    D --> B
    G --> E
    H --> I[Success]
```

## Summary

URDF files provide a standardized way to describe robot geometry and kinematics. The XML structure defines the robot as a collection of links connected by joints, which ROS 2 tools use for visualization, simulation, and planning.