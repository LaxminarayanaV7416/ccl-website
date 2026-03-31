---
layout: post
title: "TaskVine Insights: How to Propose a Pull Request to the CCL Team"
date: 2026-03-31T12:00:00-05:00
author: Cooperative Computing Lab
image: /assets/blog/2026/taskvine-insights-how-to-propose-a-pull-request-to-the-ccl-team/TaskVine-Insights.png
categories:
  - technical-articles
tags:
  - taskvine
  - cctools
  - contribution
  - github
description: Contributions help TaskVine and CCTools move forward. This post welcomes discussion, pull requests, and patches, then describes the workflow from issue to merge and how to build, test, and submit against the official repository.
toc: false
related_posts: false
---

<div class="row justify-content-sm-center">
<div class="col-sm-12">
{% include figure.liquid path="/assets/blog/2026/taskvine-insights-how-to-propose-a-pull-request-to-the-ccl-team/TaskVine-Insights.png" title="" class="img-fluid rounded z-depth-1" zoomable=true %}
</div>
</div>

TaskVine and CCTools improve when people share ideas, report bugs, and ship code. The Cooperative Computing Lab welcomes your participation. We want **GitHub discussions**, **issues**, **pull requests**, and **patches** to the codebase. You do not need permission to start a conversation or to propose a change.

