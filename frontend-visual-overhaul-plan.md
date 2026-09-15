# Frontend Visual Overhaul Plan

## Goal
Transform the existing functional-but-plain React dashboard into a polished,
production-quality UI suitable for hackathon judges. No backend changes, no data
schema changes, no new features — pure visual uplift only.

## Scope
All files live under `src/frontend/src/`. The plan introduces a shared design
system (CSS classes + CSS variables), reusable component primitives, and upgrades
every page. No third-party UI libraries are added — only vanilla CSS and the
existing React + Vite stack.

## Status
[x] complete

---

## Sub-Task 1 — Design System Foundation

**Intent**
Replace the broken, disconnected `index.css` / `App.css` with a single, coherent
design-system stylesheet that every component will consume. All hardcoded hex
colours currently scattered across inline styles get replaced by CSS custom
properties. The `#root` centering and width constraints that fight the table
layouts are fixed here.

**Expected Outcomes**
- One file, `src/styles/design-system.css`, defines all tokens and utility classes.
- `index.css` is reset to a clean base (margin, box-sizing, font stack only).
- `App.css` is cleared of dead Vite scaffold styles.
- No visual change yet — this is the token/class foundation.

**Todo List**
1. Create `src/frontend/src/styles/design-system.css` with:
   - Color tokens: `--color-navy`, `--color-red`, `--color-orange`,
     `--color-blue`, `--color-purple`, `--color-green`, `--color-bg`,
     `--color-surface`, `--color-border`, `--color-text`, `--color-text-muted`
   - Spacing scale tokens: `--space-1` through `--space-8`
   - Shadow tokens: `--shadow-sm`, `--shadow-md`
   - Border radius token: `--radius`
   - Utility classes: `.badge`, `.badge--red`, `.badge--orange`, `.badge--blue`,
     `.badge--purple`, `.badge--green`, `.badge--grey`, `.badge--yellow`
   - Table classes: `.data-table`, `.data-table thead tr`,
     `.data-table tbody tr`, `.data-table tbody tr:hover`, `.data-table td`,
     `.data-table th`
   - Card classes: `.stat-card`, `.stat-card__value`, `.stat-card__label`
   - Skeleton loader class: `.skeleton`, `@keyframes shimmer`
   - Expandable row highlight: `.row-expanded`
2. Rewrite `index.css` to base reset only (body margin, box-sizing, font stack).
3. Clear `App.css` of all Vite scaffold content; leave the file empty or minimal.
4. Import `design-system.css` in `main.jsx`.

**Relevant Context**
- `src/frontend/src/index.css` — current file, has `#root` width/centering that
  breaks tables; must be removed.
- `src/frontend/src/App.css` — dead Vite scaffold styles, safe to clear.
- `src/frontend/src/main.jsx` — entry point, add the new CSS import here.

**Status** [x] done

---

## Sub-Task 2 — App Shell and Header Redesign

**Intent**
Replace the plain dark `<div>` header and bare tab bar in `App.jsx` with an
IBM-inspired navy header that includes a logo mark, product name, and subtitle.
Upgrade the tab bar to use proper CSS classes with smooth active-tab indicator
transitions.

**Expected Outcomes**
- Header shows a small ship/anchor logo mark (SVG inline), bold product name,
  and "Powered by IBM Bob · watsonx.ai" subtitle with subtle opacity.
- Tab bar has hover states, smooth underline transition on active tab.
- Overall shell uses `--color-bg` and `--color-surface` tokens, not hardcoded hex.
- Page content area has correct `max-width` and padding from tokens.

**Todo List**
1. In `App.jsx`, replace the inline-styled header `<div>` with a semantic
   `<header>` element using a CSS class `app-header`.
2. Add `app-header` styles in `design-system.css`: navy background
   (`--color-navy`), flex layout, padding from spacing tokens, bottom border.
3. Add a simple inline SVG logo mark (⛴ or a minimal chain-link icon in SVG)
   to the left of the title text.
4. Replace inline tab bar styles with `.tab-bar`, `.tab-bar__item`,
   `.tab-bar__item--active` CSS classes defined in `design-system.css`.
5. Keep the same 5 tab IDs and labels — only styling changes.
6. Wrap the page content in a `<main>` with class `page-content` for consistent
   padding and max-width.

**Relevant Context**
- `src/frontend/src/App.jsx` — the only file changed in this sub-task.
- Existing tab state logic (`useState`, `TABS`, `PAGES`) stays untouched.

**Status** [x] done

---

## Sub-Task 3 — Dashboard Overview Page

**Intent**
Upgrade the 4 summary stat cards from plain colored `<div>` boxes to polished
stat cards with an icon, large number, label, and subtle shadow. Add a skeleton
loader while data is fetching instead of no visual feedback.

**Expected Outcomes**
- 4 stat cards use `.stat-card` class, show a relevant emoji/icon, value in large
  bold type, label below, with `--shadow-sm` and `--radius`.
