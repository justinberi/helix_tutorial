# Helix Cheatsheet

A reference of every command taught in `curriculum.md`, grouped by topic.
Descriptions include searchable keywords inline.

> **For agents:** If you are an agent reading this, you are a cheatsheet
> lookup helper. Spend minimal effort — find the relevant row(s), quote
> them, and stop. Do not re-teach or expand on concepts unprompted. If the
> user questions a description or says an entry is unclear / missing, then
> offer to expand the description or add a new row to this file.

---

## Modes

| Key | Description |
|---|---|
| `i` | enter `INS`ert mode for typing text input |
| `a` | append insert mode after the selection |
| `o` | open new line below in insert mode |
| `v` | toggle `SEL`ect / extend mode — motions extend instead of replace selection |
| `<Esc>` | exit current mode back to `NOR`mal mode / dismiss popup |

---

## Basic Motions (selection builders)

| Key | Description |
|---|---|
| `h` `j` `k` `l` | character step left / down / up / right (replaces selection) |
| `w` `b` `e` | next `w`ord / `b`ack word / word `e`nd (selection builder) |
| `W` `B` `E` | WORD (whitespace-separated) next / back / end |
| `f{c}` | `f`ind next occurrence of char on line, selection extends to it |
| `t{c}` | `t`ill — find up to but not including char |
| `F{c}` `T{c}` | same as `f` / `t` but searching backwards |
| `<A-.>` | repeat last `f` / `t` motion same direction |
| `;` | collapse selection to single character at cursor head |
| `<A-;>` | flip / swap selection direction (anchor and head) |

---

## Goto Motions (jumps)

| Key | Description |
|---|---|
| `gg` | `g`o to file start / beginning |
| `ge` | `g`o to file `e`nd |
| `gh` | `g`o to line start / `h`ome (column 0) |
| `gl` | `g`o to `l`ine end |
| `gs` | `g`o to first non-whitespace `s`tart of content |
| `gt` | `g`o to `t`op of visible screen |
| `gc` | `g`o to `c`enter of visible screen |
| `gb` | `g`o to `b`ottom of visible screen |
| `gw` | `g`oto `w`ord — flash-style two-letter label jump (easymotion) |
| `gW` | `g`oto `W`ORD — same but for whitespace-separated tokens |
| `ga` | `g`o to `a`lternate (previously edited) buffer toggle |
| `gn` / `gp` | `g`oto `n`ext / `p`revious buffer |
| `gd` | `g`oto `d`efinition (LSP) |
| `gr` | `g`oto `r`eferences (LSP) |
| `gi` | `g`oto `i`mplementation (LSP) |
| `gy` | `g`oto t`y`pe definition (LSP) |

---

## Page / Scroll Motions

| Key | Description |
|---|---|
| `<C-d>` | half-page `d`own |
| `<C-u>` | half-page `u`p |
| `<C-f>` | `f`ull page forward / down |
| `<C-b>` | full page `b`ackward / up |

---

## Whole-Range Selectors

| Key | Description |
|---|---|
| `x` | select entire `x` line; repeat extends line-wise downward |
| `X` | extend selection to line bounds; repeat extends downward |
| `%` | select the whole file / buffer |
| `<A-o>` | expand selection to surrounding syntax node (treesitter parent) |
| `<A-i>` | shrink selection to child node (treesitter) |

---

## Match Text Objects (the `m` namespace)

