---
layout: software3
title: "AllocFS: A Filesystem With Allocations"
show_title: true
description: "AllocFS is a filesystem that allows users to make guaranteed space allocations within an existing directory structure."
carousel: false
order: 9
skip_list: true
category: tools
publication_keywords:
  - allocfs
links:
  - name: User Manual
    url: https://ccl.cse.nd.edu/software/manuals/allocfs.html
---

Space allocation is a critical facility for making reliable data intensive computing systems. However, traditional operating systems do not make it easy to guarantee that space will be available for a future operation.

<div class="row justify-content-sm-center mt-3">
    <div class="col-sm-6">
        {% include figure.liquid path="assets/img/software/allocfs-logo.gif" class="img-fluid rounded z-depth-0" zoomable=true %}
    </div>
</div>

To address this limitation, we have developed **AllocFS** , a filesystem that allows users to make guaranteed space allocations within an existing directory structure. For example, the user simply issues **mkalloc /dir/name 25M** and receives a directory that is guaranteed to hold 25MB of data. Allocations are hierarchical, so this space can be further divided for other purposes.

**AllocFS** is a modified version of the production **ext2** filesystem. It is a loadable kernel module that uses the same on-disk layout as ext2, so the allocation facility can be added to (or removed from) an existing filesystem without reformatting.

## Software

- [AllocFS User Manual](manual.html)
- [allocfs-0.2-src.tar.gz](allocfs-src-0.2.tar.gz)
