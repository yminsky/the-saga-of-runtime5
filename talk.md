---
title: The saga of runtime5
author: Yaron Minsky
theme:
  name: dark
---

History
-------

<!-- incremental_lists: true -->

- 2013: OCaml Multicore project born
- 2015: "Effect Handlers for OCaml" presented at OCaml Workshop
- 2019: Sandmark benchmark suite created
- 2020: "Retrofitting Parallelism onto OCaml" published
- 2021: "Retrofitting Effect Handlers to OCaml" published
- 2022: OCaml 5 released

9 years! And now it's finally arrived...

<!-- end_slide -->

Or has it?
----------

<!-- incremental_lists: true -->



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
- Paced via space-overhead

<!-- column: 1 -->
# Runtime 5

- Parallel
- Generational
- Incremental
- Paced via space-overhead

<!-- end_slide -->
