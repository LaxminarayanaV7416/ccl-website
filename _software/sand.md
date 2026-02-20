---
layout: software3
title: SAND - Scalable Assembly at Notre Dame
show_title: true
description: SAND - Scalable Assembly at Notre Dame
carousel: false
order: 10
skip_list: true
category: tools
publication_keywords:
  - sand
links:
  - name: User Manual
    url: https://ccl.cse.nd.edu/software/manuals/sand.html
---

SAND is a set of modules for genome assembly that are built atop the [Work Queue](http://www.nd.edu/~ccl/software/workqueue/) platform for large-scale distributed computation on clusters, clouds, or grids. SAND was designed as a modular replacement for the conventional overlapper in the Celera assembler, separated into two distinct steps: candidate filtering and alignment.

<div class="row justify-content-sm-center mt-3">
    <div class="col-sm-6">
        {% include figure.liquid path="assets/img/software/sand-logo.gif" class="img-fluid rounded z-depth-0" zoomable=true %}
    </div>
</div>

To use SAND, you start your assembly process as normal, then run a lightweight `worker` program on as many other machines as you can access. You can start them manually, run them on the cloud, or submit them to systems like Condor or SGE. SAND will organize the machines into a workforce that, under the right conditions, can speed up assembly tasks by several hundred fold.

The correct output of SAND has been validated on the anopheles gambiae, sorghum bicolor, and homo sapiens datasets listed below.

## Sample Data

The following are the datasets used for evaluating SAND in our various publications. The `.cfa` data format is binary Compressed FAsta, which can be converted to/from plain text FASTA files using `sand_compress_reads` and `sand_uncompress_reads`.

**(Note: We are in the middle of restoring these datasets from backup. The small, medium, and large datasets are available for download. The repeat files are currently being regenerated. The human dataset is still being restored.)**

| Sequence Data                 | Repeat Data                           | Num Reads | Compr. Size | Notes                                                    |
| ----------------------------- | ------------------------------------- | --------- | ----------- | -------------------------------------------------------- |
| [small.cfa](data/small.cfa)   | [small.repeats](data/small.repeats)   | 101617    | 21MB        | Small subset of Anopheles gambiae.                       |
| [medium.cfa](data/medium.cfa) | [medium.repeats](data/medium.repeats) | 2586385   | 642MB       | Full set of reads from the Anopheles gambiae Mopti form. |
| [large.cfa](data/large.cfa)   | [large.repeats](data/large.repeats)   | 7915277   | 1.7GB       | Simulated reads from the Sorghum bicolor genome.         |
| [human.cfa](data/human.cfa)   | [human.repeats](data/human.repeats)   | 31257852  | 7.1GB       | Ventner Homo sapiens genome.                             |
