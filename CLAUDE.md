# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository contains materials for "The Saga of Multicore OCaml" presentation by Yaron Minsky. It documents the transition from OCaml Runtime 4 to Runtime 5 (multicore support) and the performance challenges encountered during this migration at Jane Street.

## Architecture and Structure

### Core Content
- `talk.md` - Main presentation slides in markdown format using a slide deck framework (tokyonight-storm theme)
- `notes.org` - Detailed notes and outline covering the technical challenges, timeline, and lessons learned
- Performance analysis images (`space_overhead_*.png`, `gc-pacing-graph.png`) - Visualizations showing GC performance comparisons
- `workflow.png` - XKCD comic about backwards compatibility challenges

### Key Technical Topics Covered
- OCaml Runtime 4 vs Runtime 5 architectural differences
- Garbage collection pacing algorithms (open-loop vs closed-loop)
- Transparent Huge Pages (THP) allocation issues
- Memory management and performance regression analysis
- Multicore GC design trade-offs and synchronization points

## File Structure Context

This is a presentation repository focused on documenting the technical journey of migrating from single-threaded to multicore OCaml runtime. The materials serve as both a talk presentation and technical documentation of the performance engineering challenges encountered during this major language runtime transition.

The repository represents a case study in large-scale systems migration, highlighting the complexities of garbage collector design, performance debugging methodologies, and the challenges of maintaining backwards compatibility in production systems.