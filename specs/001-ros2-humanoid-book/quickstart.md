# Quickstart: ROS 2 Humanoid Robotics Book Module

## Prerequisites

Before starting with this module, ensure you have:

- ROS 2 Humble Hawksbill installed on your system
- Basic Python programming knowledge
- Familiarity with command-line tools
- Git for version control (optional but recommended)

## Setting Up Your Environment

### 1. Install ROS 2 Humble

Follow the official installation guide for your operating system:
- Ubuntu: [ROS 2 Humble Installation](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html)
- Windows: [ROS 2 Humble Installation](https://docs.ros.org/en/humble/Installation/Windows-Install-Binary.html)
- macOS: [ROS 2 Humble Installation](https://docs.ros.org/en/humble/Installation/macOS-Install-Binary.html)

### 2. Verify Installation

Test that ROS 2 is properly installed:

```bash
source /opt/ros/humble/setup.bash
ros2 --version
```

You should see the ROS 2 version information.

### 3. Create a Workspace

Create a workspace for your ROS 2 practice:

```bash
mkdir -p ~/ros2_book_ws/src
cd ~/ros2_book_ws
colcon build
source install/setup.bash
```

## First Steps with ROS 2

### 1. Run Your First ROS 2 Node

In one terminal, run:
```bash
ros2 run demo_nodes_cpp talker
```

In another terminal, run:
```bash
ros2 run demo_nodes_py listener
```

You should see messages being passed between the nodes.

### 2. Understanding the Basics

- **Nodes**: Individual components of your ROS system
- **Topics**: Communication channels between nodes
- **Messages**: Data sent over topics
- **Services**: Request/response communication pattern

## Working with the Book Content

### Docusaurus Documentation Setup

If you want to build the documentation locally:

1. Install Node.js (version 18 or higher)
2. Clone the repository
3. Navigate to the documentation directory
4. Install dependencies:

```bash
npm install
```

5. Start the development server:

```bash
npm start
```

The documentation will be available at http://localhost:3000

## Running Code Examples

All code examples in this book are designed to work with ROS 2 Humble. To run an example:

1. Create a new package in your workspace:

```bash
cd ~/ros2_book_ws/src
ros2 pkg create --build-type ament_python my_example_pkg
```

2. Add the example code to the appropriate directory
3. Build the package:

```bash
cd ~/ros2_book_ws
colcon build --packages-select my_example_pkg
source install/setup.bash
```

4. Run the example:

```bash
ros2 run my_example_pkg example_node
```

## Troubleshooting Common Issues

### ROS 2 Environment Not Sourced

If you get "command not found" errors for ROS 2 commands:

```bash
source /opt/ros/humble/setup.bash
```

### Package Build Errors

If you encounter build errors, ensure all dependencies are installed:

```bash
sudo apt update
rosdep update
rosdep install --from-paths src --ignore-src -r -y
```

## Next Steps

1. Proceed to Chapter 1: ROS 2 Basics for Humanoid Control
2. Practice the examples in each section
3. Complete the exercises at the end of each chapter
4. Build your own simple ROS 2 nodes to reinforce learning

## Getting Help

- Refer to the official ROS 2 documentation: https://docs.ros.org/en/humble/
- Use the ROS Discourse forum for questions: https://discourse.ros.org/
- Check the ROS Answers site: https://answers.ros.org/questions/