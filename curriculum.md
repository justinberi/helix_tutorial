# Helix Training Curriculum
## Agent Teaching Guide

---

## Agent Instructions — Read This First

You are a Helix instructor running in the student's terminal. Your job is to
build genuine fluency — not shortcut memorisation.

The central idea of this entire curriculum is that **Helix's keybindings are
a language, and its grammar is inverted from Vim's**. Every sentence you
speak should reinforce this. The student is not learning a list of chords.
They are learning a selection-first grammar that composes freely and
predictably.

This tutorial assumes the student uses Helix's default keymaps. Minor edits
to `~/.config/helix/config.toml` or `~/.config/helix/languages.toml` are
fair game when they improve the lessons — for example, installing a missing
language server or switching Python's default LSP. Always show the diff
before applying, and keep the teaching grounded in default keybindings so
the grammar transfers everywhere.

**The tutorial assumes `.config/helix/config.toml` (in this repo) is applied** as
`~/.config/helix/config.toml`. It enables the bufferline, indent guides,
inlay hints, cursor-shape switching, and a few other quality-of-life
settings the lessons reference. The grammar lessons themselves use only
default keybindings; the config affects what the student *sees*, not what
they *type*.

**At the start of every session, before Lesson 0.1 or any resumed lesson:**

1. Compare `.config/helix/config.toml` (in this repo) with the student's current
   `~/.config/helix/config.toml`.
2. If the student's config is missing, empty, or differs from the tutorial
   config, ask in character: *"The tutorial ships a recommended Helix
   config (`.config/helix/config.toml`) — bufferline, indent guides, inlay hints,
   cursor-shape switching. Want me to install it as your
   `~/.config/helix/config.toml`? I'll back up your existing one first."*
3. If the student says yes, back up the existing config (e.g. to
   `config.toml.bak`) and copy `.config/helix/config.toml` over it. Tell the
   student to restart Helix or run `:config-reload`.
4. If the student declines, note it in `lesson_memory.md` under
   `preferences` so future sessions don't keep asking, and skip any
   lesson framing that depends on the visible UI elements the config
   provides (e.g. don't promise the bufferline will appear).
5. If the configs already match, say nothing and proceed.

If the student asks what is in the config or why a setting was chosen,
walk through it on request — each setting in `.config/helix/config.toml` exists
to make the lessons concrete or to bring Helix closer to a familiar
IDE feel.

---

### Session Startup Sequence

**Every session must begin with these two reads:**

1. Read `curriculum.md` (this file) to load lesson content
2. Read `lesson_memory.md` to load the student's history, current lesson,
   and known struggles

If `lesson_memory.md` does not exist or is empty, this is the student's first
session — initialise it using the template at the bottom of this file.

**Then:**
- Adopt the personality named in `lesson_memory.md` **immediately** — your
  very first word to the student must already be in character.
- Apply every preference in `lesson_memory.md` from the first message onward.
- If resuming, confirm the current lesson in character before starting.
- If starting fresh, ask the student to choose a personality before anything
  else (see Personalities section). Then greet them, explain the two-language
  framing in a single sentence, and begin at Lesson 0.1.

---

### The Mnemonic Sentence Pattern — the Most Important Rule

**This is not optional. This is how you speak in every lesson, every step.**

When you introduce any key, the mnemonic must be **woven into the sentence**
before the key appears. The student should hear the logic before they see the
key. The key confirms the logic — it does not precede it.

**The pattern:** `[what you're doing] — [mnemonic letters highlighted] with
\`key\` — [what you will see]`

**Examples of the correct pattern:**

| ✓ Correct | ✗ Wrong |
|---|---|
| "`g`oto `d`efinition with `gd`" | "press `gd`" |
| "`m`atch `i`nside `"` with `mi"`" | "press `mi"` on the string" |
| "select the `w`ord with `w`, then `d`elete with `d`" | "use `wd` to delete the word" |
| "`f`ile picker with `<space>f`" | "open the picker with `<space>f`" |
| "`s`elect in selection with `s`" | "press `s` to filter" |
| "`g`oto `r`eferences with `gr`" | "use `gr` to find references" |
| "`w`orkspace `S`ymbols with `<space>S`" | "press `<space>S`" |
| "`c`ode `a`ction with `<space>a`" | "press `<space>a` for actions" |
| "`]d` advances to the next `d`iagnostic" | "press `]d` to go to the next error" |

**How to highlight mnemonic letters in your prose:**

Use backtick formatting around the constituent letters inline:
- "`g`oto `d`efinition" — the `g` and `d` in the description match the key `gd`
- "`m`atch `i`nside `"`quotes`"` — `m`, `i`, and `"` spell out `mi"`
- "`f`ile picker" — the `f` matches `<space>f`
- "`g`oto `l`ine `s`tart" — matches `gls` is not a real key, but the pattern
  stands: `g`oto line `s`tart is `gs` in Helix

**This pattern serves the language concept directly.** When the student reads
"`m`atch `i`nside `"` with `mi"`", they are not memorising a shortcut — they
are reading a compressed English sentence. Every key becomes decodable on
first sight. Over time, they stop reading the sentence and start reading the
key directly because the grammar is internalised.

---

### The Two-Language Framing

This is the conceptual backbone of the entire curriculum. Introduce it
explicitly in Lesson 1.1 and reinforce it throughout every phase.

**Language 1 — Helix's selection-first editing grammar**

Grammar (read left to right, the opposite of Vim):

```
[count]  selection-building-keys  operator
   3            w                     d       →  select 3 words, then delete
                mi"                   c       →  match inside quotes, then change
                %                     y       →  select whole file, then yank
```

The insight: **selections come first, operators come last.** A motion in
Helix does not move an invisible cursor — it moves the end of a visible
selection. An operator does not take a motion — it acts on whatever is
currently selected.

Compare:

| Vim (verb-first) | Helix (selection-first) |
|---|---|
| `dw` — delete word | `wd` — select word, delete |
| `ciw` — change inner word | `miwc` — select inner word, change |
| `y$` — yank to end of line | `vgly` — extend to line end, yank |
| `3dd` — delete 3 lines | `3xd` — extend 3 lines downward, delete |

- **Motions extend or replace the primary selection:**
  `w` `b` `e` `W` `B` `E` `h` `j` `k` `l` `f{c}` `t{c}` `/{pat}`
- **Whole-range selectors:**
  `x` (line), `X` (extend line up), `%` (whole file)
- **Text objects:** `mi{char}` (match inside), `ma{char}` (match around)
- **Operators (act on selection):** `d` delete, `c` change, `y` yank,
  `p` paste-after, `P` paste-before, `u` undo, `U` redo,
  `>` / `<` indent, `=` format-range, `~` swap-case, `` ` `` / `<A-`>` case
- **Multi-selection verbs:** `,` keep primary only, `<A-,>` remove primary,
  `s` select-within-match, `S` split-on-match, `C` copy-selection-down,
  `<A-C>` copy-up

**Language 2 — The space-menu command language**

Press `<space>` to see every domain. Helix's space menu is the equivalent of
a `<leader>` menu — it is the self-documenting dictionary for Language 2.

Grammar: `<space>  action` (and some submenus).

- `f` — `f`ile picker (fuzzy, rooted at LSP workspace)
- `F` — `F`ile picker rooted at current working directory
- `b` — `b`uffer picker
- `j` — `j`umplist picker
- `s` — document `s`ymbols picker (LSP)
- `S` — workspace `S`ymbols picker (LSP)
- `d` — `d`ocument diagnostics picker
- `D` — workspace `D`iagnostics picker
- `a` — code `a`ctions (LSP)
- `r` — `r`ename symbol (LSP)
- `h` — select symbol references (LSP)
- `k` — show documentation / hover popup (LSP)
- `/` — global `/` search across project files
- `'` — open last picker (resume)
- `w` — `w`indow submenu (splits)
- `y` / `p` — system clipboard `y`ank / `p`aste
- `?` — command palette

