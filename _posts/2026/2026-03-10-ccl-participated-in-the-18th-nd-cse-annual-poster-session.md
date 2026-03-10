---
layout: post
title: CCL Participated in the 18th ND CSE Annual Poster Session
date: 2026-03-10T12:00:00-05:00
author: Cooperative Computing Lab
image:
categories:
  - news
tags:
  - news
  - poster-session
description: CCL team members presented eight research posters at the 18th ND CSE Annual Poster Session on February 26, 2026, spanning HEP workflows, DAG execution, reproducibility, digital agriculture, and LLM inference.
toc: false
related_posts: false
pinned_to_home: false
---

On February 26, 2026, we participated in the 18th ND CSE Annual Poster Session. It was a good chance for the lab to share what we've been working on. Here's a quick rundown of what everyone presented.

**Alan Malta** presented his work on large-scale HEP workflows. CMS and other LHC experiments run workflows across the Worldwide LHC Computing Grid, and the way you group and compose tasks can make a big difference in throughput and resource use. Alan built DAGFlowSim to explore the trade-offs between different workflow constructions (TaskChain vs StepChain and everything in between) and figure out which compositions work best for event throughput, CPU utilization, and network efficiency.

<div class="row justify-content-sm-center">
<div class="col-sm-12">
{% include figure.liquid path="/assets/blog/2026/ccl-participated-in-the-18th-nd-cse-annual-poster-session/Alan.png" title="Alan Malta Poster" class="img-fluid rounded z-depth-1" zoomable=true %}
</div>
</div>

**Barry Sly-Delgado** talked about restructuring workflows with algebraic labels. The idea is that if you can characterize operations by properties like commutativity and associativity, you can restructure the DAG for a better topology, with more parallelism, less overhead, and better fault tolerance. He integrated this with Dask and TaskVine and showed improvements on real HEP apps like RsTriPhoton, DVS, and tBar.

<div class="row justify-content-sm-center">
<div class="col-sm-12">
{% include figure.liquid path="/assets/blog/2026/ccl-participated-in-the-18th-nd-cse-annual-poster-session/Barry.png" title="Barry Sly-Delgado Poster" class="img-fluid rounded z-depth-1" zoomable=true %}
</div>
</div>

**Colin Thomas** presented Contour, a tool that traces the I/O of a running application and turns it into an "execution contract." Scientific apps often have implicit file dependencies that are hard to see from the script alone. Contour captures what gets read and written, then uses that to generate workflows for Makeflow so you can reproduce, distribute, and scale the app more reliably.

<div class="row justify-content-sm-center">
<div class="col-sm-12">
{% include figure.liquid path="/assets/blog/2026/ccl-participated-in-the-18th-nd-cse-annual-poster-session/Colin.png" title="Colin Thomas Poster" class="img-fluid rounded z-depth-1" zoomable=true %}
</div>
</div>

**Jin Zhou** presented DAGVine, which tackles a bottleneck we've been hitting: when you have lots of small tasks, serialization and dispatch overhead can dominate. DAGVine pre-compiles the whole dependency graph and installs it on workers, so at runtime you just send lightweight task references instead of shipping Python objects every time. In benchmarks it gets up to 82× higher throughput than DaskVine.

<div class="row justify-content-sm-center">
<div class="col-sm-12">
{% include figure.liquid path="/assets/blog/2026/ccl-participated-in-the-18th-nd-cse-annual-poster-session/Jin.png" title="Jin Zhou Poster" class="img-fluid rounded z-depth-1" zoomable=true %}
</div>
</div>

**Laxminarayana Vadnala** (Lax) presented SADE-SIM, a simulation platform for validating city-scale multi-drone operations. It combines physics simulation with photorealistic visualization so you can test autonomous UAV missions in realistic urban environments. His case study ran 32 heterogeneous drones over downtown Chicago with dynamic airspace policies. Only public-safety drones could enter a restricted zone, while others were deflected at the boundary.

<div class="row justify-content-sm-center">
<div class="col-sm-12">
{% include figure.liquid path="/assets/blog/2026/ccl-participated-in-the-18th-nd-cse-annual-poster-session/Lax.png" title="Laxminarayana Vadnala Poster" class="img-fluid rounded z-depth-1" zoomable=true %}
</div>
</div>

**Ryan Hartung** presented xGFabric, which connects sensors in the field with HPC facilities over 5G/6G networks for real-time digital agriculture. Sensors at UNL collect weather data, which flows over a private 5G cell to a base station, then to UCSB, and finally triggers an OpenFOAM simulation on an HPC cluster. The whole pipeline runs in near real time so you can steer the simulation based on what's happening in the field.

<div class="row justify-content-sm-center">
<div class="col-sm-12">
{% include figure.liquid path="/assets/blog/2026/ccl-participated-in-the-18th-nd-cse-annual-poster-session/Ryan.png" title="Ryan Hartung Poster" class="img-fluid rounded z-depth-1" zoomable=true %}
</div>
</div>

**Md Saiful Islam** presented his work on portable notebook workflows. Data-intensive notebooks are hard to move between HPC sites because of different storage, paths, and staging logic. Saiful's Backpack abstraction uses declarative data specs and fingerprinting to capture what's needed and run consistently across ND CRC, Anvil, and Stampede3. He demonstrated it on HEP analysis and image convolution workloads.

<div class="row justify-content-sm-center">
<div class="col-sm-12">
{% include figure.liquid path="/assets/blog/2026/ccl-participated-in-the-18th-nd-cse-annual-poster-session/Saiful.png" title="Md Saiful Islam Poster" class="img-fluid rounded z-depth-1" zoomable=true %}
</div>
</div>

**Thanh Son Phung** presented StickyInvoc, which rethinks how we run LLM inference at scale. The problem is that loading a model on a GPU is expensive, and on opportunistic clusters you might get preempted and have to reload over and over. StickyInvoc lets workers keep model state across tasks so subsequent inferences reuse it. In a claim verification workflow it hit 3.6× speedup, and scaled to 186 opportunistic GPU tasks in about 13 minutes.

<div class="row justify-content-sm-center">
<div class="col-sm-12">
{% include figure.liquid path="/assets/blog/2026/ccl-participated-in-the-18th-nd-cse-annual-poster-session/Thanh.png" title="Thanh Son Phung Poster" class="img-fluid rounded z-depth-1" zoomable=true %}
</div>
</div>

It was a great day to catch up with colleagues and share what we've been building. Thanks to everyone who stopped by our posters, and we look forward to the next one.
