// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Introduction',
      items: ['intro'],
      link: {
        type: 'generated-index',
        description: 'Getting started with ROS 2 for humanoid robotics',
      },
    },
    {
      type: 'category',
      label: 'ROS 2 Basics for Humanoid Control',
      link: {
        type: 'generated-index',
        description: 'Fundamental concepts of ROS 2 middleware for humanoid robots',
      },
      items: [
        'ros2-basics/index',
        'ros2-basics/nodes-topics-services',
        'ros2-basics/practical-examples'
      ],
    },
    {
      type: 'category',
      label: 'Python Agents to ROS 2 Controllers',
      link: {
        type: 'generated-index',
        description: 'Using Python and rclpy for ROS 2 control',
      },
      items: [
        'python-control/index',
        'python-control/rclpy-fundamentals',
        'python-control/controller-implementation'
      ],
    },
    {
      type: 'category',
      label: 'The Digital Twin (Gazebo & Unity)',
      link: {
        type: 'generated-index',
        description: 'Simulation environments for humanoid robotics digital twins',
      },
      items: [
        'module-2/2.1-physics-in-gazebo',
        'module-2/2.2-unity-rendering-for-hri',
        'module-2/2.3-sensor-streams'
      ],
    },
    {
      type: 'category',
      label: 'URDF Structure for Humanoids',
      link: {
        type: 'generated-index',
        description: 'Unified Robot Description Format for humanoid robots',
      },
      items: [
        'urdf-modeling/index',
        'urdf-modeling/structure-basics',
        'urdf-modeling/humanoid-examples',
        'urdf-modeling/urdf-visualization'
      ],
    },
    {
      type: 'category',
      label: 'Reference',
      items: ['glossary'],
      link: {
        type: 'doc',
        id: 'glossary',
      },
    },
  ],
};

module.exports = sidebars;