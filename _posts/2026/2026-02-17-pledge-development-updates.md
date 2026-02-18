---
layout: post
title: Pledge Development Updates
date: 2026-02-17T12:00:00-05:00
author: Cooperative Computing Lab
image: /assets/blog/2026/pledge-development-updates/pledge-figure.png
categories:
  - news
tags:
  - pledge
description: Our Pledge project continues to evolve, uncovering hidden dependencies in HPC scripts and making scalable workflows increasingly within reach.
toc: false
related_posts: false
---

<div class="row justify-content-sm-center">
<div class="col-sm-12">
{% include figure.liquid path="/assets/blog/2026/pledge-development-updates/pledge-figure.png" title="" class="img-fluid rounded z-depth-1" zoomable=true %}
</div>
</div>

Many HPC applications are composed of shell scripts which invoke one or more executables from a scientific software package. These applications can be distributed by sending the scripts out through a batch submission system, or they may invoke the batch system within the script along with configurations to determine scale and resource allocations.

There are a number of reasons one may wish to convert the application to use a higher-level workflow system which constructs a proper DAG. There could be missed concurrency opportunities, data movement bottlenecks, or the desire for portability to run on another system.

It can be a significant challenge to port an application to a task-based workflow system since the user must understand the dependencies of each application component. Executables often read and write to implicit locations and files which are not apparent from reading the script itself. The environment can influence the behavior of an application, causing it to function differently if run elsewhere or by another user.

In the past months the Pledge project has been under development with focus emphasized on observing or tracing a running application and creating a functional contract. The contract is a legible and comprehensive description of the application's I/O behavior. The user can read the contract to understand the implicit or unexpected behavior of their software.

The contract can also be further processed into a Makeflow application using the JX Expression language. With the application written in this format the user can make minimal edits to scale the application and run a distributed workflow using the TaskVine executor.

Check out the latest additions in the Pledge repository: https://github.com/cooperative-computing-lab/pledge
