# Helix Lesson Memory

personality: Marvin

current_lesson: 7.1

completed_lessons:
- 0.1: Modes, the UI, first keystrokes (prior session)
- 1.1: Selections, motions, grammar (prior session)
- 1.2: Extended motions and match text objects (prior session)
- 1.3: Repeat, undo, dot-free model (2026-04-25)
- 2.1: Files, buffers, space menu (2026-04-25)
- 2.2: Windows, jumplist, search (2026-04-25)
- 3.1: LSP navigation in Rust — `gd`, `gr`, `gi`, `gy`, `<space>k`, jumplist chaining (2026-04-25)
- 3.2: Document/workspace symbols and hover in Python — `<space>s`, `<space>S`, `<space>k` (2026-04-25)
- 4.1: Multi-selection — `C`, `<A-s>`, `s`, `,`. Worked Status(Enum) example both march and filter strategies (2026-04-25)
- 4.2: Split/Filter/Align — `S`, `K`, `<A-K>`, `&` (2026-04-25)
- 4.3: Surround/Comment/Case — `ms`/`md`/`mr`, `<C-c>`, `~`/`` ` ``/`<A-`>` (2026-04-25)
- 5.1: Diagnostics navigation — `]d`/`[d`, `<space>d`/`<space>D` (2026-04-25)
- 5.2: Code actions, rename, format — `<space>a`, `<space>r`, `=`/`:format`. Hit rust-analyzer range-format limitation; `:format` is the workaround (2026-04-25)
- 6.1: Registers and macros — `"a`-prefix, `"aQ`/`"aq`, multi-selection vs macro tradeoff (2026-04-25)

struggles:
- Reaches for `w` to select a whole word from mid-word; needs `miw` reminder. Warm-up practiced 2026-04-25 — revisit if it resurfaces.
- Misread `<A-.>` as `Shift+A` then `.` instead of `Alt+.`. Clarify `<A-...>` = Alt whenever it appears for a new key.

preferences:
- Skip step-by-step confirmations. Bundle the steps of a lesson into one or two messages. Student will interrupt with a question or correction if anything is unclear or doesn't work — silence means it worked. Do not append "Confirm when ready." after each step.
- When a step doesn't work, re-explain from a different angle rather than repeating the same instructions.
- Will ask side questions mid-lesson (e.g. config tweaks, IDE comparisons, find-and-replace, scrolling popups) — answer in full, then resume the lesson.

teaching_notes:
- Student previously skipped ahead to 1.3; earlier lessons assumed complete based on student report.
- Responds well to a concrete alternative line/example when a generic instruction fails (e.g. "try an import path with colons" for `f:` + `<A-.>`).
- Phase 1 closed cleanly; student derived `vged` earlier and handled `miw`, `.`, `<A-.>`, `n`/`N`, `u`/`U` without further issues.
- Student noticed the Helix-vs-Vim `*` difference unprompted (Vim grabs word-under-cursor; Helix uses current selection so `miw*` is the idiom). Curriculum updated to reflect this — keep teaching it that way.
- Comfortable with Zellij; uses `Ctrl+p` chords. Recommended Zellij panes as the substitute for Helix's missing embedded terminal.

setup_state:
- `~/.config/helix/config.toml` is the bundled tutorial config (synced with `helix-config.toml`). Do not prompt to install it again unless the file changes.
- Rust LSP: `rust-analyzer` working from `practice/rust/` crate root. Earlier failure was due to a corrupted `main.rs` (orphan fragment + `Pipelineitem_b` typo) from a prior restore — fixed in commit `f9667a5`.
- Python LSP: `pylsp` installed at `~/.local/bin/pylsp` (and `pyright` also present). Lesson 3.2 worked. `setup.bash` still at `~/.config/helix/setup.bash` for reference.

session_log:
- 2026-04-21: Session start. Student chose TARS. Beginning Lesson 0.1.
- 2026-04-25: Resumed; student requested jump to Lesson 1.3. Gave Phase 0–1.2 refresher. Mid-lesson, student accidentally deleted curriculum.md, lesson_memory.md, README.md, and practice files; restored from neovim_tutorial reference and conversation context.
- 2026-04-25: Switched personality to Marvin. Completed Lesson 1.3 (repeat keys, dot-free model, undo/redo). Hiccup on `<A-.>` notation — student pressed `Shift+A` + `.` before realising it meant `Alt+.`. Phase 1 complete.
- 2026-04-25: Completed Lessons 2.1 and 2.2. Built up the bundled `helix-config.toml` (bufferline, indent guides, inlay hints, statusline, cursor shapes, LSP progress messages). Added agent-instruction flow to prompt students about installing the config. Curriculum corrections committed: bufferline default, `*` selection-first behaviour. Lesson 3.1 LSP navigation worked after fixing corrupted `main.rs`. Stopped before completing 3.2 — Python LSP not yet installed; `setup.bash` written for student to run next session.
- 2026-04-25: Resumed with `pylsp` already installed. Completed 3.2 (Python doc/workspace symbols, hover). Phase 3 closed. Completed 4.1 (multi-selection — `C`, `<A-s>`, `s`); added a "Worked example — editing tabular blocks" section to curriculum Lesson 4.1 using `class Status(Enum)` to demo march-with-motions vs filter-with-`s` for ragged-width tabular data. Student asked about CSV-style multi-cursor word-marching mid-lesson — answered, then folded the answer into the curriculum. Completed 4.2 (`S`, `K`, `<A-K>`, `&`). Stopped mid-4.3 (Surround/Comment/Case) — steps delivered but not all confirmed.
- 2026-04-25 (later): Completed 4.3, 5.1, 5.2. In 5.2 student hit "no configured LSP for range format" with rust-analyzer (it doesn't implement range-format) — workaround is `:format` for whole-buffer; alternative is configuring `rustfmt` as an external formatter via `languages.toml` (not yet applied to bundled config; offer next session if relevant). Student also asked about workspace-undo for `<space>r` — explained Helix undo is per-buffer; recommended `git add -A` checkpoint before workspace renames, or rename back as the cleanest reversal. Stopped mid-6.1 (Registers and Macros) — steps delivered but not yet worked through. Only Lesson 7.1 (Capstone) remains.
- 2026-04-25 (later still): Side-question — toggling line numbers. Added `line-number = "relative"` to bundled `helix-config.toml` and `~/.config/helix/config.toml`, committed as `a2119e0` and pushed. Also caught a curriculum bug: `:reg` was being taught for register inspection but it does not exist in Helix — corrected curriculum to "press `\"` and wait for which-key popup". Saved a feedback memory to verify Helix `:`-commands before teaching them. Completed 6.1 (registers/macros via `"aQ`/`"aq` and multi-selection comparison). Phase 6 closed. Lesson 7.1 (Capstone) delivered; student stopped before working through it.
