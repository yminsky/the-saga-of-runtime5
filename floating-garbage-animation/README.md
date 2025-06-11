# Floating Garbage Animation

This animation visualizes the difference in floating garbage lifetime
between OCaml's Runtime 4 (traditional mark-and-sweep) and Runtime 5
(merged mark/sweep phases).

## Key Concepts

- **Snapshot-at-the-beginning**: The GC takes a snapshot of the heap
  at the start of each mark phase. Objects allocated during marking
  won't be seen until the next mark phase begins.
- **Floating garbage**: Objects that become unreachable but haven't
  been collected yet.
- **Runtime 4**: Separate sweep [S] and mark [M] phases with
  synchronization between each.
- **Runtime 5**: Merged sweep/mark [S/M] phases to reduce
  synchronization points.

## Visual Design

- Timeline flows left to right
- Each phase is represented as a rectangular block
- Runtime 4: Alternating [S] and [M] blocks of equal width
- Runtime 5: [S/M] blocks that are twice as wide (representing combined phase duration)
- Colors:
  - Sweep phases: Blue (#4682B4)
  - Mark phases: Green (#228B22)
  - Merged S/M phases: Purple (#6B46C1)
  - Allocation markers: Green triangles pointing up
  - Collection markers: Red triangles pointing up
  - Horizontal bars connect allocations to collections with cycle count labels

## Frame-by-Frame Animation

### Frame 1: Initial Runtime 4 Timeline
- Show timeline with phases: [S][M][S][M][S][M]
- Simple label: "Runtime 4"
- No other chrome or titles

### Frame 2: Allocation in Sweep Phase
- Add green triangle allocation marker below the first [S] block

### Frame 3: Collection Point for Sweep Allocation
- Keep allocation marker from Frame 2
- Add horizontal bar from allocation to collection point with "1 cycle" label
- Add red triangle collection marker below the [S] block after the next [M]
- Shows 1 cycle lifetime for garbage allocated during sweep

### Frame 4: Add Mark Allocation
- Keep all markers from the sweep example
- Add green triangle allocation marker below the first [M] block
- Positioned lower than sweep example for visual separation

### Frame 5: Collection Point for Mark Allocation
- Keep all previous markers
- Add horizontal bar from mark allocation to collection point with "1.5 cycles" label
- Add red triangle collection marker below the [S] block in position 4
- Shows 1.5 cycle lifetime for garbage allocated during mark

### Frame 6: Add Runtime 5 Timeline
- Keep Runtime 4 visualization above with both allocation/collection examples
- Add Runtime 5 timeline below: [S/M][S/M][S/M]
- Simple label: "Runtime 5"
- [S/M] blocks are twice as wide and aligned with [S][M] pairs above

### Frame 7: Runtime 5 First Allocation
- Add green triangle allocation marker in first half of first [S/M] block
- Aligned horizontally with sweep allocation position in Runtime 4

### Frame 8: Runtime 5 Second Allocation
- Keep first allocation marker
- Add second green triangle allocation marker in second half of first [S/M] block
- Aligned horizontally with mark allocation position in Runtime 4

### Frame 9: Runtime 5 First Collection
- Keep both allocation markers
- Add horizontal bar from first allocation to collection point with "2 cycles" label
- Add red triangle collection marker in first half of third [S/M] block

### Frame 10: Runtime 5 Second Allocation (maintained)
- Keep all previous markers including the second allocation
- This frame ensures the second allocation remains visible

### Frame 11: Runtime 5 Both Collections
- Keep all previous markers
- Add horizontal bar from second allocation to collection point with "2 cycles" label
- Add red triangle collection marker in first half of third [S/M] block
- Both allocations collected at same horizontal position

### Frame 12: Final Comparison
- Show both timelines with all allocation and collection points
- Runtime 4: [S] allocation → 1 cycle, [M] allocation → 1.5 cycles
- Runtime 5: Both allocations → 2 cycles to same collection point

## Implementation Notes

- Use HTML5 with CSS animations
- Navigation: Keyboard only
  - Arrow keys (left/right) to move between frames
  - Space bar also advances to next frame
- No visible buttons or UI chrome
- Each frame transition should be clear and smooth
- No automatic progression

## Technical Details

The key insight is that Runtime 5's design trades off:
- **Benefit**: One less synchronization point per cycle (better parallelism)
- **Cost**: Floating garbage lives longer on average

In Runtime 4:
- Garbage allocated during [S]: Lives for 1 cycle
- Garbage allocated during [M]: Lives for 1.5 cycles
- Average: 1.25 cycles

In Runtime 5:
- Garbage allocated anywhere in [S/M]: Lives for 2 cycles
- This represents a 60% increase in floating garbage lifetime on average

This visualization helps explain why Runtime 5 showed increased memory
usage despite having similar GC algorithms.
