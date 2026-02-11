---
layout: post
title: "TaskVine Insights: Picking the Right Task Surface in Python (Task, PythonTask, FunctionCall)"
date: 2026-02-10T12:00:00-05:00
author: Cooperative Computing Lab
image: /assets/blog/2026/taskvine-insights-picking-the-right-task-surface-in-python/TaskVine-Insights.png
categories:
  - technical-articles
tags:
  - taskvine
  - python
  - api
description: In the TaskVine API, Task, PythonTask, and FunctionCall are three ways to describe work. This post explains how each one expresses dependencies with File objects, and why libraries help avoid Python cold starts and reuse imports and global state.
toc: false
related_posts: false
---

<div class="row justify-content-sm-center">
<div class="col-sm-12">
{% include figure.liquid path="/assets/blog/2026/taskvine-insights-picking-the-right-task-surface-in-python/TaskVine-Insights.png" title="" class="img-fluid rounded z-depth-1" zoomable=true %}
</div>
</div>

Two API layers exist in the TaskVine Python interface. The first layer is direct task creation. This layer includes `Task`, `PythonTask`, and `FunctionCall`. The second layer is graph oriented workflow APIs such as DAGVine and DaskVine. Those graph APIs build on top of the same primitives. Another post will cover DAGVine and DaskVine.

This post stays in the first layer. The goal is simple. It clarifies how each task surface expresses dependencies with `File` objects. It also explains why a long lived library exists, and what it changes for Python workloads.

TaskVine uses the same dependency model for all three. The manager schedules tasks, workers execute tasks, and data dependencies live in explicit `File` objects. The three surfaces differ in how they create those file edges and what they assume about Python execution.

`Task` is the most explicit surface. You provide a command line and you declare inputs and outputs yourself. That makes dependencies visible in your code. It also makes debugging straightforward because the task boundary matches a real process boundary.

```python
import ndcctools.taskvine as vine

m = vine.Manager()

inp = m.declare_file("data/input.txt")
out = m.declare_file("results/output.txt")

t = vine.Task("python3 run_pipeline.py input.txt output.txt")
t.add_input(inp, "input.txt")
t.add_output(out, "output.txt")

m.submit(t)

while not m.empty():
    done = m.wait(5)
    if done and done.successful():
        print("output at:", out.source())
```

`PythonTask` builds on `Task`, but it changes how you describe work. You provide a Python callable and arguments. TaskVine turns that into a command that runs Python on the worker. At submission time the manager materializes the pieces needed to run the function. It creates a small wrapper script, it stores the function body in a manager side buffer file, it serializes arguments to a file in the manager staging directory, and it creates an output file to carry the return value. TaskVine then attaches those `File` objects as inputs and outputs on the underlying task.

That design has two direct consequences for dependency handling. First, the function code and arguments still travel as files and they become part of the task dependency set, even if you never wrote `add_input` for them. Second, the return value is still a `File`, even when you read it back as a Python object through `.output`.

This surface is convenient for glue logic. It is also sensitive to Python cold start overhead. Each `PythonTask` runs in its own Python process on the worker, so interpreter startup and repeated imports can dominate when tasks are small. The worker environment must match your function. Imports must exist on workers, and version skew can show up as ordinary Python exceptions.

```python
import ndcctools.taskvine as vine

m = vine.Manager()

def score(x, y, scale=1.0):
    return scale * (x * x + y * y)

t = vine.PythonTask(score, 3, 4, scale=0.5)
m.submit(t)

while not m.empty():
    done = m.wait(5)
    if done and done.successful():
        print("score =", done.output)
```

`PythonTask` exposes one additional handle that matters for dependencies. The `.output_file` property gives you the `File` object that carries the result. Downstream tasks can depend on that file edge. This is essential when temp output is enabled because `.output` is not available on the manager. The same temp output rule also applies to `FunctionCall`.

`FunctionCall` also builds on `Task`, but it targets a different execution model. It is designed for the case where Python cold start overhead dominates. A workflow can have millions of tiny calls where each call does little work. Starting a fresh Python process per call can cost more than the function itself.

TaskVine solves this with a long lived library. The library runs as a persistent worker side process. You install it through the manager. The manager can generate the library from Python functions and it can hoist imports into the library preamble. The library also has an execution mode. It can run calls directly in process, or it can fork for isolation. A `FunctionCall` then sends only a function name plus arguments to the library. It still serializes the call arguments, but it does not need to ship the function body each time. Imports and global variables can live inside the library and stay warm across calls.

The example below uses the manager helper that creates a library from local Python functions and installs it on workers. The `FunctionCall` tasks then reference the library by name.

```python
import ndcctools.taskvine as vine

m = vine.Manager()

def preprocess(inp, out):
    return (inp, out)

def align(inp, out, threads=1):
    return (inp, out, threads)

lib = m.create_library_from_functions(
    "mylib",
    preprocess,
    align,
    hoisting_modules=["os"],
    exec_mode="fork",
)
m.install_library(lib)

t1 = vine.FunctionCall("mylib", "preprocess", "a.fastq", "a.clean.fastq")
t2 = vine.FunctionCall("mylib", "align", "a.clean.fastq", "a.bam", threads=8)
m.submit(t1)
m.submit(t2)

while not m.empty():
    done = m.wait(5)
    if done and done.successful():
        print(done.output)
```

This surface has one extra dependency hook that matters. A `FunctionCall` requires a library name and the manager checks it at submission time. The call arguments go into an input file. The result goes into an output file. The `.output` property then decodes the result back into a Python value. Temp output works the same way as in `PythonTask`. The downstream dependency should use the `File` edge, not the Python return value.

Mode choice usually follows the boundary you want. `Task` fits external commands and explicit file edges. `PythonTask` is the simplest to get running for Python glue code and structured returns, but `FunctionCall` often wins on runtime performance once Python cold start overhead matters. `FunctionCall` asks you to manage a library, but it keeps Python warm, it centralizes imports and global state, and it avoids paying interpreter startup costs on every call.
