# Heap Marking Animation

This directory contains an OCaml program that generates an interactive HTML animation demonstrating the garbage collection marking and sweeping process.

## Files

- `generate_heap_animation.ml` - OCaml program that generates the HTML animation
- `heap_animation.html` - Generated interactive animation (created by running make)
- `heap_marking.png` - Static diagram showing the heap marking state
- `heap_marking.svg` - SVG version of the static diagram
- `dune` - Dune build configuration
- `dune-project` - Dune project file
- `Makefile` - Build automation

## Building

```bash
# Generate the animation
make

# Clean generated files and build artifacts
make clean
```

## Requirements

- OCaml with Base and Stdio libraries
- Dune build system
- ppx_jane preprocessor

## Animation Features

The interactive animation demonstrates:
- **Marking phase**: Starting from roots, traversing and marking reachable objects
- **Sweeping phase**: Scanning through memory, removing unmarked objects and resetting marked objects

### Visual Design

- **Root objects**: Blue - Starting points in the stack
- **Marked objects**: Green - Reachable objects that will be kept
- **Unmarked objects**: Red - Unreachable garbage to be collected
- **Active connections**: Burgundy arrows show the current traversal path

### Controls

- **Arrow keys** (← →): Navigate between frames
- **Space**: Advance to next frame
- **C**: Toggle auto-advance mode (100ms per frame)

## Implementation

The animation is implemented in OCaml using Jane Street style:
- Immutable data structures
- Declarative heap configuration
- Frame-based animation generation
- Clean separation between data generation and HTML rendering