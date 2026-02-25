---
layout: software3
title: The Wavefront Abstraction
show_title: true
description: The Wavefront abstraction is used to express computations on a two-dimensional grid where each cell depends on its neighboring cells.
carousel: false
order: 9
skip_list: true
category: tools
publication_keywords:
  - wavefront
links:
  - name: User Manual
    url: https://github.com/cooperative-computing-lab/work-queue-examples/tree/master/wq_wavefront#readme
---

The Wavefront abstraction computes a two dimensional recurrence relation. You provide a function F that accepts the left (x), right (y), and diagonal (d) values and initial values for the edges of the matrix. You may optionally provide additional parameters for each cell, given by a matrix P. The abstraction then runs each of the functions in the order of dependency, handling load balancing, data movement, fault tolerance, and so on.

<div class="row justify-content-sm-center mt-3">
    <div class="col-sm-6">
        {% include figure.liquid path="assets/img/software/wavefront-logo.gif" class="img-fluid rounded z-depth-0" zoomable=true %}
    </div>
</div>