- While loading, 4 skeleton placeholder cards are shown using `.skeleton` class
  (shimmer animation).
- Cards use colour tokens, not hardcoded hex strings.
- Descriptive sub-paragraph below the cards is styled with `--color-text-muted`.

**Todo List**
1. Create a `StatCard` component inline in `Dashboard.jsx` (or as a small
   function component) that accepts `icon`, `value`, `label`, `colorVar` props
   and renders a `.stat-card`.
2. Create a `SkeletonCard` component that renders a `.skeleton` block of the
   same dimensions as a stat card.
3. In the `useEffect`, show 4 `SkeletonCard`s while the 3 parallel API calls
   are in flight; replace with real `StatCard`s on resolution.
4. Use icons: 🚨 Affected Shipments, 🚛 Idle Fleet Assets, 🌡 Cold Chain Alerts,
   ⚠️ Critical Excursions.
5. Replace all hardcoded hex colours with the appropriate CSS variable.

**Relevant Context**
- `src/frontend/src/pages/Dashboard.jsx` — only file changed here.
- API calls (`getImpact`, `getFleetIdle`, `getColdChain`) stay identical.

**Status** [x] done

---

## Sub-Task 4 — Disruptions Page

**Intent**
Replace the plain HTML table with the styled `.data-table` class (hover states,
alternating subtle background on critical rows, sticky header). Polish the
severity score into a coloured badge-style chip. Improve the inline reroute
expansion row to look like a proper panel, not a raw colspan cell.

**Expected Outcomes**
- Table uses `.data-table` class — hover highlight, `--color-border` borders,
  proper `--color-surface` header row.
- Severity score rendered as a coloured pill badge (`--color-red` for ≥8,
  `--color-orange` for ≥5, `--color-green` otherwise) using `.badge` class.
- Priority badge uses `.badge--red` for high, `.badge--grey` for normal.
- "Reroute" button styled with proper button class (`.btn`, `.btn--primary`).
- Loading state shows a skeleton table (3 placeholder rows).
- Reroute expansion row has a card-style container with a subtle left border in
  `--color-blue`, numbered options clearly separated.

**Todo List**
1. Add `.btn`, `.btn--primary`, `.btn--sm` utility classes to `design-system.css`.
2. In `Disruptions.jsx`, replace all inline `style={}` on `<table>`, `<thead>`,
   `<tbody>`, `<tr>`, `<th>`, `<td>` with `.data-table` class.
3. Replace the inline badge `<span>` functions with the `.badge` utility classes.
4. Replace the Reroute `<button>` inline styles with `.btn .btn--primary .btn--sm`.
5. Add a `SkeletonTable` helper (3 rows, 8 columns of `.skeleton` cells) shown
   while `loading === true`.
6. Style the reroute expansion row: add class `row-expanded`, wrap content in a
   `.reroute-panel` div with left border and padding.
7. Add `.reroute-panel` styles to `design-system.css`.

**Relevant Context**
- `src/frontend/src/pages/Disruptions.jsx` — only file changed here.
- `reroute()` API call and state logic stay identical.

**Status** [x] done

---

## Sub-Task 5 — Fleet Assets Page

**Intent**
Upgrade the Fleet page table using `.data-table`, improve the asset-type badge
colours using CSS classes instead of inline `typeColor` lookup, and style the
region filter dropdown.

**Expected Outcomes**
- Table uses `.data-table` class consistently with all other pages.
- Asset type badges use `.badge--blue` (truck), `.badge--purple` (reefer),
  `.badge--green` (vessel), `.badge--orange` (container) CSS classes.
- "⚠ Yes" near-disruption indicator styled as `.badge--red`, "No" as
  `.badge--green`.
- Region filter `<select>` styled with `.select` CSS class (border, padding,
  radius, focus ring).
- Loading shows skeleton table.

**Todo List**
1. Add `.select` class to `design-system.css`.
2. In `Fleet.jsx`, remove the `typeColor` object and inline badge function.
   Map asset types to badge class names with a plain lookup object.
3. Replace table inline styles with `.data-table`.
4. Replace near-disruption inline spans with `.badge--red` / `.badge--green`.
5. Add skeleton loader (same pattern as other pages).
6. Style the filter row (flex, gap, align-items) using `design-system.css` tokens.

**Relevant Context**
- `src/frontend/src/pages/Fleet.jsx` — only file changed here.
- API call and region filter state logic stay identical.

**Status** [x] done

---

## Sub-Task 6 — Cold Chain Page

**Intent**
The Cold Chain page is the highest-stakes feature (the team's proudest feature per
README). It should look the part. Upgrade the summary counters into proper stat
cards (same as Dashboard), polish the severity badge, highlight critical rows with
a full left-border accent, and make the action text readable in a constrained
column.

**Expected Outcomes**
- Summary counter row uses `.stat-card` components matching the Dashboard style.
- Severity badge uses `.badge` CSS class: `.badge--red` for CRITICAL,
  `.badge--orange` for REPORTABLE BREACH, `.badge--yellow` for MINOR DEVIATION.
