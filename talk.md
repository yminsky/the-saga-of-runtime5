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
    - typst
    - latex
---

Let's start with the paper
--------------------------

<span style="color:green">**Retrofitting Parallelism onto OCaml**</span>, ICFP 2020

- A modern, high-performance multi-core GC for OCaml
- Easy to maintain, easy to adopt.
  - One runtime for parallel and sequential
  - Preserving sequential performance, pause times, FFI

Lots of benchmarks and evaluation!

- Runtime loss of ~3% for sequential programs
- Memory used is similar
- Pause times very similar
- Good speedups

It did take a while, though...
-------

<!-- incremental_lists: false -->
<!-- pause -->

- 2013: OCaml Multicore project born
- 2015: <span style="color:green">"Effect Handlers for OCaml"</span>
  presented at OCaml Workshop
- 2019: Sandmark benchmark suite created
- 2020: <span style="color:green">"Retrofitting Parallelism onto OCaml"</span> published
- 2020: Core team commits to upstreaming multicore
- 2021: <span style="color:green">"Retrofitting Effect Handlers to OCaml"</span> published
- 2022: OCaml 5.0 released with multicore GC and effects

<!-- pause -->

- 2023-09: <span style="color:blue">prefetching restored</span> (5.1)
- 2023-11: OCaml 5.1 merged to JS branch, w/both runtimes
- 2023-12: <span style="color: #ff9000">JS benchmarks find serious
  performance regressions</span>
- 2024-05: <span style="color:blue">compaction restored</span> (5.2)
- 2025-01: <span style="color:blue">statmemprof restored</span> (5.3)
- 2025-05: <span style="color: #ff9000">Regressions fixed</span>, multicore is GA at JS


What is OCaml's GC like?
------------------

<!-- column_layout: [1, 1] -->

<!-- pause -->
<!-- column: 0 -->
# Runtime 4

- Sequential
- Generational
- With a write-barrier
- Mark & Sweep
- Incremental
- Snapshot-at-the-beginning
- Mostly open-loop pacing
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

Regressions
-----------

- Some programs running 10-20% slower
- Some programs using 10-20% more memory

# Sources

- Transparent huge-pages not getting allocated
- GC pacing problems
- Slow context switching in systhreads
- Slow stack checks

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

<!-- speaker_note: And why does the old GC (invented before THP)
     outperform the new one? -->

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

How does pacing work?
---------------------

<!-- column_layout: [1, 1] -->
<!-- pause -->

<!-- column: 0 -->

# Runtime 4

- Constant amount of collection per word promoted.
- External memory
  - extra_heap_resources determines when to do an extra cycle
  - Increment by N/kH on every external alloc


<!-- column: 1 -->

# Runtime 5

- Same pacing approach for ordinary allocations
- Fixed a bunch of implementation bugs

GC Pacing Results
-----------------

![](./images/space_overhead_0.png)

GC Pacing Results (rt4)
-----------------

![](./images/space_overhead_1.png)

GC Pacing Results (rt5)
-----------------

![](./images/space_overhead_2.png)

What happened?
--------------

- Ordinary collection is less aggressive
  - Unified mark & sweep => too much floating garbage (~25%)
  - Fix with markdelay patch, breaking them back up
- But excessive collection with bigstrings is better
  - One bugfix made allocation less aggressive
  - (But others made it more aggressive)

GC Pacing Results (rt5)
-----------------

![](./images/space_overhead_2.png)

GC Pacing Results (rt5-markdelay)
-----------------

![](./images/space_overhead_3.png)

Where are we now?
-----------------

- Ordinary pacing is better (though still not quite right)
- Excessive collection is worse

What next?

- Tried to fix some of the design bugs
- e.g., N/kH uses the wrong notion of H
- But...results were hard to tune and control


Open-loop and Closed-loop pacing
--------------------------------

<!-- pause -->
# Open-loop

```mermaid +render
graph LR
    Obs --> Dec
```

Predictable, but has a hard time hitting the target

<!-- pause -->
# Closed-loop

```mermaid +render
graph LR
    Obs --> Dec
    Dec --> Obs
```

Can hit the target precisely, but often oscillates or converges too
slowly

Back to the drawing board!
--------------------------

- Rethinking the steady-state analysis, an open-loop solution was
  found!
- Constant number of words collected per word allocated
- But an extra word of sweeping per on-heap byte

GC Pacing Results (rt5-markdelay)
-----------------

![](./images/space_overhead_3.png)

GC Pacing Results (rt5-open-loop)
-----------------

![](./images/space_overhead_4.png)

Things we learned
-----------------
<!-- incremental_lists: false -->
<!-- pause -->

# Benchmarking is hard

- Original testing leaned too much on small programs
- Different use-cases put different pressures on the design
- <span style="color:blue">**Takeaway**</span>: More of the initial
  evaluation should have been real systems.

<!-- pause -->
# Performance debugging is hard

- Problems cover each other
- Too much time spent implementing full solutions to non-problems
- <span style="color:blue">**Takeaway**</span>: More focused
  benchmarks and proof-of-concept fixes while iterating on the
  solutions

Things we learned
-----------------
<!-- incremental_lists: false -->

# Go back to the drawing board, sometimes

- We knew external memory handling was hacky
- We tried to fix the issues incrementally
- But a first-principles approach turned out better

Things we learned
-----------------
<!-- incremental_lists: false -->

<!-- column_layout: [3, 2] -->

<!-- column: 0 -->
# Backwards compatibility is hard

Every change breaks someone's workflow.

<!-- column: 1 -->
![](./images/workflow.png)

What's next?
------------

<!-- pause -->

<span style="color:green">**Data Race Freedom à la Mode**</span>, POPL
2025

- Propagating type information through our libraries
  - And fixing data-races!
- High-performance data-structures
- User-level scheduling
- Profiling and analysis tools
- New abstractions for efficiently combining parallelism and
  concurrency
- Teaching people how to use it!

Stay tuned!
