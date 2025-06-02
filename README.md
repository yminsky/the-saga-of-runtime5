# The Saga of Multicore OCaml

Presentation materials documenting Jane Street's experience migrating
from OCaml Runtime 4 to Runtime 5 (multicore support).

## Contents

- `talk.md` - Presentation slides (reveal.js format)
- `notes.org` - Detailed technical notes
- `gc-talk-graphs/` - Performance analysis data and visualization script
- `*.png` - Generated performance comparison charts
- `Makefile` - Build configuration for generating HTML slides

## Usage

Build the presentation:
```bash
make slides
```

Open `talk.html` in a web browser to view the reveal.js presentation.

The presentation covers the technical challenges, performance
regressions, and solutions discovered during the runtime migration
process.
