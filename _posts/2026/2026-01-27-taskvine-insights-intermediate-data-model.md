---
layout: post
title: TaskVine Insights - Intermediate Data Model
date: 2026-01-27T12:00:00-05:00
author: Cooperative Computing Lab
image: /assets/blog/2026/taskvine-insights-intermediate-data-model/TaskVine-Insights.png
categories:
  - technical-articles
tags:
  - taskvine
description: Large DAGs often bottleneck on intermediate data. Here's how TaskVine's temp files keep intermediates on workers and cut manager-side transfers.
toc: false
related_posts: false
---

<div class="row justify-content-sm-center">
<div class="col-sm-12">
{% include figure.liquid path="/assets/blog/2026/taskvine-insights-intermediate-data-model/TaskVine-Insights.png" title="" class="img-fluid rounded z-depth-1" zoomable=true %}
</div>
</div>

## Why intermediate data becomes the bottleneck

If you've run large DAG workflows on a cluster, you've probably seen this pattern: CPU looks fine, workers are alive, but the makespan still crawls. A common reason is **intermediate data**—the "in between" outputs that feed the next stages of the graph.

In a small workflow, it's totally reasonable to ship every task's output back to the manager (or to some central location), then redistribute it later. In a big DAG, that approach turns the manager into a traffic jam:

- every edge in the DAG starts to look like "worker -> manager -> worker"
- the manager's network and disk become shared bottlenecks
- recovery/retries multiply the same transfers

TaskVine's intermediate data model exists mostly to avoid that outcome.

## The default model: outputs come back to the manager

At a high level, TaskVine's manager schedules tasks, and workers execute tasks. Files are tracked as TaskVine `File` objects in the manager-side API, and tasks declare which files they consume/produce.

In the default mode, when a task produces output files, those outputs are treated as something the manager can retrieve and store locally. That's the safe, simple behavior: once the manager has the file, it can hand it to any future task without caring which worker originally produced it.

The downside is obvious in large DAGs: if many tasks are producing large intermediates, you end up "pinballing" data through the manager.

## The intermediate model: declare outputs as temp, keep them on workers

TaskVine has a second, more DAG-friendly model for intermediate results: declare the intermediate as a **temp file**.

The key idea is:

1. The producing task writes the output as usual on its worker.
2. Instead of immediately bringing that file back to the manager, the file is kept on the **worker's local disk / cache**.
3. The worker notifies the manager that the file exists (think: "this cached name is now ready on worker X").
4. When some downstream task needs that file, TaskVine can arrange a **worker-to-worker transfer** to wherever the consumer runs.

So the DAG edge becomes "worker → worker" most of the time, and the manager stays mostly control-plane.

This is not magic: you're still moving bytes. The win is that you avoid forcing _all_ intermediate bytes to traverse one central node.

## Using temp outputs in the Python API

There are two common ways you'll use this from Python:

### 1) Create a temp file explicitly with `declare_temp()`

This is the most direct style: you create a temp `File`, attach it as an output of one task, then attach it as an input of another task.

```python
import ndcctools.taskvine as vine

m = vine.Manager()

# A temp file represents an intermediate result.
F = m.declare_temp()

# Producer writes F on its worker.
tA = vine.Task("python3 produce.py out.dat")
tA.add_output(F, "out.dat")
m.submit(tA)

# Consumer reads F (TaskVine will fetch it from a worker that has it).
tB = vine.Task("python3 consume.py in.dat")
tB.add_input(F, "in.dat")
m.submit(tB)

while not m.empty():
    t = m.wait(5)
    if t:
        pass
```

This is the mental model you want for DAGs: temp files are named intermediates that can stay out on the workers.

### 2) For PythonTask and FunctionCall tasks: `enable_temp_output()`

If you're using `PythonTask` or `FunctionCall` and you want the result file to stay at workers, enable temp output on that task. When temp output is enabled, the task's Python-level output is not available locally (because the output wasn't brought back); instead, you pass around the `File` object and let downstream tasks load it.

```python
import cloudpickle
import ndcctools.taskvine as vine

m = vine.Manager()

def make_big():
    # pretend this is a big intermediate
    return {"x": "..." * 10_000_000}

def use_big(filename):
    with open(filename, "rb") as f:
        data = cloudpickle.load(f)
    return len(data["x"])

tA = vine.PythonTask(make_big)
tA.enable_temp_output()          # keep output on worker
m.submit(tA)

# IMPORTANT: downstream tasks consume the output via the File object.
tB = vine.PythonTask(use_big, "in.p")
tB.add_input(tA.output_file, "in.p")
m.submit(tB)

while not m.empty():
    t = m.wait(5)
    if t and t.successful():
        # tB is not temp-output, so we can read it normally
        pass
```

## Using temp outputs in DaskVine graph executor

DaskVine already exposes this idea with a simple switch: `worker_transfers`.

When `worker_transfers=True` (the default), DaskVine tries to treat intermediate results as worker-resident and only brings results back to the manager when needed (targets, checkpoints, etc.). In the DaskVine implementation, tasks that are considered "lazy" for transfer enable temp output so that their results remain on workers.

In practice, you use it like this:

```python
from ndcctools.taskvine.compat.dask_executor import DaskVine
import dask

m = DaskVine(name="my-dask-run")

# Default is worker_transfers=True: intermediates stay on workers.
with dask.config.set(scheduler=m.get):
    result = some_dask_collection.compute()
```

If you want to force intermediates to be brought back to manager (more conservative, often slower at scale), you can set:

```python
with dask.config.set(scheduler=m.get):
    result = some_dask_collection.compute(scheduler=m.get, worker_transfers=False)
```

## Practical advice

Temp intermediates help most when your DAG has big intermediate edges and lots of reuse. They help less (or can hurt) when intermediates are tiny, when the cluster network is already saturated, or when worker local disks are very constrained.

There's an important implication to keep in mind: keeping data on workers trades manager-side throughput for durability. If you're running on a cluster where worker failure, preemption, or churn is common, then leaving key intermediates only on worker-local disks is risky—losing a worker can mean losing the only copy and forcing recomputation. In those environments, you may prefer to bring important data back to the manager (or checkpoint it to a shared filesystem) so the workflow can survive worker loss without paying the full recompute cost.

This is especially true for expensive intermediates: if a task ran for hours to produce a file, you often want that output to be persisted rather than treated as a temporary cache entry. On the other hand, for large numbers of fine-grained tasks (small outputs, lots of edges) or on clusters with good worker reliability, temp intermediates are usually the right default because they reduce manager-worker traffic and keep the system moving.
