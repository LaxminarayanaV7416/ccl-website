---
layout: software3
title: Resource_monitor
description: "The Resource Monitor (RM) is used to accurately capture the resource consumption (CPU, RAM, I/O, Disk, GPU, etc) of applications running in distributed systems. Production applications are typically not single processes, but complex assemblies of scripts, libraries, and processes written in multiple languages. The resource monitor tracks all components accurately and provides the enforcement needed to execute applications reliable at scale."
long_description: "The Resource Monitor (RM) is used to accurately capture the resource consumption (CPU, RAM, I/O, Disk, GPU, etc) of applications running in distributed systems. Production applications are typically not single processes, but complex assemblies of scripts, libraries, and processes written in multiple languages. The resource monitor tracks all components accurately and provides the enforcement needed to execute applications reliable at scale."
img: assets/img/software/resource-monitor-logo.png
carousel: false
order: 6
category: tools
publication_keywords:
  - resource_monitor
links:
  - name: Install
    url: https://cctools.readthedocs.io/en/latest/install/
  - name: User Manual
    url: https://ccl.cse.nd.edu/software/manuals/resource_monitor.html
---

The `resource_monitor` is a tool to monitor the computational resources of complex, multi-process applications. This is an essential capability for executing large scale applications reliably in clusters, clouds, and grids. It works on Linux, FreeBSD, and OSX, and can be used as a standalone tool, or automatically with distributed systems like [Makeflow](../makeflow), [Work Queue](../workqueue) and [TaskVine](../taskvine).

When invoked, the resource monitor tracks all of the processes and threads created by the subject program, and monitors their individual resource and I/O behavior. It generates up to three report files: a summary file with the maximum values of resource used, a time-series that shows the resources used at given time intervals, and a list of files that were opened during execution, together with the count of read and write operations.

Additionally, the monitor can be used as a watchdog. Maximum resource limits can be specified, and if one of the resources goes over the limit, then the monitor terminates the task, including a report of the resource that was above the limit.

<div class="row justify-content-sm-center">
    <div class="col-sm-6">
        {% include figure.liquid path="assets/img/software/cpu_time_600x600_hist.png" class="img-fluid rounded z-depth-0" zoomable=true %}
    </div>
</div>

The `resource_monitor_visualizer` creates a series of webpages summarizing the logs produced by the `resource_monitor`. It generates histograms for each resource and each group. For example, the histogram to the right shows the distribution of cpu usage of a workflow with 5,000 tasks. To use the `resource_monitor_visualizer` specify the location of the resource logs and the location for the output.
