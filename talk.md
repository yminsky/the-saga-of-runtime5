---
title: The Saga of Multicore OCaml
author: Yaron Minsky
theme:
  name: tokyonight-storm
options:
  implicit_slide_ends: true
  incremental_lists: true
  auto_render_languages:
    - mermaid
---

Goals
-----

- Build a modern, high-performance multicore GC for OCaml
- In a way that's easy to adopt! So...
    - Single, easy-to-maintain runtime
    - Don't break sequential performance
    - Maintain low pause times
    - Good parallel speedups
    - Don't break the FFI

<span style="color:green">**Retrofitting Parallelism onto OCaml**</span>, ICFP 2020

<!-- speaker_note: The results are pretty good! -->

- Performance loss of ~3% for sequential programs
- Pause times very similar
- Memory sizes similar-or-better
- Good speedups

It did take a while, though...
-------

- 2013: OCaml Multicore project born
- 2015: "Effect Handlers for OCaml" presented at OCaml Workshop
- 2019: Sandmark benchmark suite created
- 2020: "Retrofitting Parallelism onto OCaml" published
- 2020: Core team commits to upstreaming multicore
- 2021: "Retrofitting Effect Handlers to OCaml" published
- 2022: OCaml 5.0 released with Multicore GC!

9 years! But at least it's done.

Or is it?
----------

- 2023-09: OCaml 5.1 released w/prefetching restored
- 2023-11: OCaml 5.1 merged to JS branch, w/both runtimes
- 2023-12: JS benchmarks find serious performance regressions
- 2024-05: OCaml 5.2 released w/compaction restored
- 2025-01: OCaml 5.3 released w/statmemprof restored
- 2025-05(?): Runtime5 made GA at Jane Street

Another 2.5 years! What happened?

<!-- pause -->

And in particular, what about
<span style="color:green">**the 1.5 years from 2023-12 to 2025-05?**</span>

What is OCaml's GC like?
------------------

<!-- column_layout: [1, 1] -->

<!-- pause -->
<!-- column: 0 -->
# Runtime 4

- Sequential
- Incremental
- Generational
- Snapshot-at-the-beginning
- With a write-barrier
- Closed-loop pacing via a steady-state analysis
- Tuned by space-overhead
- Supporting external memory

<!-- column: 1 -->
# Runtime 5

- ~~Sequential~~ Parallel
- Minor heap
  - One minor heap per domain
  - stop-the-world collection
- Major heap
  - Shared heap
  - Merged mark/sweep design
  - Stop-the-world sync at cycle end
- Safe-points

What problems did we encounter?
-------------------

- Missing features (prefetching, statmemprof, compaction, ...)
- 10-20% regressions on GC-intense programs
- 10% regressions on zero-allocation applications

# What were the causes?

- Transparent huge-pages weren't working
- Context switching in systhreads were slow
- GC pacing was off
  - Due to changes to mark/sweep design
  - and bad heuristics for external memory

Transparent Huge Pages
----------------------

<!-- incremental_lists: false -->
<!-- pause -->

Background

- Traditional pages are 4kb, "Huge" pages are 2Mb (or 1GB)
- Huge savings in TLB pressure
- **Transparent** huge pages is when the OS does it for you,
  implicitly

<!-- pause -->
What happened?

- Worked in 4.14, failed under 5.0
- Serious effect, 3x slowdown in pathological benchmark

What happened to our hugepages?
---------------------------

<!-- column_layout: [1, 1] -->
<!-- pause -->

<!-- column: 0 -->

# Runtime 4

- Grow in big chunks
- Compaction into one big space
- No clever virtual-memory games

<!-- column: 1 -->

# Runtime 5

- Grows in small increments
- Compaction into 32k chunks
- Guard pages to break up the minor heap

<!-- reset_layout -->

# Solution

- Grow heap in big chunks instead
- Compact into one big region
- Carefully align minor heaps

GC Pacing Problems
------------------

- Lots of programs consuming more memory (20%)
- Programs using lots of external memory seeing large slowdowns

How does pacing work?
---------------------

<!-- column_layout: [1, 1] -->
<!-- pause -->

<!-- column: 0 -->

# Runtime 4

- Closed loop control function




GC Pacing Results
-----------------

<!-- pause -->
![](./gc-pacing-graph.png)



Performance debugging is hard
-------------

Project management is hard
-------------


Deployment is hard
-------------

Backwards compatibility is hard
-------------------------------

<!-- pause -->

Every change breaks someone's workflow.

![](./workflow.png)