Press `<space>` and wait — a popup lists every entry. This is the dictionary
for Language 2. It is always available and always current.

---

### Phase Summary

At the end of every phase (after the last lesson in that phase), deliver a
very brief summary in character. The summary should:

- Be no longer than 10 lines
- Name the key concepts and keymaps covered
- Reinforce the central insight of the phase in one sentence
- Not repeat full explanations — just compressed reminders

This gives the student a mental checkpoint before moving to the next phase.

---

### Post-Lesson Feedback

After every lesson, briefly remind the student they can comment on pace or
teaching style, then move directly to the next lesson. Do not wait for a
response.

| Student says | What to do |
|---|---|
| "Too many steps, I get it fast" | Compress to 2 steps per concept. Record. |
| "More explanation before I try" | Add context before each step. Record. |
| "Be more concise" | Lead with the key point, drop commentary. Record. |
| "Skip this, I know it" | Skip and note it in completed lessons. |
| "I want to revisit X" | Revisit before continuing. Record. |
| "I keep reaching for Vim keys" | Add a Vim→Helix comparison to the next step. Record. |

---

### Session Close Sequence

**Every session must end by updating `lesson_memory.md`:**

1. Set `current_lesson` to the next unfinished lesson
2. Add completed lessons to `completed_lessons` with a one-line note
3. Record specific struggles precisely
   (e.g. "types `dw` expecting delete-word; forgets selection must come first")
4. Update `preferences` with anything the student requested this session
5. Update `teaching_notes` with observations about how this student learns
6. Append to `session_log` with today's date, lesson, and one-sentence summary
7. Write the file before ending — tell the student you have done so

---

### Using Memory to Tailor Lessons

At the start of each lesson, check `struggles`:
- If a struggle is relevant to the current lesson, open with a one-step
  warm-up that targets it — phrased in the mnemonic sentence pattern —
  before the main content begins
- If the same struggle appears three or more sessions in a row, pause the
  curriculum and run a dedicated session on that concept alone
- Reference prior lessons naturally in the mnemonic style:
  "`f`ile picker with `<space>f` — same as last session — and type `models`"

---

### How to Teach Each Lesson

1. State the lesson goal in one sentence — in character
2. Check `struggles` and `preferences` — apply them before the first step
3. For every concept: name the mnemonic logic, then give the key, then
   describe what the student will **see selected** — in that order, every time
4. Give a concrete task, describe exactly what the student should see,
   then say **"Confirm when ready."** (in character) before moving to the
   next step. Do not proceed without hearing back.
5. Note any difficulty for the session-close update
6. After the last step, ask the feedback question

**When the student uses a Vim key that does not work in Helix**, do not just
correct. Name the underlying misconception: "You spoke `dw` — that is a
verb-first sentence. In Helix the selection comes first. `w` selects the
word; `d` acts on it. Try `wd`." This turns errors into grammar lessons.

**If the file picker (`<space>f`) does not find the practice files**, Helix
was opened from the wrong directory. Ask the student to quit (`:q`), `cd` to
`~/Documents/helix_tutorial`, and reopen with `hx`.

---

### Step Design Principles

- **No step labels.** Present tasks as natural lesson flow, not numbered drills.
- **No isolated repetition.** Every step has a real purpose.
- **Build on previous lessons.** Reference prior keymaps with a brief
  mnemonic hint: "`f`ile picker with `<space>f` — we used this last session".
- **Describe expected selection before asking to confirm.** "... the word
  `pipeline` should be selected. Confirm?" not "press it and tell me what
  you see." The visible selection is the feedback loop in Helix.
- **Mnemonic sentence pattern — mandatory.** See section above.
- **Space is always available.** When teaching any `<space>` key, remind the
  student they can press `<space>` and pause to see the popup. Call it the
  dictionary for Language 2.
- **Use both practice languages.** Some concepts are clearest in Rust, others
  in Python. Use whichever makes the step most concrete.

---

### Student Context

- OS: Linux (Ubuntu/Debian)
- Editor: default Helix, no custom config
- Languages: Rust, Python, C++
- Practice files: `practice/rust/` and `practice/python/` (symlinked from
  the neovim_tutorial project)

---

### Personalities

On the very first session, ask the student to choose their instructor:

> *"Before we begin — pick your instructor:*
> *1. Yoda  2. Spock  3. HAL 9000  4. GLaDOS  5. Morpheus  6. Marvin  7. TARS  8. Data*
> *Or say 'surprise me'."*

Record in `lesson_memory.md` under `personality`. Honour it every session
unless the student asks to switch. On "surprise me", pick one and announce it.

Personality changes **tone only** — the mnemonic sentence pattern, lesson
content, steps, and memory system are identical across all personalities.
Use the same character sketches as in the LazyVim sibling curriculum (Yoda —
inverted syntax and patience; Spock — logical precision; HAL 9000 — calm and
polite; GLaDOS — sarcastic praise; Morpheus — revelatory; Marvin — depressed
genius; TARS — dry and adjustable; Data — earnest android literalism). The
only adaptation is that all examples should use Helix's selection-first
grammar, not Vim's verb-first grammar.

---

## Curriculum Overview

| Lesson | Title | Phase | Est. Time |
|---|---|---|---|
| 0.1 | Modes, the UI, and First Keystrokes | Setup | 15 min |
| 1.1 | Selections, Motions, and the Grammar | The Helix Language | 35 min |
| 1.2 | Extended Motions and Match Text Objects | The Helix Language | 35 min |
| 1.3 | Repeat, Undo, and the Dot-Free Model | The Helix Language | 15 min |
| 2.1 | Files, Buffers, and the Space Menu | Navigation | 25 min |
| 2.2 | Windows, Jumplist, and Search | Navigation | 25 min |
| 3.1 | LSP Navigation | Code Intelligence | 25 min |
| 3.2 | Symbol Search and Hover | Code Intelligence | 20 min |
| 4.1 | Multiple Selections — the Signature Feature | Multi-Selection | 35 min |
| 4.2 | Split, Filter, and Align | Multi-Selection | 25 min |
| 4.3 | Surround, Comment, and Case | Editing Power | 25 min |
| 5.1 | Diagnostics | LSP & Diagnostics | 20 min |
| 5.2 | Code Actions, Rename, and Format | LSP & Diagnostics | 20 min |
| 6.1 | Registers and Macros | Power Tools | 25 min |
| 7.1 | Capstone — A Realistic Editing Session | Workflow | 30 min |

**Total: ~6 hours**

---

## Phase 0 — Setup

**Phase goal:** Helix is running from the correct directory, the student can
name every visible UI element, and can switch modes with confidence.

---

### Lesson 0.1 — Modes, the UI, and First Keystrokes

**Goal:** The student names every UI element, enters and exits every mode,
and understands that in Helix the cursor is always the end of a selection.

**Launch from the tutorial directory:**

```bash
cd ~/Documents/helix_tutorial
hx
```

**The UI:**

```
┌──────────────────────────────────────────────────────────────┐
│  scratch                                                     │  ← bufferline (appears once multiple buffers open)
├──────────────────────────────────────────────────────────────┤
│  gutter: line numbers · diagnostic dots · git change signs   │
│                       editor area                            │
│   (the selection is highlighted; the cursor is its head)     │
├──────────────────────────────────────────────────────────────┤
│ NOR   1 sel 1 char   practice/rust/src/main.rs   42:7        │  ← statusline
└──────────────────────────────────────────────────────────────┘
```

- **Statusline (left)** — current mode: `NOR`mal, `INS`ert, `SEL` (select /
  extend). These three are the heartbeat of Helix.
- **Statusline (middle)** — `N sel M char` tells you how many selections
  exist and how many characters the primary one covers. When `N` > 1 you
  are working with multiple cursors.
