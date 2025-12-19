---
sidebar_position: 7
---

# Chapter 7: Computer Vision

## Introduction

**Computer vision** is the science and technology of teaching machines to "see." It's a field of artificial intelligence that aims to extract meaningful information from images and videos, allowing a robot to understand the visual world. For a humanoid robot, vision is arguably the most important sense, providing a rich stream of data for navigating environments, avoiding obstacles, recognizing objects, and interacting with people.

This chapter dives into the core concepts of computer vision, from the classical techniques that laid the groundwork to the deep learning revolution that has enabled a new generation of powerful visual perception.

## 7.1 Image Fundamentals

An image, to a computer, is simply a large grid of numbers. Each number, called a **pixel**, represents the brightness or color at a specific point.

- **Color Spaces:** The most common color space is **RGB (Red, Green, Blue)**, where the color of each pixel is represented by three numbers. For many vision tasks, images are first converted to **grayscale**, where each pixel has only a single value representing its intensity from black to white.
- **Image Filtering:** A common first step in processing an image is to apply a filter to reduce noise. A **Gaussian blur**, for example, is a filter that averages each pixel with its neighbors, smoothing out the image and reducing random noise from the camera sensor.
- **Edge Detection:** Edges are one of the most fundamental features in an image. An **edge** is a curve that follows a path of rapid change in image intensity. Algorithms like the **Canny edge detector** are highly effective at extracting a clean, thin set of edges from an image, providing a basic "line drawing" of the scene.

## 7.2 The Deep Learning Revolution

For decades, computer vision relied on "hand-engineered" features. Researchers would design clever algorithms to detect specific patterns like corners, edges, and textures. A major breakthrough came with the rise of deep learning, and specifically, **Convolutional Neural Networks (CNNs)**.

A CNN is a special type of neural network that learns to recognize patterns in images directly from data. It does this using layers of "convolutional filters."

- **Intuition behind CNNs:** Imagine the first layer of filters learns to recognize simple patterns like horizontal, vertical, and diagonal edges. The next layer can then combine these edge patterns to recognize more complex shapes like corners and curves. The next layer might combine those to recognize parts of objects, like an eye or a wheel. By stacking these layers, a CNN can learn a hierarchical representation of the visual world, all automatically from labeled training data.

This ability to learn features automatically has led to superhuman performance on many vision tasks.

## 7.3 Core Vision Tasks in Robotics

Modern computer vision, powered by deep learning, allows a robot to perform several critical tasks:

- **Image Classification:** This is the task of assigning a single label to an entire image (e.g., "This is a photo of a cat"). While simple, it's the foundation for many more complex tasks.
- **Object Detection:** This task answers "What objects are in this image, and where are they?" The output is a set of **bounding boxes** drawn around each detected object, along with a class label for each box (e.g., "person," "cup," "table"). This is essential for a robot that needs to find and interact with specific objects. Popular and effective object detection models include **YOLO (You Only Look Once)**.
- **Semantic Segmentation:** This provides a much more detailed understanding of the scene. Instead of just drawing a box, semantic segmentation assigns a class label to *every single pixel* in the image. The output is an image that is "painted" with categories (e.g., all pixels belonging to people are colored blue, all pixels belonging to the road are colored gray). This is vital for navigation and scene understanding.
- **Instance Segmentation:** This is a step beyond semantic segmentation. It not only labels each pixel but also distinguishes between different instances of the same object class (e.g., "person 1" is colored blue, and "person 2" is colored green).

## 7.4 3D Computer Vision

A 2D image is a flat projection of a 3D world. For a robot to move and interact physically, it needs to recover the 3D structure of its environment.

- **Stereo Vision:** By using two cameras separated by a known distance (like human eyes), we can perceive depth. By identifying the same point in both the left and right images, we can measure the **disparity** (the difference in pixel location). A large disparity means the point is close, and a small disparity means it is far away. Using triangulation, this disparity can be converted into a depth value.
- **RGB-D Cameras:** These specialized cameras (like the Microsoft Kinect or Intel RealSense) directly provide 3D information. They typically project an invisible pattern of infrared light into the scene and measure its distortion to calculate the distance to every pixel. The output is a **depth image**, where each pixel's value represents its distance from the camera. This technology greatly simplifies many 3D perception problems.
- **Visual SLAM:** As introduced in the previous chapter, SLAM (Simultaneous Localization and Mapping) is the process of building a map while simultaneously tracking the robot's location. **Visual SLAM** refers to systems that use one or more cameras as their primary sensor. These systems track visual features from frame to frame to estimate the camera's motion and build a 3D map of the environment, often as a sparse point cloud of features or a dense 3D reconstruction.