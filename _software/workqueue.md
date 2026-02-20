---
layout: software3
title: Work Queue
description: Work Queue is an application framework for creating and managing dynamic manager-worker style programs that scale up to tens of thousands of machines on clusters, clouds, and grids.
long_description: "Work Queue is a framework for building large distributed applications that span thousands of machines drawn from clusters, clouds, and grids. Work Queue applications are written in Python, Perl, or C using a simple API that allows users to define tasks, submit them to the queue, and wait for completion. Tasks are executed by a general worker process that can run on any available machine. Each worker calls home to the manager process, arranges for data transfer, and executes the tasks. A wide variety of scheduling and resource management features are provided to enable the efficient use of large fleets of multicore servers. The system handles a wide variety of failures, allowing for dynamically scalable and robust applications."
img: assets/img/software/work-queue-logo.png
carousel: true
order: 3
category: work
publication_keywords:
  - workqueue
links:
  - name: Install
    url: https://cctools.readthedocs.io/en/latest/install/
  - name: User Manual
    url: https://cctools.readthedocs.io/en/stable/work_queue/
  - name: Example Repository
    url: https://github.com/cooperative-computing-lab/work-queue-examples
---

Work Queue is a framework for building large distributed applications that span thousands of machines drawn from clusters, clouds, and grids. Work Queue applications are written in Python, Perl, or C using a simple API that allows users to define tasks, submit them to the queue, and wait for completion. Tasks are executed by a general worker process that can run on any available machine. Each worker calls home to the manager process, arranges for data transfer, and executes the tasks. A wide variety of scheduling and resource management features are provided to enable the efficient use of large fleets of multicore servers. The system handles a wide variety of failures, allowing for dynamically scalable and robust applications.

## Who Uses Work Queue?

Work Queue has been used to write applications that
scale from a handful of workstations up to tens of thousands
of cores running on supercomputers.
Examples include the [Parsl](http://parsl-project.org) workflow system, the [Coffea](https://github.com/CoffeaTeam/coffea) analysis framework, the [Makeflow](../makeflow) workflow engine, [SHADHO](https://shadho.readthedocs.io/en/latest/hyperparam.html), [Lobster](http://cclnd.blogspot.com/2015/05/cms-analysis-on-10k-cores-with-lobster.html), [NanoReactors](http://cclnd.blogspot.com/2014/11/work-queue-powers-nanoreactor.html), [ForceBalance](https://simtk.org/home/forcebalance), [Accelerated Weighted Ensemble](../awe), the [SAND genome assembler](../sand), and the [All-Pairs](../allpairs) and [Wavefront](../wavefront) abstractions.

The framework is easy to use, and has been used to teach courses in parallel computing, cloud computing, distributed computing, and cyberinfrastructure at the University of Notre Dame, the University of Arizona, the University of Wisconsin, and many other locations.

## Video Introduction to Work Queue

<div class="row mt-3">
    <div class="col-sm-12">
        {% include video.liquid path="https://www.youtube.com/embed/uhI_2ABnfPQ" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
