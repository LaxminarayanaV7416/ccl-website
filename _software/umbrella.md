---
layout: software3
title: Umbrella Software Environment Specification
show_title: true
description: "Umbrella is a tool for specifying and materializing comprehensive execution environments, from the hardware all the way up to software and data. "
carousel: false
order: 10
skip_list: true
category: tools
publication_keywords:
  - umbrella
links:
  - name: User Manual
    url: https://ccl.cse.nd.edu/software/manuals/umbrella.html
---

Umbrella is a tool for specifying and materializing comprehensive execution environments, from the hardware all the way up to software and data. A user simply invokes Umbrella with the desired task, and Umbrella parses the specification, determines the minimum mechanism necessary to run the task, downloads missing dependencies, and executes the application through the available minimal mechanism, which may be direct execution, a system container ([Parrot](http://ccl.cse.nd.edu/software/parrot/), [Docker](https://www.docker.com/), [chroot](http://en.wikipedia.org/wiki/Chroot)), a local virtual machine (i.e., [VMware](http://www.vmware.com/)), or submission to a cloud environment (i.e., [Amazon EC2](http://aws.amazon.com/ec2/)) or grid environment (i.e., [HTCondor](http://research.cs.wisc.edu/htcondor/)).

<div class="row justify-content-sm-center mt-3">
    <div class="col-sm-6">
        {% include figure.liquid path="assets/img/software/umbrella-logo.png" class="img-fluid rounded z-depth-0" zoomable=true %}
    </div>
</div>

An Umbrella specification includes **six** sections: **hardware** , **kernel** , **os** , **software** , **data** , and **environ**. By specifying the dependencies of an application clearly and materializing the execution environment during runtime automatically, the application becomes **portable** and **reproducible**.

Umbrella involves multiple sandboxing and virtualization techniques, however, the key idea of Umbrella is to construct a sandbox for an application during runtime by **mounting** all the os, software, and data dependencies into a virtual root filesystem without copying them. The usage of mounting mechanism allows multiple sandboxes share the same dependencies concurrently.
