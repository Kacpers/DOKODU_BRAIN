# Plan 5: UX Framework Refresh — Drawer + Multi-View + Filter Gallery

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development.

**Goal:** Implement the second WOW factor from spec — Trello-like UX patterns: drawer-not-page entity details, multi-view per board (Kanban/List/Calendar/Timeline), filter gallery (tab strip + saved views + smart auto-suggest).

**Architecture:**
- **Drawer pattern**: clicking an entity (Deal, Company, Contact) slides drawer from right (~50% width). User retains list context. Replaces current "navigate to /deals/[id]" full-page pattern.
- **Multi-view**: every list page (Pipeline, Companies, Deals, Tasks, Projects) gets toggleable views — Kanban (drag-drop), List (sortable table), Calendar (date-based), Timeline (Gantt for projects/milestones).
- **Filter gallery**: 3 levels — tab strip above list (most-used filters as tabs), sidebar expand under entity name (pinned views), settings page (manage all + share with team). Plus smart auto-suggest after 3× same filter combo.

**Tech:** Existing shadcn/ui (Dialog, Tabs, Table, etc.) + react-day-picker (already in deps for calendar) + dnd-kit (already in deps for kanban). No new libs.

---

## Files

### Created
- `src/components/drawer/entity-drawer.tsx` — generic right-side drawer
- `src/components/drawer/deal-drawer-content.tsx` — Deal-specific content
- `src/components/drawer/company-drawer-content.tsx`
- `src/components/drawer/contact-drawer-content.tsx`
- `src/components/views/view-switcher.tsx` — Kanban/List/Calendar/Timeline toggle
- `src/components/views/calendar-view.tsx` — generic calendar view for any entity with date field
- `src/components/views/timeline-view.tsx` — Gantt-style for projects/milestones
- `src/components/filters/filter-tab-strip.tsx` — tabs above list
- `src/components/filters/saved-views-sidebar.tsx` — pinned views in sidebar
- `src/components/filters/saved-views-manager.tsx` — settings page
- `src/components/filters/filter-suggester.tsx` — smart auto-suggest after 3× same combo
- `src/lib/use-saved-views.ts` — hook for managing saved views (URL-encoded + persisted via API)
- `src/app/api/saved-views/route.ts` — CRUD for saved views
- `prisma/schema-additions.prisma` — `SavedView` model addition

### Modified
- `src/app/(app)/pipeline/page.tsx` — switch to view-switcher pattern, drawer-not-page
- `src/app/(app)/companies/company-list.tsx` — same
- `src/app/(app)/deals/page.tsx` — same
- `src/app/(app)/tasks/page.tsx` — same
- `src/app/(app)/projects/page.tsx` — add timeline view
- `src/app/(app)/deals/[id]/page.tsx` — keep as fallback for direct URL, but main flow uses drawer

---

## Tasks (high-level only — full task spec in implementation session)

### Phase A: Drawer infrastructure (~3 days)
1. EntityDrawer base component with shadcn Sheet
2. URL state sync (open drawer reflects in `?drawer=deal:abc123`)
3. Deal/Company/Contact drawer content (read-only first, editable second)
4. Replace navigation in list pages with drawer trigger

### Phase B: Multi-view (~3-4 days)
5. ViewSwitcher component (4 modes)
6. Calendar view (entity with `dueDate` or similar field)
7. Timeline view (projects + milestones)
8. List view = enhanced table with sortable columns + density modes
9. Kanban already exists, refactor to use shared interfaces

### Phase C: Filter gallery (~2-3 days)
10. SavedView Prisma model + migration
11. /api/saved-views CRUD
12. URL-shareable filter encoding (existing pattern but expand)
13. Tab strip component
14. Sidebar pinned views
15. Settings management UI
16. Smart auto-suggest (`useFilterTracking` hook)

### Phase D: Polish + testing (~2 days)
17. Animation tuning (drawer slide, view transitions)
18. Mobile responsive (drawer becomes full-screen on small screens)
19. Keyboard navigation (Tab, Esc, Cmd+/ to toggle filters)
20. Component tests (Vitest + Testing Library)

**Total estimate:** 10-12 days

---

## Out of scope (later)

- Custom user-created views with their own SQL (just predefined "smart filters" for now)
- Cross-board views ("show all hot stuff" merging deals + tasks + meetings)
- AI-suggested views ("you usually look at Q2 hot deals on Monday — want to pin?")
- Real-time updates (websocket sync when others change view)

---

## Open questions

- Drawer width: 50% (current spec) vs adaptive (50% on wide, 80% on tablet)?
- Calendar view granularity: month default? Or week?
- Timeline view: should milestones be draggable to reschedule? Risky — typo + drag could shift project plan.
- Saved views: per-user only, or "team views" too? Spec says both — start with per-user, add team later.
