---
title: The Saga of Multicore OCaml
author: Yaron Minsky
theme:
  name: dark
---

Goals
-----

<!-- incremental_lists: true -->

- Build a modern, high-performance multicore GC for OCaml
- In a way that's easy to adopt! So...
    - Single, easy-to-maintain runtime
    - Don't break sequential performance
    - Maintain low pause times
    - Good parallel speedups

<span style="color:green">**Retrofitting Parallelism onto OCaml**</span>, ICFP 2020


<!-- end_slide -->

History
-------

<!-- incremental_lists: true -->

- 2013: OCaml Multicore project born
- 2015: "Effect Handlers for OCaml" presented at OCaml Workshop
- 2019: Sandmark benchmark suite created
- 2020: "Retrofitting Parallelism onto OCaml" published
- 2020: Core team commits to upstreaming multicore
- 2021: "Retrofitting Effect Handlers to OCaml" published
- 2022: OCaml 5.0 released with Multicore GC!

9 years! But at least it's done.

<!-- end_slide -->

Or is it?
----------
<!-- incremental_lists: true -->

- 2023-09: _OCaml 5.1_ released w/prefetching restored
- 2023-11: **OCaml 5.1** merged to JS branch, w/both runtimes
- 2023-12: JS benchmarks find serious performance regressions
- 2024-05: OCaml 5.2 released w/compaction restored
- 2025-01: OCaml 5.3 released w/statmemprof restored
- 2025-05(?): Runtime5 made GA at Jane Street

Another 2.5 years! What happened?

<!-- pause -->

And in particular, what about
<span style="color:green">**the 1.5 years from 2023-12 to 2025-05?**</span>

<!-- end_slide -->

What is OCaml's GC like?
------------------

<!-- column_layout: [1, 1] -->
<!-- incremental_lists: true -->

<!-- pause -->
<!-- column: 0 -->
# Runtime 4

- Sequential
- Generational
- Incremental
- Closed-loop pacing via a steady-state analysis
- Tuned by space-overhead
- Supporting external memory

<!-- column: 1 -->
# Runtime 5

- ~~Sequential~~ Parallel
- Shared major heap
- One minor heap per domain
- Merged mark/sweep design
- With one (brief) stop-the-world sync per mark/sweep cycle

<!-- end_slide -->

What were the problems
---------------------

<!-- incremental_lists: true -->

- Missing features (prefetching, statmemprof, compaction)
- Large time-performance regressions: 10-20% on GC-intence programs
  - And not just us! Other major users had hit similar slowdowns
- Material slowdowns (10%) on GC-free applications (!?!)

# What were the problems?

- Stack checks were expensive
- Collection rate was too low in general
- Transparent huge-pages weren't working
- Applications with heavy use of external memory had big (20%-100%)
  size regressions
- Context switching in systhreads were slow

<!-- end_slide -->

Performance debugging is hard
-------------

<!-- end_slide -->

Project management is hard
-------------

<!-- end_slide -->

Deployment is hard
-------------

<!-- end_slide -->

Backwards compatibility is hard
-------------------------------

<!-- pause -->

Every change breaks someone's workflow.

![](./workflow.png)

<!-- end_slide -->

Backwards compatibility is hard
-------------------------------

<!-- pause -->

Every change breaks someone's workflow.

![](./workflow.png)

<!-- end_slide -->
