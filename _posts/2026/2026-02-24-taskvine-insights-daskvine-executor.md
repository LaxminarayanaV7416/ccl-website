---
layout: post
title: "TaskVine Insights: DaskVine Executor for Practical Scientific Graphs"
date: 2026-02-24T12:00:00-05:00
author: Cooperative Computing Lab
image: /assets/blog/2026/taskvine-insights-daskvine-executor/TaskVine-Insights.png
categories:
  - technical-articles
tags:
  - taskvine
description: In the TaskVine world, workflows can be built task by task or as full graphs. This post focuses on DaskVine and shows how to run Dask graphs on TaskVine with practical guidance on execution modes, data movement, and scheduling options.
toc: false
related_posts: false
---

<div class="row justify-content-sm-center">
<div class="col-sm-12">
{% include figure.liquid path="/assets/blog/2026/taskvine-insights-daskvine-executor/TaskVine-Insights.png" title="" class="img-fluid rounded z-depth-1" zoomable=true %}
</div>
</div>

In the TaskVine world, Python users usually build workflows in two ways.

The first way is the native TaskVine API surface. It includes three task surfaces: `Task`, `PythonTask`, and `FunctionCall`. You create tasks directly, attach inputs and outputs as `File` objects, and control dependencies at fine granularity. This is powerful and explicit. It is also verbose when the workflow is large. The differences among these three surfaces are discussed in detail here: [TaskVine Insights: Picking the Right Task Surface in Python (Task, PythonTask, FunctionCall)](https://ccl.cse.nd.edu/blog/2026/taskvine-insights-picking-the-right-task-surface-in-python/).

The second way is a graph level API surface. You describe a whole computation graph and let the runtime map that graph to tasks, dependencies, and scheduling actions.

DaskVine sits in this second layer. You use Dask to build the graph you already want, then hand that graph to TaskVine for execution. TaskVine remains the underlying scheduler that places work, tracks files, and moves data. DaskVine gives you that backend without forcing you to write every dependency edge manually.

This post focuses on the second way, which is DaskVine. The goal is to help you build a graph with Dask APIs, run it with DaskVine, and tune the parameters that matter for throughput.

## Basic execution pattern

The user side pattern is intentionally small. You construct Dask collections in the usual way, create a DaskVine manager, then run `compute` with `scheduler=m.get`.

```python
import dask
import dask.array as da
import ndcctools.taskvine as vine

x = da.random.random((10000, 10000), chunks=(1000, 1000))
y = (x + 1).sum()

m = vine.DaskVine(port=9123)

with dask.config.set(scheduler=m.get):
    result = y.compute(
        task_mode="function-calls",
        worker_transfers=True,
        task_priority_mode="largest-input-first",
        scheduling_mode="files",
    )

print(result)
```

You still write Dask code. DaskVine controls how that graph runs on TaskVine workers.

## New Dask and legacy Dask paths

TaskVine ships two DaskVine executor implementations:

- `ndcctools.taskvine.dask_executor` handles the modern Dask task specification path.
- `ndcctools.taskvine.compat.dask_executor` preserves legacy behavior for older Dask graph expression styles.

In practice, users should think in terms of compatibility, not internals. Most users should import `vine.DaskVine` from `ndcctools.taskvine` and let the package choose the backend. Current package logic switches at Dask `2024.12.0`: modern versions use the new executor, older versions route to the compat executor. Most users do not need to rewrite graph logic. You keep building the same Dask workflow and pass it to `m.get`.

## Task mode recommendation: prefer FunctionCall

DaskVine supports two execution surfaces:

- `task_mode="tasks"` uses `PythonTask`.
- `task_mode="function-calls"` uses `FunctionCall`.

The detailed tradeoff is covered in the earlier TaskVine Insights post on Python task surfaces: [TaskVine Insights: Picking the Right Task Surface in Python](https://ccl.cse.nd.edu/blog/2026/taskvine-insights-picking-the-right-task-surface-in-python/).

One accuracy note matters here. The API signature still has `task_mode="tasks"` as the code default for compatibility. Our operational recommendation is different. For most DaskVine workloads, treat `function-calls` as your practical default and set it explicitly. It avoids repeated Python cold starts, reuses a long lived worker side library, and usually gives better throughput for the small and medium task granularity that appears in scientific graphs.

## Parameters that matter most in real runs

Many options exist, but a few settings dominate behavior.

### `lib_resources`

`lib_resources` defines resources for the long lived library process that serves `FunctionCall` tasks.

The two most important keys are:

- `cores`: total cores assigned to the library task on one worker.
- `slots`: concurrent function call slots inside that library.

A simple mental model:

- `cores=8`, `slots=2` means up to 2 calls run at once and each can effectively use about 4 cores.
- `cores=8`, `slots=8` means up to 8 calls run at once and each maps to about 1 core.

In current practice, setting `cores == slots` is the safest recommendation because TaskVine function call concurrency is usually tuned as one core per call.

If `memory` and `disk` are omitted in `lib_resources`, the library follows normal TaskVine allocation behavior for unspecified dimensions. In many deployments this effectively gives the library most of the worker budget on those dimensions, especially when few competing tasks share the worker. If you need strict memory and disk guarantees, set them explicitly.

```python
lib_resources = {
    "cores": 8,
    "slots": 8,
}
```

### `worker_transfers`

`worker_transfers=True` means non target intermediate outputs are treated as worker resident temp outputs whenever possible. They stay near the workers instead of returning to the manager after every edge. Final requested targets still come back to the manager. You can also force selected intermediates to return by providing `checkpoint_fn`.

The result is lower manager network pressure and less sequential transfer overhead on large DAGs. This should remain your default unless worker failure rates are high enough that recomputation cost dominates.

### `lib_modules`

`lib_modules` hoists imports into the function call library preamble. That prevents repeating heavy imports in every individual call.

A source level detail matters here. `lib_modules` is forwarded as `hoisting_modules`, and the current generator handles module objects, functions, and classes. Plain strings are not hoisted. Pass real module objects instead of names.

```python
import numpy
import pandas
import scipy

result = graph.compute(
    scheduler=m.get,
    task_mode="function-calls",
    lib_modules=[numpy, pandas, scipy],
)
```

This is especially valuable when import time is noticeable relative to task runtime.

### `extra_files`

Many workflows need side inputs that are not represented as upstream Dask values. `extra_files` is the hook for that case.

The expected shape is a dictionary:

- key: a TaskVine `File` object returned by `m.declare_file`, `m.declare_url`, or other `declare_*` calls
- value: the remote filename string inside the task sandbox

Implementation wise, DaskVine forwards this dictionary into every generated graph task, then calls `add_input(file, remote_name)` for each pair. This happens in both `task_mode="tasks"` and `task_mode="function-calls"`.

```python
weights = m.declare_file("model_weights.bin")
config = m.declare_file("run_config.json")

result = graph.compute(
    scheduler=m.get,
    extra_files={
        weights: "model_weights.bin",
        config: "run_config.json",
    },
    task_mode="function-calls",
)
```

This pattern is common for model parameters, static lookup tables, and domain specific config bundles.

### `task_priority_mode`

TaskVine uses a priority queue. `task_priority_mode` decides how task priority is computed before dispatch.

Common choices:

- `largest-input-first` (default): prioritize tasks with larger ready inputs, often better for storage pressure and pruning.
- `FIFO`: older submitted tasks first.
- `LIFO`: newer submitted tasks first.
- `depth-first`: go deeper in the graph quickly.
- `breadth-first`: spread progress across branches.
- `random`: randomized ordering.
- `longest-category-first` and `shortest-category-first`: adaptive policies based on observed category runtime.

### `scheduling_mode`

After a task is selected, `scheduling_mode` chooses the worker.

- `files` (default): prefer workers that already hold more required input bytes for that task.
- `time`: prefer workers that have completed tasks faster.
- `rand`: random available worker.
- `worst`: prefer worker with the most currently unused resources.
- `disk`: prefer worker with the most unused disk.

`files` is usually the right default because it improves data locality and reduces peer transfer volume.
These policy names map to manager level scheduling choices in the TaskVine runtime.

## A practical tuned template

The following template is a good starting point for many scientific Dask workloads:

```python
with dask.config.set(scheduler=m.get):
    result = graph.compute(
        task_mode="function-calls",
        worker_transfers=True,
        lib_resources={"cores": 8, "slots": 8},
        lib_modules=[numpy, pandas],
        extra_files={static_file: "static_file.dat"},
        task_priority_mode="largest-input-first",
        scheduling_mode="files",
        retries=5,
    )
```

From there, tune one parameter at a time and inspect throughput and failure behavior.

## Where to look for the full option set

DaskVine exposes many additional options such as resource policy, submission backpressure, wrappers, pruning behavior, reconstruction controls, and progress display knobs. The TaskVine manual documents these options and their semantics in detail:

[https://cctools.readthedocs.io/en/latest/taskvine/](https://cctools.readthedocs.io/en/latest/taskvine/)

## What comes next: DAGVine

DaskVine gives a practical path to run Dask graphs on TaskVine today. We are also developing DAGVine as a faster graph execution path. DAGVine targets both Dask built graphs and DAGVine native graphs, with a strong focus on reducing serialization overhead and improving overhead limited throughput.

If your workflows are dominated by orchestration cost rather than kernel compute time, this direction is especially relevant.
