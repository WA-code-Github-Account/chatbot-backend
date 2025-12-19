# Part 2: Core Technologies

## Overview

Having established the foundations of humanoid robotics in Part 1, we now turn to the core technologies that enable robots to perceive, learn, and interact with their environment. This part bridges the gap between theoretical principles and practical implementation, introducing the sensors, algorithms, and software frameworks that power modern humanoid robots.

## What You'll Learn

### Chapter 6: Sensors and Perception
Discover the sensory systems that give robots awareness of their surroundings—from cameras and LiDAR to force/torque sensors and IMUs. Learn how raw sensor data is processed into meaningful environmental understanding.

### Chapter 7: Computer Vision
Explore how robots "see" the world through computer vision algorithms. Master object detection, tracking, semantic segmentation, and depth estimation techniques essential for robot navigation and manipulation.

### Chapter 8: Machine Learning
Understand how robots learn from data using supervised, unsupervised, and self-supervised learning paradigms. Dive into neural network architectures specifically designed for robotic applications.

### Chapter 9: Reinforcement Learning
Learn how robots discover optimal behaviors through trial and error. Explore policy gradient methods, value-based learning, and modern deep RL algorithms that enable robots to master complex tasks.

### Chapter 10: ROS (Robot Operating System)
Master the de facto standard middleware for robotics development. Learn how ROS enables modular robot software architecture, inter-process communication, and integration of diverse hardware and algorithms.

## The Perception-Action Loop

At the heart of every intelligent robot is the perception-action loop:

1. **Sense**: Gather data from the environment through sensors
2. **Perceive**: Process sensor data to understand the world state
3. **Decide**: Use learning algorithms to choose appropriate actions
4. **Act**: Execute motor commands to affect the environment
5. **Learn**: Update internal models based on outcomes

The technologies covered in this part implement each stage of this loop, transforming humanoid robots from mechanical sculptures into intelligent, adaptive systems.

## Prerequisites

Before starting Part 2, you should be comfortable with:
- Mathematical foundations from Part 1
- Python programming and NumPy
- Basic understanding of robot kinematics and dynamics
- Linear algebra and probability theory

## Practical Focus

Unlike Part 1's theoretical emphasis, Part 2 is deeply practical. You'll work with:
- Real sensor data and datasets
- Popular machine learning frameworks (PyTorch, TensorFlow)
- ROS simulation environments
- Computer vision libraries (OpenCV, detectron2)

Each chapter includes hands-on code examples and exercises designed to build your implementation skills.

## Industry Relevance

The technologies in this part are not just academic exercises—they power today's commercial humanoid robots:

- **Boston Dynamics Atlas**: Computer vision for terrain perception and obstacle avoidance
- **Tesla Optimus**: Deep learning for vision-based manipulation
- **Agility Robotics Digit**: Reinforcement learning for adaptive locomotion
- **Figure 01**: Vision-language models for natural task understanding

By mastering these core technologies, you'll be equipped to contribute to cutting-edge robotics projects.

## Learning Path

**Recommended Sequence**: Follow chapters 6→7→8→9→10 in order, as concepts build progressively.

**For Practitioners with ML Background**: You may skim Chapter 8 and focus more deeply on Chapters 7, 9, and 10 which are robotics-specific.

**For ROS Developers**: Chapter 10 will feel familiar, but earlier chapters provide essential context on the algorithms you'll integrate.

## What's Next?

After completing Part 2, you'll understand how robots perceive and learn. Part 3 will synthesize these technologies into complete systems for locomotion, manipulation, and human-robot interaction.

---

**Ready to explore sensors and perception? Turn to Chapter 6!**