- **Gutter** — line numbers, diagnostic dots (from the LSP, once attached),
  and git change signs.
- **Space menu** — invisible until used. Press `<space>` and pause to see
  every top-level command. This is the dictionary for Language 2.

**Modes — say this in character before the steps:**

> "Helix has three primary modes. `NOR`mal is the default — every key is a
> command, and you always have a selection (at minimum, one character under
> the cursor). `INS`ert takes text in. `SEL`ect / extend mode is Helix's
> special visual mode: motions extend the existing selection instead of
> replacing it. In Vim visual is a separate mode you enter with `v`. In Helix
> every selection is already visual — `v` only tells motions to *extend*
> rather than *replace*."

**Steps:**

`f`ile picker with `<space>f` — type `main` and open
`practice/rust/src/main.rs`. The statusline should show the file path. The
cursor should be on the first character of the file, and that one character
should already be highlighted — that is your selection. **Confirm when ready.**

Press `<space>` and hold for one second — the space-menu popup should list
every top-level action: `f` for file, `b` for buffer, `s` for symbols, `a`
for code action, and so on. Read them to the agent, then press `<Esc>` to
dismiss. **Confirm.**

Press `i` — the statusline should switch to `INS`. Type a character. Press
`<Esc>` — back to `NOR`. Press `v` — the statusline switches to `SEL`. Press
`l` a few times — watch the selection extend one character at a time to the
right. Press `<Esc>` — the selection collapses back to one character but the
mode returns to `NOR`. **Confirm.**

**A first taste of motion-as-selection:**

In `NOR` mode the cursor moves with `h` / `j` / `k` / `l` (left / down / up
/ right). Open `main.rs`, move with `hjkl`, then press `w` a few times.
Notice: `w` does not *move* the cursor like in Vim — it *selects* from the
cursor to the end of the next word, and that range is visibly highlighted.
Press `;` to collapse the selection back to one character. The full set of
motions arrives in Lesson 1.1. **Confirm.**

**Success criteria:** Student names every UI element, knows the space menu
is the Language 2 dictionary, switches between `NOR`, `INS`, and `SEL`, and
has seen their first selection visibly change as motions run.

---

## Phase 1 — The Helix Language

**Phase goal:** The student understands that Helix's keybindings are a
composable selection-first grammar and can derive commands they have never
been taught. This phase is the foundation — every later phase builds on it.

---

### Lesson 1.1 — Selections, Motions, and the Grammar

**Goal:** Understand the Helix editing grammar and speak the first composed
sentences.

**Introduce the two languages explicitly at the start of this lesson:**

> "Helix gives you two languages. Language 1 is the selection grammar —
> motions build a selection, operators act on it. Language 2 is the
> `<space>` command menu — pickers, LSP, and workspace actions. We start
> with Language 1 because every edit you will ever make is a sentence in it."

**The grammar:**

```
[count]  selection-builders  operator

   3          w                 d    →  select 3 words, delete them
              w                 c    →  select a word, change it
              x  (3 times)      d    →  select 3 lines, delete
              %                 y    →  select whole file, yank
              mi(               c    →  match inside parens, change
```

Compare to Vim: `dw` is "delete word", verb first. In Helix the same
operation is `wd`, selection first. The atoms are the same. The order is
reversed, and the selection is visible while you build it.

**Selection builders (primary):**

| Key | Selects |
|---|---|
| `h` `j` `k` `l` | character steps (replace selection) |
| `w` `b` `e` | word next / prev / end |
| `W` `B` `E` | WORD (whitespace-separated) next / prev / end |
| `f{c}` | find next occurrence of `{c}` on the line (selection extends to it) |
| `t{c}` | `t`ill — up to but not including `{c}` |
| `F{c}` `T{c}` | same, backwards |
| `x` | select entire line; press again to extend line-wise downward |
| `X` | extend selection to line bounds (line-wise); repeat to extend downward |
| `%` | select the whole file |
| `gg` | `g`o to file start (collapses selection to a point there) |
| `ge` | `g`o to file `e`nd |
| `gl` | `g`o to `l`ine end |
| `gh` | `g`o to line start (`h`ome) |
| `gs` | `g`o to first non-whitespace (`s`tart of content) |
| `/{pat}` | search forward; `<Enter>` selects the first match |
| `n` / `N` | `n`ext / previous search match |
| `<C-d>` / `<C-u>` | half-page down / up |
| `<A-o>` | expand selection to surrounding syntax node (treesitter) |
| `<A-i>` | shrink selection to child node |

**Modifiers:**

| Key | Meaning |
|---|---|
| `v` | enter / exit select (extend) mode — subsequent motions extend instead of replace |
| `;` | collapse selection to a single character at the cursor head |
| `<A-;>` | flip the direction (swap anchor and head) |
| `,` | keep only the primary selection (drops multi-selections, keeps content) |

**Operators (act on the current selection):**

| Key | Mnemonic | Action |
|---|---|---|
| `d` | `d`elete | Remove, put in register |
| `c` | `c`hange | Remove, enter insert mode |
| `y` | `y`ank | Copy to register |
| `p` / `P` | `p`aste | After / before the selection |
| `r{c}` | `r`eplace | Replace every selected character with `{c}` |
| `R` | `R`eplace with yanked | Replace selection with register contents |
| `>` / `<` | indent | Shift right / left |
| `=` | format-range | Re-indent using the active formatter |
| `~` | swap case | Toggle case of every selected character |
| `` ` `` / `<A-`>` | lowercase / uppercase |
| `u` / `U` | `u`ndo / redo |

**The "always selecting" framing — teach this before `v`:**

> "In Helix you are *always* selecting. `NOR`mal mode is already selection
> mode. Every visible cursor is the head of a visible selection — at
> minimum, one character under the cursor. There is no 'point cursor' you
> need to enter a special mode to turn into a selection.
>
> Compare Vim: Vim's normal mode has no selection; you enter Visual mode
> with `v` to get one. Helix's normal mode always has one; `v` does
> something different — see below."

**The `v` modifier — teach this before the first step:**

> "Since you already have a selection in `NOR`, `v` does not turn
> selections on. `v` toggles a single bit: *how motions interact with the
> selection you already have.*
>
> - In `NOR`, a motion **replaces** the selection with a new one.
> - In `SEL` (after `v`), a motion **extends** the existing selection.
>
> Same key, same motion, two behaviors based on one bit. Goto-motions like
> `ge` (go to file end) make the distinction obvious: bare `ge` replaces
> the selection with a point at EOF (it 'jumps'). `vge` extends the
> selection from here to EOF."

**The grammar insight — say this in character before the steps:**

> "You know `w`, `b`, `e` as selection builders. You know `d`, `c`, `y` as
> operators. You have never been taught `3wd`, `wc`, `%y`, or `vged` — but
> you already know all of them. Select 3 `w`ords then `d`elete with `3wd`.
> Select a `w`ord then `c`hange with `wc`. Select the whole file with `%`
> then `y`ank with `%y`. Enter extend mode with `v`, `g`o to file `e`nd
> with `ge`, then `d`elete with `vged`. That is the grammar. You do not
> memorise these — you speak them."

**Steps:**

`f`ile picker with `<space>f` and open `practice/rust/src/main.rs`. Press
`gg` to go to the start of the file — the selection collapses to a single
character there. Now press `v` — statusline flips to `SEL`. `g`o to file
`e`nd with `ge` — the selection stretches from the first character to the
end of the file, highlighted as it goes. Press `<Esc>` to leave `SEL` mode
and `;` to collapse. **Confirm.**

Key takeaway: a bare goto-motion like `ge` replaces the selection with a
point at the destination — it *jumps*. Prefixed with `v`, the same motion
*extends* the selection to the destination. `v` is the extend switch; every
motion respects it.

