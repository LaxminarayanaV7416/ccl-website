---
layout: software3
title: Makeflow
description: Makeflow is a workflow system for executing large complex workflows on clusters, clouds, and grids.
long_description: "Makeflow is a production-ready workflow system for executing large, complex scientific applications on clusters, clouds, and grids. Its language is similar to Make, allowing users to easily define workflows as directed acyclic graphs (DAGs) of tasks, from simple chains to thousands of jobs. Makeflow is portable across local machines, public clouds, batch systems, and container environments, enabling seamless migration between platforms. It is highly scalable and fault-tolerant, capable of running millions of jobs for extended periods, and provides analysis tools for monitoring and visualizing workflow performance. Makeflow is widely used in fields such as data mining, physics, image processing, and bioinformatics."
img: assets/img/software/makeflow-logo.png
carousel: false
order: 4
category: work
publication_keywords:
  - makeflow
links:
  - name: Install
    url: https://cctools.readthedocs.io/en/latest/install/
  - name: User Manual
    url: https://cctools.readthedocs.io/en/stable/makeflow/
  - name: Tutorial Slides
    url: /assets/pdf/intro-makeflow-workqueue.pdf
  - name: Example Repository
    url: https://github.com/cooperative-computing-lab/makeflow-examples
---

Makeflow is a workflow system for executing large complex workflows on clusters, clouds, and grids.

Makeflow is easy to use. The Makeflow language is similar to traditional Make, so if you can write a Makefile, then you can write a Makeflow. A workflow can be just a few commands chained together, or it can be a complex application consisting of thousands of tasks. It can have an arbitrary DAG structure and is not limited to specific patterns.

<div class="row justify-content-sm-center">
    <div class="col-sm-12">
        {% include figure.liquid path="assets/img/software/makeflow-banner.png" class="img-fluid rounded z-depth-0" zoomable=true %}
    </div>
</div>

Makeflow is production-ready. Makeflow is used on a daily basis to execute complex scientific applications in fields such as data mining, high energy physics, image processing, and bioinformatics. It has run on campus clusters, the Open Science Grid, NSF XSEDE machines, NCSA Blue Waters, and Amazon Web Services. Here are some real examples of workflows used in production systems:

Makeflow is portable. A workflow is written in a technology neutral way, and then can be deployed to a variety of different systems without modification, including local execution on a single multicore machine, public cloud services such as Amazon EC2 and Amazon Lambda, batch systems like HTCondor, SGE, PBS, Torque, SLURM, or the bundled Work Queue system. Makeflow can also easily run your jobs in a container environment like Docker or Singularity on top of an existing batch system. The same specification works for all systems, so you can easily move your application from one system to another without rewriting everything.

Makeflow is powerful. Makeflow can handle workloads of millions of jobs running on thousands of machines for months at a time. Makeflow is highly fault tolerant: it can crash or be killed, and upon resuming, will reconnect to running jobs and continue where it left off. A variety of analysis tools are available to understand the performance of your jobs, measure the progress of a workflow, and visualize what is going on.

## Video Introduction to Workflows

<div class="row mt-3">
    <div class="col-sm-12">
        {% include video.liquid path="https://www.youtube.com/embed/Ogpu4L-nDJE" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
