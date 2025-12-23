---
sidebar_position: 2
---

# URDF Structure Basics

URDF (Unified Robot Description Format) is an XML-based format used to describe robots in ROS. It defines the robot's physical structure, including links, joints, and their relationships.

## Understanding URDF

URDF describes a robot as a collection of links connected by joints:
- **Links**: Rigid parts of the robot (e.g., torso, upper arm, lower arm)
- **Joints**: Connections between links that allow relative motion
- **Materials**: Visual properties like color
- **Inertial properties**: Mass, center of mass, and inertia for physics simulation

## Basic URDF Structure

Here's the basic structure of a URDF file:

```xml
<?xml version="1.0"?>
<robot name="simple_robot">
  <!-- Links -->
  <link name="base_link">
    <visual>
      <geometry>
        <cylinder length="0.6" radius="0.2"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 0.8 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.6" radius="0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10"/>
      <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
    </inertial>
  </link>

  <!-- Joints -->
  <joint name="base_to_upper_leg" type="revolute">
    <parent link="base_link"/>
    <child link="upper_leg"/>
    <origin xyz="0 0 0.3" rpy="0 0 0"/>
    <axis xyz="1 0 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>
</robot>
```

## Links

Links represent rigid bodies in the robot. Each link contains:

- **Visual**: How the link looks in visualization
- **Collision**: How the link interacts in collision detection
- **Inertial**: Physical properties for simulation

### Link Example

```xml
<link name="upper_arm">
  <visual>
    <geometry>
      <cylinder length="0.4" radius="0.05"/>
    </geometry>
    <material name="gray">
      <color rgba="0.5 0.5 0.5 1"/>
    </material>
  </visual>
  <collision>
    <geometry>
      <cylinder length="0.4" radius="0.05"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="2"/>
    <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.001"/>
  </inertial>
</link>
```

## Joints

Joints connect links and define how they can move relative to each other. Common joint types:

- **revolute**: Rotational joint with limited range (like an elbow)
- **continuous**: Rotational joint without limits (like a wheel)
- **prismatic**: Linear sliding joint
- **fixed**: No movement (welds two links together)

### Joint Example

```xml
<joint name="shoulder_joint" type="revolute">
  <parent link="torso"/>
  <child link="upper_arm"/>
  <origin xyz="0 0 0.5" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  <dynamics damping="0.1" friction="0.0"/>
</joint>
```

## Materials

Materials define visual properties:

```xml
<material name="red">
  <color rgba="0.8 0.2 0.2 1"/>
</material>
```

## Common URDF Elements

- **origin**: Position and orientation offset (xyz position, rpy rotation)
- **geometry**: Shape definition (box, cylinder, sphere, mesh)
- **axis**: Joint rotation axis
- **limit**: Joint constraints (for revolute/prismatic joints)

## URDF for Humanoid Robots

Humanoid robots typically have a tree-like structure:
- Base (torso/pelvis)
- Two legs (each with hip, knee, ankle joints)
- Two arms (each with shoulder, elbow, wrist joints)
- Head (on neck joint)

## Validation

URDF files should be validated to ensure they're properly formed:

```bash
# Check URDF syntax
check_urdf your_robot.urdf

# Or use xacro if your file uses xacro macros
ros2 run xacro xacro your_robot.urdf.xacro
```

## Troubleshooting Common Issues

When working with URDF files for humanoid robots, you may encounter common issues. Here are solutions to typical problems:

### XML Syntax Errors
- **Problem**: Invalid XML syntax causing parsing failures
- **Solution**: Use a proper XML editor or validator to check for unclosed tags, incorrect attribute values, or invalid characters

### Missing Inertial Properties
- **Problem**: Physics simulation errors or unstable behavior
- **Solution**: Ensure all links have proper `<inertial>` tags with mass and inertia values, even if they're just placeholders

### Joint Limit Issues
- **Problem**: Robot self-collisions or unrealistic movements
- **Solution**: Carefully set joint limits based on physical constraints of the real robot, and validate with forward kinematics

### TF Tree Problems
- **Problem**: Robot state publisher errors or missing transforms
- **Solution**: Verify that all links are connected in a proper tree structure with no disconnected components or loops

### Visual/Collision Mismatch
- **Problem**: Robot appears differently in simulation vs. visualization
- **Solution**: Ensure visual and collision geometries are properly aligned and scaled

## Summary

URDF provides a standardized way to describe robot geometry and kinematics. For humanoid robots, it's essential to correctly define the kinematic chain from the base to each end effector (hands and feet).