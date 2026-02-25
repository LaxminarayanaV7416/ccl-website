---
layout: project
title: "Filesystems for Grid Computing"
subtitle: "PI: Douglas Thain, University of Notre Dame"
description: "Description goes here."
order: 9
skip_list: true
category: work
carousel: false
publication_keywords:
  - gridfs
---

Grid computing systems such as the [Open Science Grid](http://www.opensciencegrid.org) and the [NSF TeraGrid](http://www.teragrid.org) give users easy access to hundreds or thousands of CPUs at once. However, within computing grids, it is not always easy to access one's data. Traditional filesystems such as NFS and AFS are not usable in most grid computing systems, because they require privileged access to install and use at both client and server side. A user of grid computing rarely has such access.

To remedy this problem, we have designed and implemented a variety of filesystems for grid computing, all based on the [Parrot](/software/parrot) and [Chirp](/software/chirp) software. These user-level tools can be deployed without special privileges into existing grids, and used to access data wherever it may be located. We work directly with users in bioinformatics and high energy physics to design and deploy production filesystem services. You can download and use our software [from this page](https://cctools.readthedocs.io/en/latest/install/).
