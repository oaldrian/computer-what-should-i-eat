# computer-what-should-i-eat

A webpage that tells you what to cook, based on a base set of entries, and self entered ones.

- Fully vibe coded
- Intentionally no backend
- No localization, only German frontend.

## Generated (English)

This generated section contains an English overview and usage notes for the project.

### Overview

A small single-file web app that helps you decide what to eat. It ships with a built-in dataset and lets you add local items and overrides which are persisted to the browser's `localStorage`.

Key points

- Client-only: no backend required — open `index.html` in a browser or serve the folder with a static file server.
- Data: builtin items are loaded from `data.json`. Local additions and overrides are stored under `picker_items_local` and `picker_items_overrides` in `localStorage`.

Usage

1. Serve the folder (recommended) and open the app in a browser:

```bash
python -m http.server 8000
# then open http://localhost:8000/index.html
```

2. Use the left column to browse items, filter by attributes or rating, and search (supports attribute:value queries and `*` wildcards).
3. Add new items with the Add button (or press `a`), edit built-in items (creates overrides), and export/import your local data.

Keyboard shortcuts

- `/` : Focus the search field
- `r` : Pick a random item from the current filters
- `a` : Open the Add Item modal

Accessibility and behavior

- Modals use `role="dialog"` and trap focus while open; focus is restored on close.
- Non-blocking toasts are announced via a hidden live region and appear in the top-right corner.
- The app strives to be keyboard-friendly (accordion behavior, Enter/Space to toggle cards).

Import/Export notes

- Export produces a JSON file containing your local items and overrides plus metadata (timestamp and counts).
- Importing a previously exported JSON shows a preview and will detect ID conflicts. You can choose to merge (skip duplicates), overwrite overrides, or automatically rename incoming items to avoid collisions.

Developer notes

- Quick checks in browser console:
  - Run the lightweight test runner: `window.__picker.runTests()`
  - Inspect `localStorage` keys: `picker_items_local`, `picker_items_overrides`

License

- This project is provided as-is under the repository license.