| Key | Description |
|---|---|
| `mi{c}` | `m`atch `i`nside object — content excluding delimiters |
| `ma{c}` | `m`atch `a`round object — content plus delimiters |
| `miw` / `maw` | inside / around `w`ord |
| `miW` / `maW` | inside / around `W`ORD whitespace-separated |
| `mi"` `mi'` ``mi` `` | inside string / quotes |
| `mi(` `mi)` `mib` | inside parentheses / parens (balanced) |
| `mi{` `mi}` `miB` | inside braces / curly brackets |
| `mi[` `mi]` | inside brackets / square brackets |
| `mi<` `mi>` | inside angle brackets |
| `mip` | inside `p`aragraph |
| `maf` | around `f`unction (treesitter) |
| `mac` | around `c`omment (treesitter) |
| `mat` | around `t`ype / class (treesitter) |
| `maT` | around `T`est (treesitter) |
| `maa` | around `a`rgument / parameter (treesitter) |
| `mag` | around change hunk / `g`it diff |
| `max` | around (X)HTML element |
| `mam` | closest surround / `m`atch pair |
| `mm` | jump between `m`atching pair delimiters (Vim's `%`) |

---

## Surround (within `m` namespace)

| Key | Description |
|---|---|
| `ms{c}` | `m`atch `s`urround — wrap selection with char |
| `md{c}` | `m`atch `d`elete surrounding char |
| `mr{old}{new}` | `m`atch `r`eplace surrounding char with new char |

---

## Operators (act on current selection)

| Key | Description |
|---|---|
| `d` | `d`elete selection (into register) |
| `c` | `c`hange — delete and enter insert mode |
| `y` | `y`ank / copy selection to register |
| `p` | `p`aste after selection |
| `P` | `P`aste before selection |
| `r{c}` | `r`eplace every selected character with char |
| `R` | `R`eplace selection with yanked register contents |
| `>` | indent / shift right |
| `<` | indent / shift left |
| `=` | format-range — re-indent / reformat selection |
| `~` | swap / toggle case of every selected character |
| `` ` `` | force `lowercase on selection |
| `<A-`>` | force UPPERCASE on selection |
| `<C-c>` | toggle line `c`omment on selection |
| `&` | align selections — pad with spaces so each starts at same column |

---

## Undo / Redo / Repeat

| Key | Description |
|---|---|
| `u` | `u`ndo last change |
| `U` | redo (Helix `U` is redo, not Vim line-undo) |
| `.` | repeat last insert (only inserted text, not whole change) |
| `<A-.>` | repeat last `f` / `t` find motion |
| `n` / `N` | `n`ext / previous search match repeat |

---

## Search

| Key | Description |
|---|---|
| `/` | search forward in current buffer (regex, live) |
| `?` | search backward in current buffer (regex) |
| `n` | `n`ext search match |
| `N` | previous search match |
| `*` | copy current selection into search register (selection-first, not word-under-cursor) |
| `<space>/` | global `/` project-wide search across files (ripgrep-style) |
| `<space>'` | resume / reopen last picker with same query |

---

## Multi-Selection

| Key | Description |
|---|---|
| `C` | `C`opy selection down — add selection below at same column |
| `<A-C>` | copy selection up — add selection above |
| `s` | `s`elect within selection — regex filter into matches |
| `S` | `S`plit on regex match — selections become text between matches |
| `<A-s>` | `s`plit on newlines — break selection into one-per-line |
| `K` | `K`eep selections matching regex |
| `<A-K>` | remove / drop selections matching regex |
| `,` | keep primary selection only — collapse multi to single |
| `<A-,>` | remove the primary selection, keep the rest |
| `)` / `(` | rotate primary forward / backward through selections |
| `<A-)>` / `<A-(>` | rotate selection contents through the selections |
| `&` | align selections — pad spaces to align starts |

---

## Files & Buffers (Space Menu — Language 2)

| Key | Description |
|---|---|
| `<space>f` | `f`ile picker — fuzzy file finder rooted at LSP workspace |
| `<space>F` | `F`ile picker rooted at current working directory (cwd) |
| `<space>b` | `b`uffer picker — list of open buffers |
| `<space>j` | `j`umplist picker with previews |
| `<space>'` | resume last picker |
| `ga` | `g`o to `a`lternate buffer toggle |
| `gn` / `gp` | `g`oto `n`ext / `p`revious buffer cycle |
| `:bc` | `b`uffer `c`lose current buffer |
| `:bc!` | force buffer close, discard unsaved changes |
| `:bco` | `b`uffer-`c`lose-`o`thers — close all except current |
| `:bnext` / `:bprev` | long form of `gn` / `gp` |
| `:w` | write / save buffer |
| `:q` | quit |
| `:wqa` | write all and quit all |

---

## Pickers (interaction inside any picker)

| Key | Description |
|---|---|
| `<C-n>` / `<C-p>` | move highlight down / up |
| `<C-j>` / `<C-k>` | move highlight down / up (alt) |
| `<Enter>` | open / select in current window |
| `<C-v>` | open in `v`ertical split |
| `<C-x>` | open in horizontal split |
| `<C-t>` | open in new tab |
| `<Esc>` | cancel / dismiss picker |

