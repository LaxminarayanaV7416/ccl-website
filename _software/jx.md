---
layout: software3
title: JX
description: "JX (JSON Expressions) is an expression language for unstructured data. Adding to the standard JSON data description language, it provides operators, variables, functions, list comprehensions, and other conveniences to generate and query complex documents. JX is used throughout the CCTools to describe and query data."
long_description: "JX (JSON Expressions) is an expression language for unstructured data. Adding to the standard JSON data description language, it provides operators, variables, functions, list comprehensions, and other conveniences to generate and query complex documents. JX is used throughout the CCTools to describe and query data."
img: assets/img/software/jx-logo.png
carousel: false
order: 5
category: work
publication_keywords:
  - jx
list_redirect: https://cctools.readthedocs.io/en/latest/jx/
links:
  - name: User Manual
    url: https://cctools.readthedocs.io/en/latest/jx/
---

The JX Expression Language is an extension of the JSON data description language. It combines familiar expression operators, function calls, external data, and ordinary JSON contents to yield a powerful data querying and manipulation language. JX is used throughout the CCTools to manage and query unstructured data.

For example, JX expressions can be used to describe jobs in a workflow:

```
{
    "command" : "collect.exe"
    "inputs" :  [ "input."+i+".txt" ]
    "outputs" : [ "output."+i+".txt" ]
} for i in range(1,100)
```

Or to write LINQ-style queries on remote data:

```
fetch(url).select(type=="wq_master").select(tasks_submitted>100).project([name,tasks_running+tasks_waiting])
```
