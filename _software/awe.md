---
layout: software3
title: AWE - Accelerated Weighted Ensemble
show_title: true
description: Accelerated Weighted Ensemble or AWE package provides a Python library for adaptive sampling of molecular dynamics.
carousel: false
order: 10
skip_list: true
category: tools
publication_keywords:
  - awe
links:
  - name: User Manual
    url: https://ccl.cse.nd.edu/software/manuals/awe.html
  - name: Source Code
    url: https://github.com/cooperative-computing-lab/awe
---

Accelerated Weighted Ensemble or AWE package provides a Python library for adaptive sampling of molecular dynamics. The framework decomposes the resampling computations and the molecular dynamics simulations into tasks that are dispatched to [Work Queue](http://www.nd.edu/~ccl/software/workqueue/) for distribution and execution across allocated resources.

<div class="row justify-content-sm-center mt-3">
    <div class="col-sm-6">
        {% include figure.liquid path="assets/img/software/awe-logo.gif" class="img-fluid rounded z-depth-0" zoomable=true %}
    </div>
</div>

To use AWE, you write a Work Queue program using calls to the adpative sampler module. Then, run the `work_queue_worker` program on as many machines as you can access. You can start them manually, run them on the cloud, or submit them to systems like Condor or SGE. AWE will organize the machines into a workforce that, under the right conditions, can speed up protein folding by a hundred fold.

The output of AWE has been validated on the included Alanine Dipeptide protein and the WW domain dataset listed below.

## Sample Data

- [Inputs for WW protein domain](awe-ww-inputs.tar.gz)
