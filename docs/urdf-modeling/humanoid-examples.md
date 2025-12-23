---
sidebar_position: 3
---

# Humanoid Robot Examples

This section provides practical examples of URDF files specifically designed for humanoid robots, showing how to model the complex kinematic structure of human-like robots.

## Simple Humanoid Robot URDF

Here's a basic humanoid robot with torso, two arms, two legs, and a head. This example shows the essential structure with links, joints, and basic physical properties:

```xml
<?xml version="1.0"?>
<robot name="simple_humanoid">
  <!-- Materials -->
  <material name="black">
    <color rgba="0.0 0.0 0.0 1.0"/>
  </material>
  <material name="grey">
    <color rgba="0.5 0.5 0.5 1.0"/>
  </material>

  <!-- Torso -->
  <link name="torso">
    <visual>
      <geometry>
        <box size="0.3 0.2 0.5"/>
      </geometry>
      <material name="grey"/>
    </visual>
    <collision>
      <geometry>
        <box size="0.3 0.2 0.5"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10.0"/>
      <inertia ixx="0.5" ixy="0.0" ixz="0.0" iyy="0.5" iyz="0.0" izz="0.5"/>
    </inertial>
  </link>

  <!-- Head -->
  <link name="head">
    <visual>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
      <material name="grey"/>
    </visual>
    <collision>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01"/>
    </inertial>
  </link>

  <joint name="neck_joint" type="revolute">
    <parent link="torso"/>
    <child link="head"/>
    <origin xyz="0 0 0.35" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-0.5" upper="0.5" effort="10" velocity="1"/>
  </joint>

  <!-- Left Arm -->
  <link name="left_upper_arm">
    <visual>
      <geometry>
        <cylinder length="0.3" radius="0.05"/>
      </geometry>
      <material name="grey"/>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.3" radius="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <joint name="left_shoulder_joint" type="revolute">
    <parent link="torso"/>
    <child link="left_upper_arm"/>
    <origin xyz="0.2 0.15 0.1" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="10" velocity="1"/>
  </joint>

  <link name="left_lower_arm">
    <visual>
      <geometry>
        <cylinder length="0.3" radius="0.04"/>
      </geometry>
      <material name="grey"/>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.3" radius="0.04"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.8"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <joint name="left_elbow_joint" type="revolute">
    <parent link="left_upper_arm"/>
    <child link="left_lower_arm"/>
    <origin xyz="0 0 -0.3" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="0" effort="10" velocity="1"/>
  </joint>

  <!-- Right Arm (similar to left) -->
  <link name="right_upper_arm">
    <visual>
      <geometry>
        <cylinder length="0.3" radius="0.05"/>
      </geometry>
      <material name="grey"/>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.3" radius="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <joint name="right_shoulder_joint" type="revolute">
    <parent link="torso"/>
    <child link="right_upper_arm"/>
    <origin xyz="0.2 -0.15 0.1" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="10" velocity="1"/>
  </joint>

  <link name="right_lower_arm">
    <visual>
      <geometry>
        <cylinder length="0.3" radius="0.04"/>
      </geometry>
      <material name="grey"/>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.3" radius="0.04"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.8"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <joint name="right_elbow_joint" type="revolute">
    <parent link="right_upper_arm"/>
    <child link="right_lower_arm"/>
    <origin xyz="0 0 -0.3" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="0" upper="1.57" effort="10" velocity="1"/>
  </joint>
</robot>
```

## Using Xacro for Complex Humanoid Models