---

## Windows / Splits

| Key | Description |
|---|---|
| `<C-w>v` / `<space>wv` | `v`ertical window split (new pane right) |
| `<C-w>s` / `<space>ws` | `s`plit horizontal (new pane below) |
| `<C-w>h/j/k/l` | move window focus left / down / up / right |
| `<C-w>q` / `<space>wq` | `q`uit / close current window |
| `<C-w>o` / `<space>wo` | close all `o`ther windows |
| `<space>w` | `w`indow submenu (splits) |

---

## Jumplist

| Key | Description |
|---|---|
| `<C-o>` | jump `o`ut — back in jumplist history |
| `<C-i>` | jump `i`n — forward in jumplist |
| `<space>j` | `j`umplist picker with previews |

---

## LSP — Code Intelligence

| Key | Description |
|---|---|
| `gd` | `g`oto `d`efinition |
| `gr` | `g`oto `r`eferences (every usage) |
| `gi` | `g`oto `i`mplementation of trait / interface |
| `gy` | `g`oto t`y`pe definition |
| `<space>k` | show documentation / hover popup |
| `<space>h` | select all references as multi-selection |
| `<space>s` | document `s`ymbols picker (current buffer) |
| `<space>S` | workspace `S`ymbols picker (project-wide) |
| `<space>a` | code `a`ction — LSP suggested fixes |
| `<space>r` | `r`ename symbol workspace-wide |
| `:lsp-restart` | restart language server |
| `:log-open` | open Helix log to inspect LSP errors |

---

## Diagnostics

| Key | Description |
|---|---|
| `]d` | next `d`iagnostic in buffer (error / warning) |
| `[d` | previous `d`iagnostic in buffer |
| `]D` | first / last `D`iagnostic in buffer |
| `[D` | first `D`iagnostic in buffer |
| `<space>d` | document `d`iagnostics picker (current buffer) |
| `<space>D` | workspace `D`iagnostics picker (whole project dashboard) |

---

## Formatting

| Key | Description |
|---|---|
| `=` | format-range operator on selection |
| `%=` | format whole file (select all then format) |
| `:format` | format entire buffer via active formatter |

---

## Registers

| Key | Description |
|---|---|
| `"ay` | yank into register `a` (named register prefix `"`) |
| `"ap` | paste from register `a` |
| `"+y` / `"+p` | yank / paste system clipboard |
| `"*y` / `"*p` | yank / paste X11 primary selection (Linux) |
| `"_d` | delete into black-hole register (discard) |
| `"` | press and wait — popup lists every register with contents |
| `"/` | last search pattern register (read-only) |
| `":` | last executed command register |
| `"@` | last recorded macro register |
| `".` | current selection contents register |
| `"%` | current file name register |
| `"#` | selection indices register |

---

## Macros

| Key | Description |
|---|---|
| `Q` | toggle macro recording into unnamed register |
| `q` | replay / play last recorded macro |
| `"aQ` | record macro into register `a` |
| `"aq` | replay macro from register `a` |

---

## Clipboard (Space Menu)

| Key | Description |
|---|---|
| `<space>y` | system clipboard `y`ank |
| `<space>p` | system clipboard `p`aste |

---

## Space Menu Top-Level (Language 2 Dictionary)

Press `<space>` and pause for the which-key popup.

| Key | Description |
|---|---|
| `<space>f` | `f`ile picker |
| `<space>F` | `F`ile picker rooted at cwd |
| `<space>b` | `b`uffer picker |
| `<space>j` | `j`umplist picker |
| `<space>s` | document `s`ymbols (LSP) |
| `<space>S` | workspace `S`ymbols (LSP) |
| `<space>d` | document `d`iagnostics |
| `<space>D` | workspace `D`iagnostics |
| `<space>a` | code `a`ction (LSP) |
| `<space>r` | `r`ename symbol (LSP) |
| `<space>h` | select symbol references (LSP) |
| `<space>k` | hover documentation (LSP) |
| `<space>/` | global `/` search across project |
| `<space>'` | resume last picker |
| `<space>w` | `w`indow submenu (splits) |
| `<space>y` / `<space>p` | system clipboard `y`ank / `p`aste |
| `<space>?` | command palette |