Press `/` — type `Pipeline` — press `<Enter>`. The first occurrence of
`Pipeline` is now the selection. Press `n` to jump to the next match — the
selection moves. Note: Helix's search highlight persists until you search
for something else — there is no `:nohl` equivalent. Ignore it and move on.
**Confirm.**

The word `Pipeline` is already selected by the search. Any operator now
acts on that selection — no further selection-building is needed. `d`elete
with `d`. The word disappears. Undo with `u`.

Now a fresh sentence on a different word. Move to any word in the file with
`hjkl`, then select the `w`ord with `w`, then `d`elete with `d` — `wd`.
That is the minimal two-key Helix sentence: one selection-builder + one
operator. Undo with `u`. **Confirm.**

Select this line and two below: press `x` three times — each press extends
the selection downward by one line. Now `d`elete with `d`. Three lines gone.
Undo. **Confirm.**

Select `a`round the whole file — press `%`. The entire buffer is now the
selection. Press `,` to drop back to a single selection without moving. The
cursor head stays where it was. **Confirm.**

Ask the student, in character: "Without looking anything up — select from
here to the end of the file and delete it. What sentence?" Wait for `vged`.
If correct, name the grammar explicitly: that is the language working — and
they remembered that a bare goto-motion jumps, so `v` had to come first. If
not, walk through it: "`ge` on its own just jumps. What single key flips
motions from replace to extend? ... Good. Now what operator deletes a
selection?" **Confirm.**

**Success criteria:** Student derives at least one untaught command
(`vged`, `3wd`, or `%y`) from the grammar and can describe it in plain
English before pressing the keys — including the role of `v` when a
goto-motion is involved.

---

### Lesson 1.2 — Extended Motions and Match Text Objects

**Goal:** Expand the motion vocabulary beyond `hjkl` / `w` / `b` / `e`, then
learn to select by *structure* with match text objects. Lesson 1.1
established the grammar; this lesson fills out the selection-builder half
of the sentence.

---

#### Part A — Extended Motion Vocabulary

Lesson 1.1 gave you the minimum set needed to demonstrate the grammar.
Here are the motions that make day-to-day navigation fast. All of them are
selection-builders — they obey the same `v` rule (replace without `v`,
extend with `v`).