For more complex humanoid robots, Xacro (XML Macros) can simplify the URDF by allowing parameterization and reusability:

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="humanoid_with_xacro">
  <!-- Define properties -->
  <xacro:property name="M_PI" value="3.1415926535897931" />
  <xacro:property name="torso_mass" value="10.0" />
  <xacro:property name="arm_mass" value="1.0" />

  <!-- Macro for a simple arm -->
  <xacro:macro name="simple_arm" params="side reflect">
    <link name="${side}_upper_arm">
      <visual>
        <geometry>
          <cylinder length="0.3" radius="0.05"/>
        </geometry>
        <material name="grey"/>
      </visual>
      <collision>
        <geometry>
          <cylinder length="0.3" radius="0.05"/>
        </geometry>
      </collision>
      <inertial>
        <mass value="${arm_mass}"/>
        <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.001"/>
      </inertial>
    </link>

    <joint name="${side}_shoulder_joint" type="revolute">
      <parent link="torso"/>
      <child link="${side}_upper_arm"/>
      <origin xyz="0.2 ${0.15 * reflect} 0.1" rpy="0 0 0"/>
      <axis xyz="0 1 0"/>
      <limit lower="-1.57" upper="1.57" effort="10" velocity="1"/>
    </joint>

    <link name="${side}_lower_arm">
      <visual>
        <geometry>
          <cylinder length="0.3" radius="0.04"/>
        </geometry>
        <material name="grey"/>
      </visual>
      <collision>
        <geometry>
          <cylinder length="0.3" radius="0.04"/>
        </geometry>
      </collision>
      <inertial>
        <mass value="0.8"/>
        <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.001"/>
      </inertial>
    </link>

    <joint name="${side}_elbow_joint" type="revolute">
      <parent link="${side}_upper_arm"/>
      <child link="${side}_lower_arm"/>
      <origin xyz="0 0 -0.3" rpy="0 0 0"/>
      <axis xyz="0 1 0"/>
      <limit lower="-1.57" upper="0" effort="10" velocity="1"/>
    </joint>
  </xacro:macro>

  <!-- Use the macro to create both arms -->
  <xacro:simple_arm side="left" reflect="1"/>
  <xacro:simple_arm side="right" reflect="-1"/>
</robot>
```

## Common Humanoid Joint Configurations

### 6-DOF Arm Configuration
For more dexterous manipulation, humanoid robots often have 6+ degrees of freedom in each arm:
- Shoulder: 3 DOF (yaw, pitch, roll)
- Elbow: 1 DOF (pitch)
- Wrist: 2+ DOF (pitch, roll)

### 6-DOF Leg Configuration
For stable locomotion:
- Hip: 3 DOF (yaw, pitch, roll)
- Knee: 1 DOF (pitch)
- Ankle: 2 DOF (pitch, roll)

## Tips for Humanoid URDF Design

1. **Start Simple**: Begin with basic shapes and add complexity gradually
2. **Correct Mass Distribution**: Ensure masses and inertias are realistic
3. **Proper Joint Limits**: Set realistic joint limits to prevent self-collision
4. **Consistent Units**: Use meters for length, kilograms for mass
5. **Validation**: Always validate your URDF with `check_urdf`

## Exercises and Practical Examples

### Exercise 1: Create a Simple Robot Arm
Create a URDF file for a simple 3-DOF robot arm with base, upper arm, and lower arm links connected by revolute joints. Include proper visual, collision, and inertial properties.

### Exercise 2: Modify the Humanoid Model
Take the humanoid example and modify it to add simple hand links to each arm and adjust joint limits to prevent self-collision.

### Exercise 3: Xacro Practice
Convert the robot arm to use Xacro macros for reusability.

## Validating URDF Examples

Once you've created your URDF files, you should validate them using ROS 2 tools:

```bash
# Check URDF syntax and structure
check_urdf your_humanoid.urdf

# Or if using Xacro:
ros2 run xacro xacro your_humanoid.urdf.xacro > temp.urdf && check_urdf temp.urdf

# To visualize your robot in RViz:
# 1. Launch robot state publisher
ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:="`cat your_humanoid.urdf`"

# 2. Launch RViz in another terminal
ros2 run rviz2 rviz2

# In RViz, add a RobotModel display and set the topic to view your robot
```

## Summary

Creating URDF for humanoid robots requires careful attention to the kinematic structure, with proper joint types and limits to enable realistic movement patterns. Using Xacro can significantly simplify complex models with repetitive structures.