If you run TaskVine workflows, extend the runtime, or simply have a fix in mind for the [CCTools repository](https://github.com/cooperative-computing-lab/cctools), the sections below walk through a path we like: talk in public first, then build and test, then open a pull request that ties back to that conversation. The goal is to keep review fair and merges safe, not to add hoops for their own sake.

## Start with an issue or a discussion, not with a branch

Before you fork the repo or name a branch, open a topic on the upstream project so others can see the problem and the proposed direction. For a concrete bug, the [Issues](https://github.com/cooperative-computing-lab/cctools/issues) page is the usual place. Broader design questions sometimes fit better in [Discussions](https://github.com/cooperative-computing-lab/cctools/discussions). Either way, the goal is the same: you explain what fails or what you want, you share enough context that a reviewer can reproduce or reason about it, and you agree on what should change before you invest in a large patch.

Logs and traces often matter. If a run log is large, upload it to a shared location such as Google Drive and link it in the issue or discussion so maintainers can inspect the same evidence you see. A pull request should **link to that issue** (for example `Fixes #1234` or `Refs #1234` in the description). We use the issue to confirm scope before the PR lands, and we close the issue when the change is merged and the problem is addressed.

If you skip this step, you risk wasted effort. You might implement something the team would solve differently, or duplicate work someone else already started. The standardized flow is discuss first, then implement, then open the PR.

## Fork the official repository

The canonical upstream remote is:

`https://github.com/cooperative-computing-lab/cctools.git`

Sign in to GitHub, open that repository, and use **Fork** to create a copy under your account. All of your `git push` work for a contribution should go to that fork. Pull requests run from your fork into `cooperative-computing-lab/cctools`, typically targeting the `master` branch unless maintainers ask otherwise.

## Clone your fork and enter the tree

From your machine, clone **your** fork with SSH so you can push without typing a password each time. The clone URL looks like:

`git@github.com:<your-username>/cctools.git`

Example session:

```sh
git clone git@github.com:<your-username>/cctools.git cctools-test
cd cctools-test
```

You can name the working directory anything you like. The important part is that the `origin` remote points at your fork.

## Build with Conda from a clean environment

The README and manual describe building CCTools from source. For day-to-day development, we isolate compilers and Python with Conda so `./configure` can discover everything from a single prefix. A typical Linux setup looks like this:

```sh
# Create an isolated development environment with a pinned Python version.
conda create -y -n cctools-dev -c conda-forge --strict-channel-priority python=3.11.12 conda-pack
# Activate the environment so the compiler, Python packages, and install prefix all point to the same place.
conda activate cctools-dev
# Install the build toolchain and development utilities used by CCTools.
conda install -y -c conda-forge --strict-channel-priority gcc_linux-64 gxx_linux-64 gdb m4 perl swig make zlib libopenssl-static openssl conda-pack packaging cloudpickle flake8 clang-format threadpoolctl
# Go to the directory you just cloned.
cd cctools-test
# Discover dependencies from the active Conda environment and install back into that same environment.
./configure --with-base-dir "${CONDA_PREFIX}" --prefix "${CONDA_PREFIX}"
# Remove stale build artifacts before compiling.
make clean
# Build the repository in parallel, then install it.
make -j8
make install
# Sanity check that the install path is active and the worker binary is usable.
vine_worker --version
```

If `vine_worker --version` prints a sensible version string, your toolchain and install prefix are aligned. The [TaskVine User's Manual](https://cctools.readthedocs.io/en/latest/taskvine/) and the top-level [repository README](https://github.com/cooperative-computing-lab/cctools/blob/master/README.md) remain the references for environment quirks on other platforms.

## Create a branch for one coherent change

Work on a dedicated branch, not on `master` directly. Branch names should hint at the change. Suppose your patch adjusts the default manager keepalive timeout. In `taskvine/src/manager/vine_manager.c`, the default keepalive timeout is defined near the other manager defaults:

```c
/* Default value for keepalive timeout in seconds. */
#define VINE_DEFAULT_KEEPALIVE_TIMEOUT 900
```

A branch name such as `change-default-keepalive-timeout` makes the intent obvious:

```sh
git switch -c change-default-keepalive-timeout
```

Then edit the file and set the value you and the maintainers agreed on in the issue, for example `3600` instead of `900`. Keep the change minimal. One pull request should represent one logical fix or feature unless reviewers explicitly bundle work.

## Format and lint before you push

The top-level `Makefile` exposes `format` and `lint` targets. **Run `make format` first**, then `make lint`. Formatting applies `clang-format` (and package-specific rules) so C and related sources follow project style. Linting runs static checks such as `flake8` where configured. If you lint before format, you may still need a second lint pass after the formatter rewrites lines.

From the repository root after `configure`:

```sh
make format
make lint
```

Fix anything these targets report. For larger changes, also read `STYLE.md` in the repository root if your edit touches areas with extra conventions.

## Run the test suite

Your toy one line constant change might not add new failures, but the standard we expect for any merge candidate is a clean **`make test`** from the top level. That driver invokes `run_all_tests.sh`, which exercises packages including TaskVine tests under `taskvine/test/`. If you change scheduling, bindings, or worker behavior, assume you must run the full suite and address regressions before opening or updating the PR.

```sh
make test
```

## Commit, push to your fork, and open the pull request

Stage and commit your work, then push the branch to **your** GitHub fork:

```sh
git add -u
git commit -m "Describe the change in one line"
git push -u origin change-default-keepalive-timeout
```

On GitHub, open your fork, switch to the branch you pushed, and use **Compare and pull request** (or the equivalent control) to open a PR against `cooperative-computing-lab/cctools`. Fill in a clear title and a description that states motivation, what you changed, and how you tested it. Link the issue you opened earlier. That link is what ties review conversation to the original problem statement.

## CI, review, and merge

GitHub Actions and related checks run on the pull request. Expect on the order of **ten minutes** for a full run, depending on queue load. A green CI run is not optional for merge. It signals that the same tests you ran locally also pass in the project automation.

At least **one approval** from a maintainer is required before merge. For visibility, you may tag maintainers such as **dthain** or **btovar** when you need a decision or a review slot, especially for behavior that affects scheduling or protocol-level defaults. Reviewers may request changes. Address feedback with additional commits on the same branch and push again. The PR updates automatically.

When the maintainers merge your branch into `master`, return to the **issue** you linked. Close it if the fix or feature is complete, or note follow-up work if something remains out of scope.
