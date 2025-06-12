# Heap Marking Diagram

This directory contains a Python script to generate a clean heap marking visualization diagram showing:
- Stack with root pointers
- Heap with objects in different marking states
- Arrows showing references between objects
- A key explaining the visual patterns

## Files

- `generate_heap_diagram.py` - Main script that generates the SVG diagram
- `heap_marking.svg` - Generated SVG output
- `heap_marking.png` - PNG version for presentations

## Usage

```bash
# Generate both SVG and PNG
make

# Clean generated files
make clean
```

## Visual Design

The diagram illustrates the heap state at the end of the marking phase:
- **Root objects**: Blue - Starting points for reachability analysis
- **Marked objects**: Green - Reachable from roots (will be kept)
- **Unmarked objects**: Red - Unreachable garbage (will be collected)

The diagram shows:
- Stack with root pointers on the left
- Heap divided into reachable and unreachable sections
- Straight arrows showing object references
- A visually distinct legend explaining the color scheme