---
sidebar_position: 5
---

# Chapter 5: Dynamics and Control

## Introduction

If kinematics describes *how* a robot moves, **dynamics** explains *why* it moves. Dynamics is the study of motion in relation to the forces that cause it. It brings physics into the equation, accounting for concepts like mass, inertia, gravity, and the torques applied by motors.

Once we understand the dynamics of a robot, we can then apply the principles of **control theory** to command the motors to apply the correct forces and torques to achieve a desired motion. This chapter bridges the gap between the geometry of motion and the physical forces required to create it.

## 5.1 Forward Dynamics: From Torques to Motion

**Forward dynamics** answers the question: if I apply a specific set of torques to the robot's joints, what will be the resulting acceleration and subsequent motion of the robot?

This problem requires a complete physical model of the robot, including the mass, inertia, and center of mass for every single link. The relationship is captured in the **equations of motion**, which have the general form:

`τ = M(q)q̈ + C(q, q̇) + G(q)`

- `τ` (tau) is the vector of joint torques applied by the motors.
- `q`, `q̇`, and `q̈` are the position, velocity, and acceleration of the joints, respectively.
- `M(q)` is the **mass matrix** (or inertia matrix). It's a configuration-dependent matrix that represents the inertia of the entire robot.
- `C(q, q̇)` is the vector of **Coriolis and centrifugal forces**. These are complex forces that arise from the interaction of rotating links.
- `G(q)` is the vector of **gravity forces**, which depend on the robot's pose.

**Primary Application:** Forward dynamics is the engine of a physics-based robot simulator. By solving these equations over time, we can accurately predict how a robot will behave under a given set of motor commands, allowing us to develop and test control strategies in a safe virtual environment.

## 5.2 Inverse Dynamics: From Motion to Torques

**Inverse dynamics** tackles the opposite and more practical problem for control: if I want the robot to follow a specific trajectory (a path of desired joint positions, velocities, and accelerations), what are the exact torques that the motors must produce to create that motion?

By rearranging the equation of motion, we can solve for the required torques:

`τ = M(q)q̈_desired + C(q, q̇)_desired + G(q)`

**Primary Application:** This is the core of modern robot motion control. To make a robot arm move smoothly along a planned path, the controller uses this equation in real-time to calculate the feedforward torques required at every moment and sends them as commands to the motors.

## 5.3 Control Fundamentals: PID Control

The most fundamental concept in control is the **feedback loop**. We can't just send a command and hope for the best. Instead, we must:
1.  **Measure** the actual state of the system (e.g., the current joint angle from an encoder).
2.  **Compare** it to the desired state to find the **error**.
3.  **Use** that error to calculate a corrective command.

The **PID (Proportional-Integral-Derivative) controller** is the legendary workhorse of control engineering that has been used for decades to implement this loop.

- **Proportional (P):** The output is proportional to the current error (`Error`). It provides the primary corrective force. A large error results in a large correction.
- **Integral (I):** The output is proportional to the sum of all past errors (`∫Error dt`). This term works to eliminate small but persistent steady-state errors, such as a robotic arm drooping slightly under the force of gravity.
- **Derivative (D):** The output is proportional to the rate of change of the error (`d(Error)/dt`). This term acts as a damper, predicting future errors and slowing down the response to prevent the system from overshooting the target and oscillating.

The final control output is the sum of these three terms. PID controllers are simple, effective, and used in countless applications, from controlling individual robot joints to the cruise control in your car.

## 5.4 Advanced Control for Humanoids

While PID control is useful, the complex, unstable, and multi-tasking nature of a humanoid robot requires more advanced strategies.

- **Computed Torque Control:** This method combines the precision of a physical model with the robustness of a feedback loop. It uses the inverse dynamics model to calculate the primary torques needed to follow a trajectory (the feedforward term) and adds a PID feedback controller to correct for any small errors or unmodeled effects. This is far more accurate than simple PID control alone.

- **Whole-Body Control (WBC):** A humanoid robot needs to do many things at once. It must maintain balance, move its hands to a target, keep its head level, and look at an object, all while respecting joint limits and avoiding collisions. WBC is a framework that treats this as a prioritized, constrained optimization problem. The controller finds the best set of joint torques that satisfies all these tasks simultaneously, with balance almost always being the highest priority.

- **Zero-Moment Point (ZMP) and the Support Polygon:** For a bipedal robot to walk, it must control its balance. The **Zero-Moment Point (ZMP)** is the point on the ground where the net tipping-over torque (moment) from all inertial and gravitational forces is zero. To remain stable, the robot's controller must ensure that this ZMP always stays within the **support polygon**—the area formed by its feet on the ground. The planned trajectory of the ZMP is a cornerstone of most modern walking pattern generators for humanoid robots.