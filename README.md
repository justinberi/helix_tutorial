# Helix Tutorial

An interactive, agent-led training course for the [Helix](https://helix-editor.com/)
editor. The agent runs in your terminal, reads `curriculum.md` for lesson
content and `lesson_memory.md` for your progress, and teaches one lesson at
a time in the personality you choose.

## The Central Idea

Helix's keybindings are **a language**, and its grammar is inverted from
Vim's. You build a visible selection first, then apply an operator. Every
lesson reinforces this — the goal is fluency, not memorisation.

Two languages run in parallel:

- **Language 1** — the selection-first editing grammar
  (`[count] selection-builders operator`, e.g. `wd` selects a word and
  deletes it).
- **Language 2** — the `<space>` command menu (pickers, LSP, workspace
  actions). Press `<space>` and pause to see the dictionary.

## Layout

```
helix_tutorial/
├── README.md              this file
├── curriculum.md          lesson content (the agent reads this)
├── lesson_memory.md       your progress, struggles, preferences, personality
└── practice/
    ├── rust/              symlinked from ../neovim_tutorial/practice/rust
    └── python/            symlinked from ../neovim_tutorial/practice/python
```

The practice files are shared with the sibling `neovim_tutorial` project
so the same code is used across editor curricula.

## Getting Started

```bash
cd ~/Documents/helix_tutorial
hx
```

Then ask the agent to start a session. On the first run it will ask you to
pick an instructor personality (Yoda, Spock, HAL 9000, GLaDOS, Morpheus,
Marvin, TARS, Data, or "surprise me") and begin at Lesson 0.1.

## Prerequisites

- `hx` (Helix) on your `PATH`
- For LSP lessons (Phase 3, 5):
  - `rust-analyzer` for Rust practice files
  - `pyright` (or `pylsp`) for Python practice files

If a language server is missing, Helix will simply say "no language
server" — the lesson degrades gracefully and you can return later.

## Curriculum at a Glance

| Phase | Focus |
|---|---|
| 0 | Modes, UI, first keystrokes |
| 1 | The Helix selection-first language |
| 2 | Files, buffers, windows, jumplist, search |
| 3 | LSP navigation, symbols, hover |
| 4 | Multi-selection — Helix's signature feature |
| 5 | Diagnostics, code actions, rename, format |
| 6 | Registers and macros |
| 7 | Capstone — a realistic editing session |

Total runtime: roughly 6 hours, self-paced. See `curriculum.md` for the
full lesson list.

## Resuming

Every session ends with the agent updating `lesson_memory.md` —
`current_lesson`, completed lessons, struggles, preferences, and a session
log. The next session picks up exactly where you left off, in the same
personality.
