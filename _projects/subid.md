---
layout: project
title: "Sub Identities: Practical Containment for Distributed Systems"
subtitle: "This work is supported by the National Science Foundation under grant CNS-05-49087"
description: "Description goes here."
order: 9
skip_list: true
category: work
carousel: false
---

Current operating systems are poorly equipped to deal with the demands of distributed and grid computing systems. Traditional workstations are overprovisioned in resources and serve a handful of non-competing users. However, distributed and grid computing systems are usually overcommitted and accessed by many competing users. The local operating system is often a point of failure under these conditions. To address this problem, we are creating lightweight operating system mechanisms that allow ordinary users to protect, name, limit, and manage both names and resources without becoming the superuser.

### Sub-Identities

A simple example of this is the matter of identifying users. An ordinary user would like to be able to create protection domains in order to run untrusted code coming in from the grid or downloaded from the web. But, creating accounts is limited to the superuser, partially because of the simple data structure (an integer) used to represent a user internally. Strangely, in order to **restrict** the privilege of a sub-process, one must fist **elevate** privilege to become the superuser.

<div class="row justify-content-sm-center mt-3">
    <div class="col-sm-6">
        {% include figure.liquid path="assets/img/projects/ccl-nested.ps.gif" class="img-fluid rounded z-depth-0" zoomable=true %}
    </div>
</div>

One way to improve this situation is to introduce **sub-identities**. In this model, any user can create a sub-user which is named relative to the user that created it. For example, the root user would still be `root`, but I would become `root:joe`. If I were to create a temporary account for a visiting user, it would be `root:joe:afriend`. In this way, each user can dynamically create protection zones that allow for visiting users as well as untrusted programs.

- [Sub-Identities: A Hierarchical Identity Model for Practical Containment](/assets/pdf/snowberger-ms-thesis.pdf), Philip Snowberger, MS CSE Thesis, University of Notre Dame, April 2007.
- [Sub-Identity: Security for Mere Mortals](http://www.nd.edu/~dthain/papers/subid-usesec06.pdf), Phil Snowberger and Douglas Thain, presented at the USENIX Security Symposium, 3 August 2006.
- [Sub-Identities: Towards Operating System Support for Distributed System Security](http://www.nd.edu/~dthain/papers/subid-tr.pdf),Phil Snowberger and Douglas Thain, Technical Report 2005-18, University of Notre Dame, Department of Computer Science and Engineering, October 2005.
- [SubID Software Package](/software/subid)

### Hierarchical Space Allocation

<div class="row justify-content-sm-center mt-3">
    <div class="col-sm-6">
        {% include figure.liquid path="assets/img/projects/alloc-model.gif" class="img-fluid rounded z-depth-0" zoomable=true %}
    </div>
</div>

Another example of this problem is space allocation in the filesystem. Grid computing systems often fail because of overcommitted storage. Many jobs and tasks share the same filesystem; if one accidentally (or deliberately) fills up the space, everything using that space will fail.

In the same spirit as sub-identities, we have created AllocFS, a filesystem that allows ordinary users to create and subdivide space allocations. These can be employed by a grid-level job or disk manager to improve the reliability of a grid computing system. We have demonstrated how adding such a facility to the head node of a cluster can make it far more reliable under load.

- [Operating System Support for Space Allocation in Grid Storage Systems](../papers/alloc-grid06.pdf), Douglas Thain, IEEE Conference on Grid Computing, September 2006.
- [Implementation Tradeoffs in Storage Allocation for Grid Computing](../papers/alloc-tr.pdf), Douglas Thain, Technical Report 2006-04, Univ of Notre Dame, Computer Science and Engineering Dept, May 2006.
- [AllocFS Software Package](../../software/allocfs)

### Lockdown: Network Managed Containment

While there exist meny mechanisms for managing security on a _single host_ (such as sub-identities), security is truly a system-wide problem that spans multiple users, applications, and hosts connected via a network. The traditional tool for managing network security is the firewall, which either permits or denies traffic based on the address and port of the source and target. However, this is a very coarse tool: a comprehensive network security policy is usually not concerned with hosts and ports, but with users and applications. A trusted application may be allowed to use the network at will, while an unknown user or application should not be allowed to use it at all. [![](lockdown.gif)](lockdown-usenix07.pdf)

To remedy this, we introduce the **Lockdown** system. Lockdown consists of a centrally managed database governing network policy, managed by the cognizant network security officer. The database controls what **users** and **applications** are allowed to talk to each other over the network. Fragments of the database are pushed out to end hosts, which are equipped with a reference monitor that allows or denies connections according to the policy. In this way, a more expressive policy can be stated and enforced in conventional systems.

- [Lockdown: Distributed Policy Analysis and Enforcement within the Enterprise Network](/assets/pdf/lockdown-security07.pdf),  
  Andrew Blaich, Qi Liao, Greg Allan, Aaron Striegel, and Douglas Thain, Poster presented at USENIX Security Conference 2007.
