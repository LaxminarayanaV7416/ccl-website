---
layout: software3
title: The Confuga Cluster File System
show_title: true
description: Description goes here.
long_description: "Description goes here."
carousel: false
order: 10
skip_list: true
category: tools
publication_keywords:
  - confuga
links:
  - name: User Manual
    url: https://ccl.cse.nd.edu/software/manuals/confuga.html
---

<!-- ![](Confuga Architecture.svg) -->

Confuga is an active storage cluster file system designed for executing DAG-structured scientific workflows. It is used as a collaborative distributed file system and as a platform for execution of scientific workflows with full data locality for all job dependencies.

<div class="row justify-content-sm-center mt-3">
    <div class="col-sm-8">
        {% include figure.liquid path="assets/img/software/confuga-logo.svg" class="img-fluid rounded z-depth-0" zoomable=true %}
    </div>
</div>

Confuga is composed of a head node and multiple storage nodes. The head node acts as the metadata server and job scheduler for the cluster. Users interact with Confuga using the head node.

A Confuga cluster can be setup as an ordinary user or maintained as a dedicated service within the cluster. The head node and storage nodes run the [Chirp](../chirp/) file system service. Users may interact with Confuga using Chirp's client toolset [chirp(1)](https://cctools.readthedocs.io/en/stable/man_pages/chirp/), [Parrot](../parrot/) [parrot_run(1)](https://cctools.readthedocs.io/en/stable/man_pages/parrot_run/), or [FUSE](https://cctools.readthedocs.io/en/stable/chirp/#access) [chirp_fuse(1)](https://cctools.readthedocs.io/en/stable/man_pages/chirp_fuse/).

Confuga manages the details of scheduling and executing jobs for you. However, it does not concern itself with job ordering; it appears as a simple batch execution platform. We recommend using a high-level workflow execution system like [Makeflow](../makeflow/) to manage your workflow and to handle the details of submitting jobs.

Confuga is designed to exploit the unique parameters and characteristics of POSIX scientific workflows. Jobs are single task POSIX applications that are expressed with all input files and all output files. Confuga uses this restricted job specification to achieve performance and to control load within the cluster.
