---
layout: software3
title: Parrot
description: "Parrot is a transparent user-level virtual filesystem that allows any ordinary program to be attached to many different remote storage services. Parrot captures the system calls (open, read, write, stat, etc) of an application through the ptrace interface, and redirects them to remote services such as HDFS, iRODS, Chirp, and FTP. This allows one to construct custom distributed filesystems on clusters without requiring special privileges."
long_description: "Parrot is a transparent user-level virtual filesystem that allows any ordinary program to be attached to many different remote storage services. Parrot captures the system calls (open, read, write, stat, etc) of an application through the ptrace interface, and redirects them to remote services such as HDFS, iRODS, Chirp, and FTP. This allows one to construct custom distributed filesystems on clusters without requiring special privileges."
img: assets/img/software/parrot-logo.png
carousel: false
order: 7
category: tools
publication_keywords:
  - parrot
links:
  - name: Install
    url: https://cctools.readthedocs.io/en/latest/install/
  - name: User Manual
    url: https://ccl.cse.nd.edu/software/manuals/parrot.html
---

The Parrot Virtual File System is a tool for attaching existing programs to remote I/O systems through the filesystem interface. For example, here's how to use Parrot with vi in order to edit a file on a remote file server:

```
% parrot_run vi /chirp/server.nd.edu/mydata
```

Parrot "speaks" a variety of remote I/O services include HTTP, FTP, [GridFTP](http://toolkit.globus.org/toolkit/docs/latest-stable/gridftp), [iRODS](http://www.irods.org), [CVMFS](http://cernvm.cern.ch/portal/filesystem), and [Chirp](/~ccl/software/chirp) on behalf of ordinary programs. It works by trapping a program's system calls through the `ptrace` debugging interface, and replacing them with remote I/O operations as desired. Parrot can be installed and operated by any user **without special privileges or kernel changes** and can be applied to **almost any program** without re-writing, re-linking, or re-installing.

<div class="row justify-content-sm-center mt-3">
    <div class="col-sm-6">
        {% include figure.liquid path="assets/img/software/parrot-poster.gif" class="img-fluid rounded z-depth-0" zoomable=true %}
    </div>
</div>

Parrot is particularly useful for running batch jobs in large scale distributed systems. It is most widely used to provide access to [high energy physics](/assets/pdf/oppo-ccgrid14.pdf) (HEP) software stacks via the global [CVMFS](http://cernvm.cern.ch/portal/filesystem) filesystem developed at CERN. Because Parrot views every operation on the filesystem, it can make arbitrary changes to an application's namespace. This allows it to function as a [sandbox environment](/assets/pdf/ibox-sc05.pdf), a [dependency tracing tool](/assets/pdf/invariant-jocs-2015.pdf), [virtual machine](/assets/pdf/umbrella-vtdc15.pdf), and more.

(Note that Parrot is very tightly coupled with the OS kernel. and so it is only available on Linux based operating systems.)
