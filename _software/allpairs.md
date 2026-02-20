---
layout: software3
title: All-Pairs Abstraction
show_title: true
description: The All-Pairs abstraction computes the Cartesian product of two sets, generating a matrix where each cell M[i,j] contains the output of the function F on objects A[i] and B[j].
carousel: false
order: 10
skip_list: true
category: tools
publication_keywords:
  - allpairs
links:
  - name: User Manual
    url: https://github.com/cooperative-computing-lab/work-queue-examples/blob/master/wq_allpairs/README.md
---

<div class="row justify-content-sm-center mt-3">
    <div class="col-sm-6">
        {% include figure.liquid path="assets/img/software/allpairs-logo.gif" class="img-fluid rounded z-depth-0" zoomable=true %}
    </div>
</div>

The All-Pairs abstraction computes the Cartesian product of two sets, generating a matrix where each cell M[i,j] contains the output of the function F on objects A[i] and B[j]. You provide two sets of data files and a function F that computes on them. You may optionally provide additional parameters to control the actual computation(e.g. compute only part of the matrix). The abstraction then executes the computation in parallel, automatically handling load balancing, data movements, fault tolerance, and so on.
