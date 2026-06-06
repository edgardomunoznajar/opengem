# L152 — Keyboard Shortcuts

**Loop**: 152 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The thesis

OPENGEM is a terminal. The user opens the command palette before they touch the mouse. Every shortcut is a chord (single key OR `mod + key`), no triple-modifier wizardry.

`mod` = `Cmd` on macOS, `Ctrl` on Linux/Windows.

## The 20 shortcuts

| # | Chord | Action | Scope |
|---|---|---|---|
| 1 | `mod + k` | Open command palette | Global |
| 2 | `/` | Focus search | Global |
| 3 | `g h` | Go to home | Global (sequential) |
| 4 | `g c` | Go to countries | Global |
| 5 | `g i` | Go to indicators | Global |
| 6 | `g s` | Go to scenarios | Global |
| 7 | `g f` | Go to forecasts | Global |
| 8 | `g l` | Go to leaderboard | Global |
| 9 | `?` | Show shortcut help | Global |
| 10 | `Esc` | Close overlay / blur input | Global |
| 11 | `mod + ,` | Open settings | Global |
| 12 | `mod + d` | Toggle dark / light mode | Global |
| 13 | `mod + b` | Toggle sidebar | Global |
| 14 | `mod + Enter` | Open primary action on focused panel | Panel-scoped |
| 15 | `mod + s` | Save current view to watchlist | View-scoped |
| 16 | `mod + shift + c` | Copy cite-this-view ID | View-scoped |
| 17 | `mod + shift + l` | Copy permalink | View-scoped |
| 18 | `j` / `k` | Next / previous item in feed or list | List-scoped |
| 19 | `[` / `]` | Previous / next vintage | View-scoped |
| 20 | `.` | Open command palette pre-filled with "actions on this view" | View-scoped |

## The `g x` family (go-to)

Sequential chords (vim-style): press `g`, then within 800ms press the target letter. If no second key arrives, `g` is consumed and ignored.

| Chord | Route |
|---|---|
| `g h` | `/` |
| `g c` | `/countries` |
| `g i` | `/indicators` |
| `g s` | `/scenarios` |
| `g f` | `/forecasts` |
| `g l` | `/leaderboard` |
| `g a` | `/accountability` |
| `g m` | `/methodology` |
| `g w` | `/watchlist` |

(`g a`, `g m`, `g w` are bonus three not in the 20 because they're "lazy" — extending the family is cheap.)

## Vintage shortcuts (`[` and `]`)

In any view that has a `vintage` dimension (forecasts, indicators with revisions), `[` moves to the previous vintage, `]` to the next. The URL updates: `?vintage=2026-05-21`. Holding shift jumps by month: `shift + [` is previous month's vintage.

This is the equivalent of Bloomberg's `F11/F12` for going through revisions.

## List navigation (`j` / `k`)

In feeds (news, leaderboard rows, watchlist rows, command palette results), `j` selects next, `k` selects previous. `Enter` opens. `o` opens in new tab (overload of route).

Spacebar pages down (browser default; we don't override).

## Comparison and selection

| Chord | Action |
|---|---|
| `c` | Mark current item for compare |
| `c c` | Open compare-2 with last 2 marked items |
| `x` | Unmark |

So a workflow looks like:
1. On Germany country page: press `c` → "marked Germany"
2. Navigate to France (`g c`, type "France", Enter)
3. Press `c c` → opens compare-2 view of Germany × France

## The "?" help

Press `?` anywhere to open a popover listing the active scope's shortcuts (global + current view-scope). The popover renders the same component used in the settings page (one source of truth).

## Modifier discipline

- No `mod + shift + alt + x` chords. If we need three modifiers, redesign.
- No conflict with browser shortcuts (`mod + t`, `mod + w`, `mod + r`, `mod + l`, `mod + j`, `mod + p`) — these stay native.
- `mod + n` (new) overridden in app pages to open "new alert" — overridden carefully, prompts on first use.
- `mod + f` (find) NOT overridden. Browser's find-in-page is a feature.

## Input field exception

When focus is in a text input, all shortcuts are suppressed except:
- `Esc` (blur the input)
- `mod + s` (save — explicit feature)
- `mod + Enter` (submit form)

The user expects to type freely. We don't fight that.

## Discoverability

1. Every icon-only button has a tooltip with the shortcut, e.g., `Search (/)`.
2. The command palette (L153) lists every action with its shortcut on the right side.
3. The `?` help popover lists all shortcuts grouped by scope.
4. On first visit, a brief banner: "Press / to search, ⌘K to open the command palette."

## Customization (deferred)

V1: shortcuts are fixed. Customization is a paid-tier feature (settings → keyboard) in V2. Most users never customize. Power users complain loudly, but they get a free-tier `key-overrides.json` that they can paste into their browser localStorage (undocumented but stable).

## Accessibility

- Every shortcut has a menu equivalent (no keyboard-only actions).
- Sequential chords work for users who can't hold modifiers.
- Screen reader announces shortcut on focus via `aria-keyshortcuts`.

## Conflicts to watch

- macOS Spotlight: `cmd + space`. Not used by us.
- Browser bookmark bar: `cmd + shift + b`. Not used by us.
- Chrome devtools: `cmd + opt + i`. Not used by us.
- VoiceOver: `ctrl + opt + arrow`. Not used by us.

We checked the conflict matrix in three browsers × two OSes.

## Implementation

Library: `react-hotkeys-hook` for declarative bindings, with a custom scope provider that respects input focus and overlay state.

```ts
useHotkeys('mod+k', openPalette, { scope: 'global' })
useHotkeys('g>c', goToCountries, { scope: 'global', sequence: true })
useHotkeys('mod+s', saveView, { scope: 'view', enableOnFormTags: ['INPUT'] })
```

A central `shortcuts.ts` registry exports the canonical list, used by:
- The `?` help popover
- The command palette right-rail render
- Tooltips on icon buttons
- The settings page

One source of truth. If a chord changes, every surface updates.

## The five we explicitly rejected

| Reject | Why |
|---|---|
| Single-letter `s` for save | Conflicts with input focus norm; would surprise |
| `shift + ?` | Just use `?` (no modifier — already accessible via `shift+/` on QWERTY) |
| `mod + arrow` for navigation | Conflicts with macOS workspaces |
| `tab` for next field | Browser owns; never override |
| `space` for open | Browser owns scroll; never override |

## The terminal feel, summarized

A power user opens OPENGEM, presses `g f`, lands on forecasts, presses `/`, types "USA CPI Q3," hits enter, lands on the forecast page, presses `[` four times to walk through the last four vintages, presses `c`, navigates to "EUR CPI Q3," presses `c c`, lands in the compare view. They have not touched the mouse. That is the bar.
