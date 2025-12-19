---
sidebar_position: 12
---

# Chapter 12: Balance and Locomotion

## Introduction

Bipedal (two-legged) locomotion is the defining feature and, without a doubt, the greatest technical challenge of humanoid robotics. Unlike a car or a four-legged animal, which are often **statically stable** (able to stand still without active effort), a humanoid robot is an inherently unstable system. It is always, in a sense, an act of controlled falling.

Mastering balance and locomotion is the key that unlocks a humanoid's potential. The ability to walk, run, and navigate complex terrain is what allows a robot to move through human-centric environments and perform useful tasks. This chapter delves into the fundamental principles and advanced strategies behind this remarkable capability.

## 12.1 The Fundamentals of Balance

To understand balance, we must first understand two key concepts:

- **Center of Mass (CoM):** This is the single, imaginary point where the entire mass of the robot can be considered to be concentrated. The control of this point is the primary goal of all balance strategies.
- **Support Polygon:** This is the area on the ground enclosed by all the points where the robot is in contact with the environment. For a robot standing on two feet, it is the area that includes both feet and the space between them.

The golden rule of **static balance** (standing still) is simple: the robot is stable if and only if the vertical projection of its Center of Mass onto the ground lies within the support polygon. If the CoM moves outside this area, the robot will begin to tip over.

## 12.2 Walking: A Controlled Fall

Walking is a dynamic process. It involves repeatedly letting the body fall forward and then catching itself with the next step.

### The Gait Cycle
A walking pattern, or **gait**, is a cycle of repeating motions. The main phases are:
- **Stance Phase:** The period when a foot is on the ground, providing support.
- **Swing Phase:** The period when a foot is in the air, swinging forward to a new position.
- **Double Support:** The brief phase in walking when both feet are on the ground simultaneously. This is a very stable phase.
- **Single Support:** The phase when the robot is balanced on only one foot. This is the most unstable part of the gait cycle.

### Zero-Moment Point (ZMP) Walking
As introduced in Chapter 5, the most common method for generating stable walking patterns is based on the **Zero-Moment Point (ZMP)**. The ZMP is the point on the ground where the net tipping-over forces (moments) are zero. As long as the ZMP stays within the support polygon, the robot will not fall.

The process of ZMP-based gait generation typically involves:
1.  Planning a desired trajectory for the robot's Center of Mass.
2.  From the CoM trajectory, calculating the required ZMP trajectory.
3.  Planning the footsteps (placement of the support polygons) to ensure the ZMP trajectory always remains within them.
4.  Using the robot's full-body inverse kinematics and dynamics controllers to calculate the joint motions needed to produce this physically-consistent CoM and ZMP motion.

A common simplification used in gait generation is the **Inverted Pendulum Model**, which models the robot as a single point mass (the CoM) on top of a massless leg. This simple model is incredibly powerful for quickly calculating stable CoM and ZMP trajectories.

## 12.3 Beyond Walking: Dynamic Locomotion

While ZMP walking is stable, it can be slow and robotic. Achieving more human-like, dynamic locomotion requires more advanced techniques.

- **Running:** The key difference between walking and running is the presence of a **flight phase**, where both feet are off the ground. This requires the robot to project itself into the air and land gracefully, which demands much more powerful actuators and faster control systems.
- **Agile Behaviors:** The cutting edge of locomotion research involves highly dynamic and non-repetitive behaviors, such as those demonstrated by Boston Dynamics' Atlas robot. Achieving running, jumping, and gymnastics requires controllers that can reason about the robot's full-body dynamics and momentum. These controllers often use techniques like **Model Predictive Control (MPC)**, where the robot is constantly re-planning its trajectory a short time into the future based on its current state.

## 12.4 Balance Recovery Strategies

What happens when the robot gets pushed or trips? It must have a hierarchy of strategies to recover its balance.

1.  **Ankle Strategy:** For small disturbances (like standing on a slightly swaying bus), the robot can recover by simply actuating its ankle joints. This shifts the robot's Center of Pressure (the point where the force is applied to the ground) to counteract the sway and re-center the CoM.
2.  **Hip Strategy:** For larger or faster disturbances, the ankle strategy is not enough. The robot must use its powerful hip and waist joints to quickly move its upper body, which shifts the CoM back over the support polygon.
3.  **Stepping Strategy:** For very large disturbances where the CoM is pushed completely outside the support polygon, the only way to prevent a fall is to take a step. The robot quickly moves one of its feet to a new location, effectively "catching" the falling CoM with a new support polygon. This is the most robust recovery strategy and is essential for any humanoid that operates in the real world.

The ability to seamlessly transition between these strategies is a hallmark of an advanced balance controller.