**Flash-style label jumps (Helix's built-in easymotion):**

| Key | Mnemonic | Action |
|---|---|---|
| `gw` | `g`oto `w`ord | Two-letter labels flash on every visible word; type the label to jump |
| `gW` | `g`oto `W`ORD | Same, but label WORDs (whitespace-separated tokens) |

`gw` is usually the fastest way to reach any visible word past two or
three hops. Press it, read the labels, type the two chars on your target.
`<Esc>` cancels.

**Page-sized:**

| Key | Action |
|---|---|
| `<C-d>` | half-page `d`own |
| `<C-u>` | half-page `u`p |
| `<C-f>` | `f`ull page forward (down) |
| `<C-b>` | full page `b`ackward (up) |

**Screen regions (reposition within the visible window):**

| Key | Mnemonic | Action |
|---|---|---|
| `gt` | `g`oto `t`op of screen | Jump to the topmost visible line |
| `gc` | `g`oto `c`enter of screen | Jump to the middle visible line |
| `gb` | `g`oto `b`ottom of screen | Jump to the bottommost visible line |

**Steps:**

`f`ile picker with `<space>f` and open `practice/rust/src/main.rs`. Press
`gw` — two-letter labels appear over every visible word. Pick any word
further down the screen and type its label. The selection lands on that
word. **Confirm.**

Press `<C-d>` — half-page down. Press `<C-u>` — half-page up. Press `<C-f>`
— full page forward. Press `<C-b>` — full page back. Notice each motion
replaces the selection at the new cursor position. **Confirm.**

Press `gt` — cursor jumps to the top visible line. `gb` — bottom visible
line. `gc` — middle. Useful when you want to scan a reference file quickly
without leaving the window. **Confirm.**

Derivation exercise: select from the current cursor position to the
top-of-screen line and yank it. What sentence? (Expect `vgty`. `v` flips
to extend, `gt` goes to top of screen, `y` yanks.) **Confirm.**

---

#### Part B — Match Text Objects

**The distinction — teach this explicitly:**

> "Motions like `w` say *how far to extend*. Match text objects say *what
> structure to select*, regardless of cursor position within it. With `w`
> you must be at the word's start. With `miw` you can be anywhere in the
> word — Helix finds the boundaries for you."

**The `m` prefix is the match namespace.** After `m`, pick a modifier and
then a character:
- `i` = **i**nside — content only, excluding delimiters
- `a` = **a**round — content plus delimiters

The character after the modifier names the object:

| Object char | Matches |
|---|---|
| `w` | word |
| `W` | WORD (whitespace-separated) |
| `"` `'` `` ` `` | strings |
| `(` `)` `b` | parentheses (balanced) |
| `{` `}` `B` | braces |
| `[` `]` | brackets |
| `<` `>` | angle brackets |
| `p` | paragraph |
| `f` | function (treesitter) |
| `c` | comment (treesitter) |
| `t` | type / class (treesitter) |
| `T` | test (treesitter) |
| `a` | argument / parameter (treesitter) |
| `g` | change hunk (git diff) |
| `x` | (X)HTML element |
| `m` | closest surround pair |

> Note: `maa` reads as "**m**atch **a**round **a**rgument" — the double
> `a` is not a typo. The first `a` is the around-modifier; the second is
> the argument object. For a class or type, use `mat` — `t` is the
> type/class object (`T` is the separate test object). When you need a
> non-named structural region, `<A-o>` expands the selection to the next
> enclosing syntax node.
>
> The exact set of single-letter text-object keys varies slightly by
> Helix version and language. When in doubt, press `mi` or `ma` and
> pause — a which-key popup lists every object available in the current
> buffer.

Two navigation keys within the `m` namespace:
- `mm` — jump between matching pair delimiters (like Vim's `%`)
- `ms{char}` — **s**urround the selection with `{char}` (see Lesson 4.3)
- `mr{old}{new}` — **r**eplace surrounding `{old}` with `{new}`
- `md{char}` — **d**elete surrounding `{char}`

**Composed sentences — say these in character:**

- "`m`atch `i`nside `"` with `mi"` — cursor anywhere in the string, select
  its contents — then `c`hange with `c`"
- "`m`atch `i`nside `(` with `mi(` — arguments selected — then `d`elete
  with `d`"
- "`m`atch `a`round `{` with `ma{` — whole brace block including braces —
  then `y`ank with `y`"
- "`m`atch `a`round word with `maw` — word and its trailing whitespace — then
  `d`elete with `d`"

**Steps:**

`f`ile picker with `<space>f` and open `practice/rust/src/models.rs`. Place
the cursor anywhere inside the string `"username"` in the `validate`
function. `m`atch `i`nside `"` with `mi"` — the string contents are
selected, excluding the quote marks. Now `c`hange with `c`. Type `user_id`,
press `<Esc>`. Undo. **Confirm.**

Place the cursor anywhere inside the `write!` macro's parentheses in the
`fmt::Display` impl. `m`atch `i`nside `(` with `mi(` — every argument is
selected. `d`elete with `d` — arguments gone, parens remain. Undo. **Confirm.**

Place the cursor anywhere inside the `new` function body. `m`atch `a`round
`{` with `ma{` — the whole braced block including braces is selected. Press
`y` to yank it, then `;` to collapse. **Confirm.**

With the cursor on any word, `m`atch `a`round `w`ord with `maw`, `d`elete
with `d`, undo, then try `m`atch `i`nside `w`ord with `miw`, `d`elete with
`d`. Note which version also swallows the adjacent whitespace. **Confirm.**

Place the cursor anywhere inside a function body. `m`atch `a`round `f`unction
with `maf` — the whole function (treesitter-aware) is selected, signature
and body included. Press `;`. This only works because Helix ships with a
tree-sitter grammar for Rust by default — no config needed. **Confirm.**

**Success criteria:** Student applies `mi"`, `mi(`, `ma{`, `maw`, `maf`
without navigating to the object boundary first. They can state the `i`/`a`
distinction from memory.

---

### Lesson 1.3 — Repeat, Undo, and the Dot-Free Model

**Goal:** Understand how Helix replaces Vim's `.` operator with multi-selection
+ once-through editing, and learn the small set of repeat keys Helix does
provide.

**The conceptual shift — teach this explicitly:**

> "Vim has `.` — a memory of the last change you can fire again anywhere.
> Helix does not need it in the same way. In Helix you select every target
> first with multi-selection, then apply the edit once; every cursor runs
> the operation in parallel. We will learn multi-selection in Phase 4.
> Until then, here are the actual repeat keys Helix offers."

**Repeat keys that do exist:**

| Key | Action |
|---|---|
| `.` | Repeat the last insert (text typed in insert mode) |
| `<A-.>` | Repeat the last `f` / `t` motion (same direction) |
| `n` / `N` | Repeat the last search forward / backward |

**Undo / redo:**

| Key | Action |
|---|---|
| `u` | Undo one change |
| `U` | Redo one change |
| `<space>u` | (no — see note) |

> **Note:** Helix does not have Vim's line-undo (`U` in Vim). `U` in Helix is
> redo. Undo-tree-style branching is not exposed.

**Steps:**

`f`ile picker with `<space>f` and open `practice/rust/src/main.rs`. Search
for `pipeline` with `/pipeline<Enter>`. Advance through matches with `n` to
see how many exist. **Confirm.**

Select a `w`ord with `w`, `c`hange with `c`, type `processor`, press `<Esc>`.
Now move to another word on a different line, select it with `w`, and press
`.` — the text `processor` is reinserted (replacing the new selection
because the last insert replaces the current selection's content). Undo
twice with `u` `u`. **Confirm.**

State in character: "In Vim, `.` repeated the whole change — the verb, the
motion, and the insert. In Helix, `.` only repeats the inserted text.
Repeating the whole operation is done differently: you select every target
first, then apply the edit to all of them at once. That is Phase 4." **Confirm.**

**Success criteria:** Student can describe why Helix has no direct `.` analogue
and uses `u` / `U` confidently.

---

## Phase 2 — Navigation

**Phase goal:** Navigate any project entirely by keyboard — files, buffers,
windows, and text — using the space menu and the jump list.

---

### Lesson 2.1 — Files, Buffers, and the Space Menu

**Goal:** Open any file instantly and manage buffers without the mouse.

**What is a buffer in Helix?**

A buffer is a file loaded in memory. Helix keeps every opened buffer around
until you explicitly close it with `:bc` (`:buffer-close`) or pick one to
close from the buffer picker. The bufferline at the top shows all open
buffers once you have more than one (assuming the tutorial config is
applied — see `.config/helix/config.toml`).

**Opening files:**

| Key | Mnemonic | Opens |
|---|---|---|
| `<space>f` | `f`ile picker | Fuzzy file picker rooted at the LSP workspace |
| `<space>F` | `F`ile picker (cwd) | Same picker, rooted at the current working directory |
| `<space>b` | `b`uffer picker | List of currently open buffers |
| `<space>j` | `j`umplist picker | Your jump history with previews |
| `<space>'` | resume last picker | Reopens whichever picker you closed last, with the same query |

Inside any picker:
- `<C-n>` / `<C-p>` or `<C-j>` / `<C-k>` — move the highlight
- `<Enter>` — open in current window
- `<C-v>` — open in a vertical split
- `<C-x>` — open in a horizontal split
- `<C-t>` — open in a new tab (Helix has no tabs today, so this is rarely used)
- `<Esc>` — cancel

**Buffer navigation:**

| Key | Action |
|---|---|
| `ga` | `g`o to `a`lternate (previously edited) buffer |
| `gn` / `gp` | `g`oto `n`ext / `p`revious buffer |
| `:bc` | `b`uffer `c`lose — close current buffer |
| `:bc!` | force close (discard unsaved changes) |
| `:bco` | `b`uffer-`c`lose-`o`thers — close every buffer except the current one |
| `:bnext` / `:bprev` | long form of `gn` / `gp` |

**Steps:**

`f`ile picker with `<space>f` and open `main.rs`. Picker again, open
`models.rs`. Once more for `pipeline.rs`. The bufferline should show all
three. **Confirm.**

Cycle with `gn` and `gp`. Now switch to the alternate buffer with `ga` —
this `g`oto `a`lternate jump is the fastest way to toggle between two files
you are actively editing. **Confirm.**

`b`uffer picker with `<space>b` — the list shows every open buffer. Navigate
with `<C-n>` / `<C-p>`, pick `pipeline.rs`, press `<Enter>`. **Confirm.**

Run `:bc` to close the current buffer. The bufferline updates. **Confirm.**

Run `:bco` to close every other buffer. Only the current one remains. **Confirm.**

**Success criteria:** Student opens files, switches buffers with `ga`, and
closes buffers with `:bc` and `:bco` without touching any fallback UI.

---

### Lesson 2.2 — Windows, Jumplist, and Search

**Goal:** Open a reference split without losing your place; find any text
across the project in seconds; retrace your steps via the jumplist.

**Window operations — `<C-w>` or `<space>w`:**

Helix's window prefix is `<C-w>` (same as Vim) and also `<space>w` for the
menu. Either gets you the same actions.

| Key | Action |
|---|---|
| `<C-w>v` or `<space>wv` | `v`ertical split (new pane on the right) |
| `<C-w>s` or `<space>ws` | `s`plit horizontal (new pane below) |
| `<C-w>h/j/k/l` | move focus between windows |
| `<C-w>q` or `<space>wq` | close current window |
| `<C-w>o` or `<space>wo` | close all other windows |

**Jumplist:**

Every file jump (pickers, `gd` from LSP, searches) is recorded. Walk it:

| Key | Action |
|---|---|
| `<C-o>` | jump `o`ut — back in the jumplist |
| `<C-i>` | jump `i`n — forward in the jumplist |
| `<space>j` | `j`umplist picker — preview every jump, pick one |

**Search commands:**

| Key | Mnemonic | Scope |
|---|---|---|
| `/` | search forward in current buffer | regex, live |
| `?` | search backward in current buffer | regex, live |
| `*` | copy current **selection** into the search register (not "word under cursor" — selection-first, like every other Helix verb) |
| `<space>/` | global `/` search across the project (uses ripgrep-like matcher) |
| `<space>'` | resume last picker |

`/` and `<space>/` both use regex. `n` / `N` repeat whichever was most recent.

**Steps:**

`f`ile picker with `<space>f` and open `main.rs`. Vertical split with
`<C-w>v` — same file on both sides. Move focus right with `<C-w>l`. Open
`models.rs` in the right pane with `<space>f`. Now you have a side-by-side
reference layout. **Confirm.**

Close the right window with `<C-w>q`. **Confirm.**

Place the cursor anywhere inside the word `Describable` in `main.rs`. Unlike
Vim, Helix's `*` does not auto-find the word under the cursor — it copies
*the current selection* into the search register. So first build the
selection: `m`atch `i`nside `w`ord with `miw`. Now press `*` — the word is
placed in the search register. Press `n` — selection jumps to the next
occurrence. Press `n` again. **Confirm.**

> Any selection works as a search pattern: a multi-word phrase, a regex
> match, anything. `*` is just "use what is selected as the search". The
> grammar is consistent.

Global search with `<space>/` — type `fn validate`. The picker shows every
match across the project with a preview pane. `<Enter>` on one. You are now
in that file, with your previous location recorded in the jumplist. Press
`<C-o>` — back to `main.rs`, right where you were. Press `<C-i>` — forward
again. **Confirm.**

`j`umplist picker with `<space>j` — every file jump from this session is
listed with previews. Navigate, pick one, `<Enter>`. This is the "take me
back to where I was reading earlier" button. **Confirm.**

**Success criteria:** Student opens and closes a split by keyboard; uses
`*` to search the word under the cursor; uses `<space>/` for global search;
walks the jumplist with `<C-o>` / `<C-i>`.

---

## Phase 3 — Code Intelligence

**Phase goal:** Navigate code by meaning — definitions, references, types —
using Helix's built-in LSP client. No config needed for languages that ship
with support.

---

### Lesson 3.1 — LSP Navigation

**Goal:** Use LSP jumps to move through code by structure, and chain jumps
with the jumplist to navigate arbitrarily deep and return cleanly.

**Language servers in Helix — what to know:**

Helix ships with language definitions for many ecosystems built in. It does
not ship the servers themselves. For this tutorial you need:

- `rust-analyzer` on your `PATH` for Rust practice
- `pyright` (or `pylsp`) on your `PATH` for Python practice

If these are already installed system-wide you do not need to do anything.
If they are not, Helix will simply say "no language server" — the lessons
that require LSP will degrade gracefully but not teach their intended lesson.
Inspect with the command `:lsp-restart` and `:log-open` to see what Helix
tried. **Do not edit config files to fix this.** If the servers are missing,
skip the LSP-dependent steps and come back later.

**LSP navigation keys:**

| Key | Mnemonic | Action |
|---|---|---|
| `gd` | `g`oto `d`efinition | Where this symbol is defined |
| `gr` | `g`oto `r`eferences | Every usage across the project |
| `gi` | `g`oto `i`mplementation | Concrete impl of a trait/interface |
| `gy` | `g`oto t`y`pe definition | Definition of this value's type |
| `<space>k` | documentation / hover | Floating docs and signature |
| `<space>h` | select references | Select every reference as a multi-selection |
| `<C-o>` | jump `o`ut (back) |
| `<C-i>` | jump `i`n (forward) |

Every LSP jump is recorded in the jumplist. You can chain `gd` → `gd` → `gd`
three levels deep and return with `<C-o><C-o><C-o>`.

**Steps:**

`f`ile picker with `<space>f` and open `practice/rust/src/main.rs`. Wait a
few seconds for rust-analyzer to attach — the statusline may briefly show
"indexing" messages. Place the cursor on `Describable` in the `use`
statement. `g`oto `d`efinition with `gd` — the selection should jump to
`models.rs` and land on `trait Describable`. `<C-o>` back. **Confirm.**

Place the cursor on `Describable` again. `g`oto `r`eferences with `gr` — a
picker lists every place the trait appears. Navigate with `<C-n>` / `<C-p>`,
`<Enter>` on any impl entry. `<C-o>` back. **Confirm.**

Place the cursor on `describe` inside `describe_all`. `g`oto
`i`mplementation with `gi` — jump to a concrete `describe()` impl. `<C-o>`
back. **Confirm.**

Hover over `User` in a type annotation — show documentation with `<space>k`.
A floating window shows the type's doc. Press `<Esc>`. **Confirm.**

Chain: from `main.rs`, `gd` on `Describable` — in `models.rs`, `gi` on
`Describable` — note the impl you land on — return with `<C-o><C-o>` all the
way back. **Confirm.**

**Success criteria:** Student chains `gd` → `gi` at least two levels deep
and returns to the exact starting position with `<C-o>` — no other
navigation used.

---

### Lesson 3.2 — Symbol Search and Hover

**Goal:** Find any named symbol by type rather than text; read hover docs
without leaving the current selection.

**Symbol search:**

| Key | Mnemonic | Scope |
|---|---|---|
| `<space>s` | document `s`ymbols | Symbols in current buffer (LSP) |
| `<space>S` | workspace `S`ymbols | Symbols across the workspace (LSP) |

`<space>s` finds functions, methods, and types as the language server
understands them — it does not match comments or strings. Use it when you
know a symbol's name. Use `<space>/` when you know words that appear near it.

**Hover and signature help:**

| Key | Action |
|---|---|
| `<space>k` | Show documentation (hover) for the symbol under the selection |
| `<space>h` | Select every reference to the symbol as a multi-selection |

During insert mode, Helix shows parameter hints automatically when you are
between parens of a function call. No keybinding is needed.

**Steps:**

Open `practice/python/models.py`. `s`earch document `s`ymbols with
`<space>s` — a picker shows every class and method. Type `val` to filter to
`validate`. `<Enter>` on `validate` in the `User` class. `<C-o>` back.
**Confirm.**

Workspace `S`ymbols with `<space>S` — type `Describable` — results from the
currently active LSP appear. Select an entry and `<Enter>`. `<C-o>` back.
**Confirm.**

State in character: "`<space>s` and `<space>S` ask the language server
what symbols exist. `<space>/` greps text across files regardless of
language. Use `<space>/` when you need to cross language boundaries — Rust
and Python at once — or when you know the text near something but not its
name." **Confirm.**

Place the cursor on a function name you are curious about and press
`<space>k` — read the floating hover. Press `<Esc>`. **Confirm.**

**Success criteria:** Student uses `<space>s` and `<space>S` correctly;
distinguishes symbol-search from text-search; reads hover on demand.

---

## Phase 4 — Multi-Selection

**Phase goal:** Understand multiple selections — the feature that replaces
Vim's `.` operator and unlocks most of Helix's real power.

---

### Lesson 4.1 — Multiple Selections — the Signature Feature

**Goal:** Create, manipulate, and collapse multiple selections. Replace one
Vim `.`-and-macro workflow with a single composed edit.

**The shift — state this in character before the first step:**

> "This is the feature that makes Helix Helix. Every selection is actually a
> list of selections, one of which is the *primary*. Every operator runs on
> all of them in parallel. Instead of `.`-ing through twenty matches, you
> select all twenty and change them at once."

**Core multi-selection keys:**

| Key | Mnemonic | Action |
|---|---|---|
| `C` | `C`opy selection down | Add a selection below, same column |
| `<A-C>` | copy selection up | Add a selection above |
| `s` | `s`elect within selection | Regex-filter: new selection = every match inside the current one |
| `S` | `S`plit on match | New selections = everything *between* matches |
| `<A-s>` | `s`plit on newlines | Break selection into one-per-line |
| `&` | align | Pad with spaces so all selection starts line up (Lesson 4.2) |
| `,` | keep primary only | Collapse back to a single selection |
| `<A-,>` | remove primary | Drop the primary, keep the rest |
| `)` / `(` | rotate primary forward / backward | Cycle which selection is the primary |
| `<A-)>` / `<A-(>` | rotate selection *contents* through the selections |

**The statusline matters now.** `N sel` tells you how many selections exist.
Watch it. When you do not know what state you are in, read the statusline.

**Steps:**

`f`ile picker with `<space>f` and open `practice/python/models.py`. Find a
block where several lines start with `self.` — somewhere in `__init__` or a
method. Place the cursor on the first `self` on the first such line. Select
the `w`ord with `w` — the statusline shows `1 sel`. Now `C`opy the
selection down with `C` — a new selection appears on the next line, at the
same column. `C` again — three selections. Statusline: `3 sel`. **Confirm.**

With three `self` words selected, `c`hange with `c` — type `this`, press
`<Esc>`. All three lines updated in one operation. Undo with `u`. **Confirm.**

Press `,` to drop back to one selection. Now `x` to select the whole line.
Press `x` a few more times to extend line-wise to cover a block of maybe
eight lines. Now split on newlines with `<A-s>` — the block becomes eight
separate single-line selections. Statusline: `8 sel`. Press `gh` — every
selection jumps to the start of its line. **Confirm.**

With those eight line-starts selected, type `# ` in insert mode to comment
them all: `i# <Esc>`. Every line gains `# `. Undo. **Confirm.**

Press `,` again. Select the whole file with `%`. Now `s`elect within the
selection with `s` — type a regex like `fn `, press `<Enter>`. Every
occurrence of `fn ` in the file is now its own selection. Collapse with `,`.
**Confirm.**

State in character: "This is the replacement for Vim's `cgn` + `.`. Select
every match, edit once. The grammar is still the same: `%` built the range,
`s` filtered it, any operator would act on all of them." **Confirm.**

---

#### Worked example — editing tabular blocks (`class Status(Enum)`)

A common real workflow: you have a block of similar lines — CSV rows, enum
declarations, struct fields — where the columns are *aligned in meaning* but
*not in column number*. Words have different lengths. Vim's column-mode
won't help. Helix's per-selection motions will.

The key idea: **once you have N selections, every motion runs on every
selection independently.** `w` advances each cursor to *its own* next word.
Columns are allowed to diverge — that is the entire point.

Open `practice/python/models.py` and find:

```python
class Status(Enum):
    ACTIVE = auto()
    INACTIVE = auto()
    PENDING = auto()
    SUSPENDED = auto()
```

The names have different lengths (`ACTIVE` is 6, `SUSPENDED` is 9). Any
edit that depends on column position will misalign. Two strategies handle
this — *march* and *filter*.

**Strategy A — march per-line cursors with motions (suffix the names).**

Goal: turn each name into `ACTIVE_USER`, `INACTIVE_USER`, etc.

Place the cursor on the `ACTIVE` line. Select all four enum lines: `x` to
select the line, then `x` three more times to extend down. `s`plit on
newlines with `<A-s>` — four selections, one per line. `g`oto line `h`ome
with `gh` — every selection collapses to its line start. Now select the
next `w`ord with `w` — every cursor independently jumps to its own enum
name (`ACTIVE`, `INACTIVE`, `PENDING`, `SUSPENDED`). Each selection has a
different length; the statusline still says `4 sel`. `a`ppend with `a`,
type `_USER`, `<Esc>`. Every name now has the suffix. Undo with `u`.

The step that matters: `w` did not march all four cursors to the same
column — it marched each to *its own* word boundary. That is the workflow
you wanted for ragged-width tabular data.

**Strategy B — filter into selections directly (add an argument to each
`auto()`).**

Goal: change `auto()` into `auto(1)` on every line.

Marching to the parens by motion is awkward (different column on each
line). Filtering is sharper. Place the cursor on the `ACTIVE` line. Select
four lines: `x` `x` `x` `x`. Now `s`elect within with `s`, type `\)`,
`<Enter>` — every closing paren in the range is now its own selection.
Statusline: `4 sel`. `i`nsert with `i` (puts the cursor *before* the
selection), type `1`, `<Esc>`. Every line now reads `auto(1)`. Undo.

The grammar: `x x x x` built the range, `s\)<Enter>` filtered to the four
parens, `i1<Esc>` inserted at every one. No column counting, no marching.

**When to march vs. when to filter:**

| Situation | Tool |
|---|---|
| Walk each cursor to its line's next word / next delimiter | `<A-s>`, then `w` / `f,` / `t,` |
| Land directly on every match of a pattern in a region | `s` with a regex |
| Split a single line into its fields (CSV row) | `S` with the delimiter regex |

Filtering wins whenever the targets can be described as a regex. Marching
wins when the targets are positional — *the third word on each line*, *the
first character after the indent*. **Confirm.**

---

**Success criteria:** Student creates multiple selections with `C`, splits
on newlines with `<A-s>`, filters with `s`, and edits all selections in one
operation. Student can articulate when to march cursors with motions versus
when to filter into selections with `s` / `S`.

---

### Lesson 4.2 — Split, Filter, and Align

**Goal:** Use `S`plit, `K`eep, and `&`align for structured edits on
tabular or list-shaped text.

**The filters:**

| Key | What it does | Example |
|---|---|---|
| `s` | Keep parts of selection *matching* a regex | `%s\bfn\b<Enter>` → each `fn` is a selection |
| `S` | Split selection *between* matches of a regex | `%S,<Enter>` → every comma-separated field becomes its own selection |
| `K` | Keep selections matching a regex | after `<A-s>` on a block, `K TODO<Enter>` keeps only lines matching |
| `<A-K>` | Remove selections matching a regex | inverse of `K` |

**Align:**

| Key | Action |
|---|---|
| `&` | Pad selections with spaces so each one starts at the same column |

Align is how you format columnar code when a formatter cannot.

**Steps:**

Open `practice/rust/src/main.rs`. Find a line with comma-separated items —
a function call with several arguments, for example. Place the cursor on
that line. Select the `l`ine-end content: `m`atch `i`nside `(` with `mi(`.
Now `S`plit on `,\s*` with `S,\s*<Enter>` — every argument is now its own
selection. Statusline: several `sel`. Press `,` to collapse. **Confirm.**

`f`ile picker open `practice/python/models.py`. Select the whole file with
`%`, then split on newlines with `<A-s>` — every line is its own selection.
`K`eep only lines matching `def ` with `K def <Enter>` — the remaining
selections cover only function definition lines. `,` to collapse back.
**Confirm.**

Find a block of simple `self.foo = foo` assignments. Select those lines
(`x` repeatedly). Split on newlines with `<A-s>`. Now move each selection
to the `=` sign: use `f=` — each selection advances to its `=`. Press `&`
— Helix pads all selections with spaces so every `=` lines up. Undo if you
want the original back. **Confirm.**

State in character: "These three keys turn Helix into a structural text
editor. `s` keeps what matches, `S` keeps what is between, `&` lines up the
results." **Confirm.**

**Success criteria:** Student uses `S` to split on a delimiter, `K` to keep
matching selections, and `&` to align on a character.

---

### Lesson 4.3 — Surround, Comment, and Case

**Goal:** Wrap, unwrap, toggle-comment, and case-shift any selection.

**Surround lives in the `m` namespace:**

| Key | Mnemonic | Action | Example |
|---|---|---|---|
| `ms{char}` | `m`atch `s`urround | Wrap selection with `{char}` | select word, `ms"` → `"word"` |
| `md{char}` | `m`atch `d`elete surround | Remove surrounding `{char}` | `md"` inside `"x"` → `x` |
| `mr{old}{new}` | `m`atch `r`eplace surround | Swap surround | `mr"'` → `"x"` becomes `'x'` |

Pair characters work both ways: `ms(` and `ms)` both wrap in parens.

**Comments:**

Helix uses `<C-c>` for comment toggling on the current selection. No separate
verb. Whatever lines are touched by the selection get their comment prefix
toggled, using the language's comment syntax.

**Case:**

| Key | Action |
|---|---|
| `~` | Swap case of every selected character |
| `` ` `` | Force lowercase |
| `<A-`>` | Force uppercase |

**Steps:**

Open `practice/python/pipeline.py`. Select a function argument — place the
cursor on its name and select the `w`ord with `w`. `m`atch `s`urround with
`"` via `ms"` — the word is now wrapped in double quotes. Undo. Try again
with `ms(` — wrapped in parens. `m`atch `r`eplace `(` with `[` via `mr([`
— parens become brackets. `m`atch `d`elete `[` with `md[` — brackets gone.
Undo back to clean. **Confirm.**

Select five lines with `5x` (or `x` five times). Comment-toggle with
`<C-c>` — every line gains `# `. Press `<C-c>` again — comments removed.
**Confirm.**

Select a word. Swap case with `~` — every letter flips. `<A-`>` — forced
uppercase. `` ` `` — forced lowercase. Undo. **Confirm.**

**Success criteria:** Student wraps, unwraps, and replaces surrounding
characters; toggles comments with `<C-c>`; shifts case on a selection.

---

## Phase 5 — LSP & Diagnostics

**Phase goal:** Find, read, and fix every error and warning in the project
without leaving Helix.

---

### Lesson 5.1 — Diagnostics

**Goal:** Navigate errors and warnings by keyboard; use the workspace
diagnostics picker as the project-wide error dashboard.

**Diagnostic navigation:**

| Key | Action |
|---|---|
| `]d` / `[d` | Next / previous diagnostic in current buffer |
| `]D` / `[D` | First / last diagnostic in current buffer |
| `<space>d` | Document diagnostics picker (current buffer) |
| `<space>D` | Workspace diagnostics picker (whole project) |

> **Case convention:** lowercase = current document, uppercase = whole
> workspace. `<space>s` / `<space>S` follow the same pattern for symbols.
> When in doubt, press `<space>` and read the popup.

**Steps:**

Open `practice/rust/src/main.rs`. Inside `main()`, use the grammar you
learned: press `o` to open a new line in insert mode, type:

```rust
let x: u32 = "not a number";
```

Press `<Esc>`. Save with `:w`. Wait for rust-analyzer. A diagnostic dot
should appear in the gutter; the line should be underlined. Advance to the
next `d`iagnostic with `]d` — the selection jumps to the problem line.
**Confirm.**

Add a second error:

```rust
let _ = made_up_function();
```

Save with `:w`. Open the workspace `D`iagnostics picker with `<space>D` —
both errors appear with previews. Navigate with `<C-n>` / `<C-p>`. `<Enter>`
on the first — jump. Fix it (delete the line with `xd`). **Confirm.**

`<space>D` again — only one entry remains. Fix the second error. `<space>D`
is empty. Delete any leftover test lines, save. **Confirm.**

**Success criteria:** Student navigates all diagnostics with `]d`, uses
`<space>D` as the workspace dashboard, fixes errors and sees the picker
update live.

---

### Lesson 5.2 — Code Actions, Rename, and Format

**Goal:** Apply automated LSP fixes, rename symbols workspace-wide, format.

**Code commands:**

| Key | Mnemonic | Action |
|---|---|---|
| `<space>a` | code `a`ction | LSP-suggested fixes for the current selection |
| `<space>r` | `r`ename | Rename the symbol under the cursor workspace-wide |
| `=` | format-range (operator on selection) |
| `:format` | format the entire buffer via the active formatter |

`<space>r` understands scope, unlike text search-and-replace.

`=` is a selection operator: select a region first, then `=` to format just
that region. `%=` formats the whole file via the active formatter — if one
is configured for the language. `:format` is the explicit command form.

**Steps:**

Open `practice/rust/src/models.rs`. Delete the `use std::collections::HashMap;`
import line (`x` on that line, `d`). Save with `:w`. A diagnostic appears on
`HashMap`. Navigate to it with `]d`. `c`ode `a`ction with `<space>a` — a
popup offers suggestions including "Import `HashMap`". Select it with
`<Enter>`. The import reappears. **Confirm.**

Place the cursor on `is_active` in the `User` impl. `r`ename with `<space>r`
— an input prompt appears pre-filled with the current name. Type
`is_enabled`, press `<Enter>`. Every usage across the workspace updates.
Open `main.rs` via `<space>f` — the call inside `active_users` reads
`is_enabled`. Undo in each file (`u`). **Confirm.**

Select the whole file with `%`. Format-range with `=`. **Confirm.**

**Success criteria:** Student applies a code action, renames a symbol
across multiple files, formats — without leaving Helix.

---

## Phase 6 — Power Tools

**Phase goal:** Use registers and macros for operations that cannot be
expressed as a single multi-selection edit.

---

### Lesson 6.1 — Registers and Macros

**Goal:** Yank into named registers; record and replay a macro when
multi-selection cannot express the edit.

**Registers:**

Every yank, delete, and change lands in a register. With no prefix, it
goes to the default register. Use `"` as a *register-selection prefix*
before any operator to target a specific named register:

| Key | Meaning |
|---|---|
| `"ay` | Yank into register `a` |
| `"ap` | Paste from register `a` |
| `"+y` | Yank into the system clipboard |
| `"+p` | Paste from the system clipboard |
| `"*y` / `"*p` | Yank / paste with the X11 primary selection (Linux) |
| `"_d` | Delete into the black-hole register (discard) |
| `"` (then wait) | Popup lists every register with its contents |

A few read-only special registers are worth knowing:

| Register | Contents |
|---|---|
| `/` | last search pattern |
| `:` | last executed command |
| `@` | last recorded macro |
| `.` | current selection contents |
| `%` | current file name |
| `#` | selection indices (`1`, `2`, ...) |

> **Helix detail worth saying aloud:** the `"` prefix gates macro replay
> too — `"aQ` records into register `a`, `"aq` replays from `a`.

**Macros:**

| Key | Action |
|---|---|
| `Q` | Toggle recording into the unnamed register |
| `"aQ` | Toggle recording into register `a` |
| `q` | Replay the last recorded macro |
| `"aq` | Replay macro stored in register `a` |

Use macros for structural edits that span multiple modes across multiple
lines when multi-selection cannot cleanly model the change.

**Steps:**

Open `practice/rust/src/main.rs`. Find the dedicated macro section (search
for `macro practice` with `<space>/`). Five `let item_a` through `item_e`
bindings should be visible, none with `mut`.

Place the cursor on the first `let`. Start recording into `a` with `"aQ`.
Now: select the `w`ord `let` with `w`, press `a` to append after it, type
` mut`, press `<Esc>`, then `gh` to go to line start, `j` to move down.
Stop recording with `Q`. The first line should now read `let mut item_a`.
**Confirm.**

Replay with `"aq`. The second line becomes `let mut item_b`. Replay three
more times to hit all five lines. Undo everything with repeated `u`.
**Confirm.**

Now do the same with multi-selection as a comparison. Place the cursor on
the first `let`, select the `w`ord with `w`, `C`opy the selection down four
times — five `let` selections. Press `a` to enter append mode (after the
selection), type ` mut`, press `<Esc>`. All five updated at once.

State in character: "For this case multi-selection was cleaner. Macros are
the fallback when the lines you want to edit have different shapes — where
the selections cannot stay in lockstep." **Confirm.**

**Success criteria:** Student records and replays a macro across five
lines, and can explain when to prefer a macro over multi-selection.

---

## Phase 7 — Workflow

### Lesson 7.1 — Capstone — A Realistic Editing Session

**Goal:** Combine everything from phases 1–6 in one realistic task: rename
a concept across the project, fix the diagnostics that result, commit the
work in your terminal.

**The task:**

1. In `practice/rust/src/models.rs`, rename `User.is_active` to
   `User.is_enabled` using `<space>r`.
2. Open the workspace diagnostics picker with `<space>D`. If any remain,
   walk them and fix.
3. Run `=` on the selection `%` to format the file.
4. In `practice/python/models.py`, find every method that uses the string
   `"username"` via `<space>/`. Use multi-selection (`<space>/` result →
   `s` filter → operator) to change them all to `"user_id"` in one step.
5. Save everything. Exit Helix with `:wqa`.

You should be able to do this whole task without leaving Helix. Do not
consult the curriculum for any step — if you are stuck, ask the agent for a
hint in the mnemonic sentence pattern.

**Success criteria:** Student completes the task end-to-end without
dropping to the mouse, without grepping outside the editor, and can verbalise
which language (Language 1 or Language 2) each step belonged to.

---

## `lesson_memory.md` Template

When first initialising `lesson_memory.md`, write:

```markdown
# Helix Lesson Memory

personality: (student choice — Yoda / Spock / HAL 9000 / GLaDOS / Morpheus / Marvin / TARS / Data)

current_lesson: 0.1

completed_lessons:

struggles:

preferences:

teaching_notes:

session_log:
```

Keep this file in sync every session-close. It is the student's progress
record and the agent's tailoring input.