- CRITICAL rows have a `2px solid --color-red` left border on the first `<td>`.
- "Recommended Action" column text is clearly readable, wraps cleanly, uses
  `--color-text-muted`.
- Excursion temp column value is bold red using `--color-red`.
- Loading shows a skeleton table.

**Todo List**
1. In `ColdChain.jsx`, replace the 3 inline counter `<div>`s with `StatCard`
   components (import the same StatCard pattern used in Dashboard).
2. Replace the inline `badge()` function with `.badge` CSS class names.
3. Replace all table inline styles with `.data-table`.
4. Add left-border critical row logic: apply a CSS class `row--critical` to `<tr>`
   elements where `severity === 'CRITICAL'`; define `row--critical td:first-child`
   in `design-system.css` with a red left border.
5. Add skeleton loader.
6. Remove `severityColor` / `severityTextColor` objects; use CSS classes instead.

**Relevant Context**
- `src/frontend/src/pages/ColdChain.jsx` — only file changed here.
- `StatCard` logic must be importable or duplicated consistently across Dashboard
  and ColdChain — consider extracting it to
  `src/frontend/src/components/StatCard.jsx` if it's needed in both.

**Status** [x] done

---

## Sub-Task 7 — Assistant Chat Page

**Intent**
The Assistant page chat UI looks like a plain bulletin board. Upgrade it to a
modern chat interface: distinct bubble shapes for user vs. assistant, a proper
input bar styled like a chat composer, suggestion chips with hover states, and a
typing indicator animation while the agent is responding.

**Expected Outcomes**
- User messages: right-aligned bubble, `--color-blue` accent, white background.
- Assistant messages: left-aligned bubble, `--color-purple` accent,
  `--color-surface` background.
- "Tools used / summary" meta line styled as a tiny muted footer inside the
  assistant bubble.
- Suggestion chips have hover fill (background shifts to `--color-blue` with
  white text on hover).
- Input bar has a visible focus ring and send button styled with `.btn--primary`.
- Loading state shows a "typing" indicator (3-dot pulse animation) inside an
  assistant bubble, not a plain `<p>`.
- Add typing indicator `@keyframes` to `design-system.css`.

**Todo List**
1. Add chat-specific CSS classes to `design-system.css`: `.chat-history`,
   `.chat-bubble`, `.chat-bubble--user`, `.chat-bubble--assistant`,
   `.chat-meta`, `.chat-input-bar`, `.suggestion-chip`, `.typing-indicator`.
2. In `Assistant.jsx`, replace all inline styles with these classes.
3. User bubble: `align-self: flex-end`, blue left border removed, right-side
   placement via flex column + align-self.
4. Assistant bubble: `align-self: flex-start`, purple left border.
5. Replace `{loading && <div>Analysing...</div>}` with a `.typing-indicator`
   element (3 animated dots using CSS animation).
6. Style suggestion chips: border, rounded pill shape, hover fill transition.
7. Wrap input and button in `.chat-input-bar` for proper flex layout.

**Relevant Context**
- `src/frontend/src/pages/Assistant.jsx` — only file changed here.
- State logic, API call, suggestion array all stay identical.

**Status** [x] done

---

## Sub-Task 8 — Extract Shared StatCard Component

**Intent**
Both Dashboard and ColdChain use the same StatCard pattern. Rather than
duplicating the component, extract it to a shared file so both pages import it
from one source.

**Expected Outcomes**
- `src/frontend/src/components/StatCard.jsx` exists and exports a `StatCard`
  component accepting `icon`, `value`, `label`, `colorClass` props.
- `Dashboard.jsx` and `ColdChain.jsx` import from this shared file.
- No logic duplication.

**Todo List**
1. Create `src/frontend/src/components/StatCard.jsx` with the `StatCard`
   component.
2. Update `Dashboard.jsx` to import `StatCard` from `../components/StatCard`.
3. Update `ColdChain.jsx` to import `StatCard` from `../components/StatCard`.
4. Remove any inline `StatCard` definitions from both page files.

**Note** — This sub-task should be done AFTER Sub-Tasks 3 and 6, once both
implementations are stable, to avoid working against moving targets.

**Relevant Context**
- `src/frontend/src/pages/Dashboard.jsx`
- `src/frontend/src/pages/ColdChain.jsx`
- New file: `src/frontend/src/components/StatCard.jsx`

**Status** [x] done

---

## Implementation Order

```
Sub-Task 1  →  Sub-Task 2  →  Sub-Task 3  →  Sub-Task 4
                                                    ↓
                              Sub-Task 8  ←  Sub-Task 5
                                    ↑
                              Sub-Task 6  →  Sub-Task 7
```

Sub-Task 1 must go first — all other sub-tasks depend on the CSS classes it
defines. Sub-Task 2 can follow immediately. Sub-Tasks 3–7 can be done in any
order after that. Sub-Task 8 consolidates shared components and should be last.
