# TikTok Explainer Scenes — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a library of 6 reusable Remotion scene compositions + transition system + JSON-driven pipeline that renders TikTok explainer reels without recording.

**Architecture:** ExplainerVideo root reads a JSON scenario → renders a `<Series>` of scene components with animated transitions → outputs MP4 (1080x1920, 30fps, no audio). Each scene is a standalone Remotion component with configurable props and built-in enter/exit animations. A Lookbook composition showcases all scenes for visual approval.

**Tech Stack:** Remotion 4.0.237, React 18, TypeScript, existing `tiktok-theme.ts`, `tiktok_pipeline.py` (Python CLI extension)

**Spec:** `docs/superpowers/specs/2026-04-16-tiktok-explainer-scenes-design.md`

---

## File Structure

```
remotion/src/compositions/TikTok/Explainer/
├── ExplainerVideo.tsx          — root composition, reads JSON inputProps, renders Series
├── scenes/
│   ├── KineticText.tsx         — animated keywords with emphasis highlighting
│   ├── SlideCard.tsx           — card with icon + title + staggered bullets
│   ├── ScreenMockup.tsx        — animated screenshot in phone/monitor frame
│   ├── StatCounter.tsx         — counting number animation with label
│   ├── VSCompare.tsx           — two-column side-by-side comparison
│   └── CTACard.tsx             — Dokodu branded CTA ending
├── transitions/
│   └── TransitionWrapper.tsx   — wraps each scene with enter/exit transition
└── Lookbook.tsx                — demo reel of all scenes + transitions

remotion/src/Root.tsx                  — MODIFY: register ExplainerVideo + Lookbook compositions
scripts/tiktok_pipeline.py             — MODIFY: add `explainer` and `lookbook` CLI commands
tiktok_publish/scenarios/              — CREATE: directory for JSON scenario files
tiktok_publish/scenarios/lookbook.json — CREATE: sample scenario for testing
```

---

### Task 1: TransitionWrapper component

**Files:**
- Create: `remotion/src/compositions/TikTok/Explainer/transitions/TransitionWrapper.tsx`

This wraps any child scene with enter/exit animations. Supports 5 transition types.

- [ ] **Step 1: Create TransitionWrapper.tsx**

```tsx
// TransitionWrapper.tsx
// Props: type ("glitch"|"swipeUp"|"zoom"|"cut"|"dissolve"), durationInFrames, children
// Enter animation: first 15 frames
// Exit animation: last 10 frames
// Middle: children rendered at full opacity
```

Implementation details:
- `glitch`: RGB channel offset (translateX on 3 overlapping layers with mix-blend-mode) for 3 frames, then snap to normal
- `swipeUp`: translateY from 100% to 0 (spring, damping: 12)
- `zoom`: scale from 1.5 to 1.0 with opacity fade-in
- `cut`: no animation, instant appear/disappear
- `dissolve`: simple opacity interpolate 0→1 enter, 1→0 exit

- [ ] **Step 2: Verify it renders in Remotion Studio**

```bash
cd /home/kacper/DOKODU_BRAIN/remotion && npx remotion studio
```

Open browser, check that TransitionWrapper doesn't error (will test properly with scenes later).

- [ ] **Step 3: Commit**

```bash
git add remotion/src/compositions/TikTok/Explainer/transitions/TransitionWrapper.tsx
git commit -m "feat(tiktok): add TransitionWrapper with 5 transition types"
```

---

### Task 2: KineticText scene

**Files:**
- Create: `remotion/src/compositions/TikTok/Explainer/scenes/KineticText.tsx`

Animated text with word-by-word spring entrance and emphasis pulse on a key word.

- [ ] **Step 1: Create KineticText.tsx**

Props interface:
```tsx
interface KineticTextProps {
  text: string;           // Full text, can contain \n for line breaks
  emphasis?: string;      // Word to highlight (accent color + scale pulse)
  fontSize?: number;      // Default: 72
  layout?: "center" | "stack";  // center = all centered, stack = words stacked vertically
}
```

Animation behavior:
- Split text into words
- Each word flies in with `spring()` (stagger: 4 frames between words, damping: 12)
- Emphasized word gets: `tiktokTheme.colors.accent` color + scale pulse (1.0 → 1.15 → 1.0)
- Background: `tiktokTheme.colors.bg` (black)
- Font: Inter Bold (already loaded via `@remotion/google-fonts/Inter`)
- Exit: all words scale down to 0.8 + fade out in last 10 frames

- [ ] **Step 2: Commit**

```bash
git add remotion/src/compositions/TikTok/Explainer/scenes/KineticText.tsx
git commit -m "feat(tiktok): add KineticText scene component"
```

---

### Task 3: SlideCard scene

**Files:**
- Create: `remotion/src/compositions/TikTok/Explainer/scenes/SlideCard.tsx`

Card with title, optional icon emoji, and bullet points that appear with stagger.

- [ ] **Step 1: Create SlideCard.tsx**

Props interface:
```tsx
interface SlideCardProps {
  title: string;
  icon?: string;           // Emoji or text icon
  bullets: string[];       // 2-5 bullet points
  accentColor?: string;    // Override accent color
}
```

Animation behavior:
- Card: rounded rect (`bgCard` color), slides up from bottom with spring (damping: 14)
- Icon: scale bounce on appear (spring, delay 5 frames)
- Title: fade + translateY (spring, delay 8 frames)
- Bullets: each fades in + slides from right, stagger 8 frames apart
- Bullet marker: small accent-colored circle
- Exit: card slides down

- [ ] **Step 2: Commit**

```bash
git add remotion/src/compositions/TikTok/Explainer/scenes/SlideCard.tsx
git commit -m "feat(tiktok): add SlideCard scene component"
```

---

### Task 4: StatCounter scene

**Files:**
- Create: `remotion/src/compositions/TikTok/Explainer/scenes/StatCounter.tsx`

Big animated number counting from 0 (or a start value) to target, with label.

- [ ] **Step 1: Create StatCounter.tsx**

Props interface:
```tsx
interface StatCounterProps {
  value: number;          // Target number (e.g. 200)
  from?: number;          // Start value (default: 0)
  label: string;          // e.g. "maili dziennie"
  suffix?: string;        // e.g. "h", "%", "x"
  prefix?: string;        // e.g. "$", "+"
}
```

Animation behavior:
- Number: interpolate from `from` to `value` over 70% of duration (easeOut)
- Font: Inter Black, fontSize 160
- Color: accent (green)
- Label below: Inter, fontSize 40, gray, fades in at 30% mark
- On reaching target: brief scale pulse (1.0 → 1.1 → 1.0)
- Exit: smash zoom (scale 1.0 → 3.0) + opacity fade

- [ ] **Step 2: Commit**

```bash
git add remotion/src/compositions/TikTok/Explainer/scenes/StatCounter.tsx
git commit -m "feat(tiktok): add StatCounter scene component"
```

---

### Task 5: VSCompare scene

**Files:**
- Create: `remotion/src/compositions/TikTok/Explainer/scenes/VSCompare.tsx`

Two-column comparison with "VS" badge in the middle.

- [ ] **Step 1: Create VSCompare.tsx**

Props interface:
```tsx
interface VSCompareProps {
  left: { title: string; points: string[]; color?: string };
  right: { title: string; points: string[]; color?: string };
  vsText?: string;        // Default: "VS"
}
```

Animation behavior:
- Left column: slides in from left edge (spring, damping: 12)
- Right column: slides in from right edge (spring, damping: 12, delay 3 frames)
- "VS" badge: scale bounce in center (spring, delay 10 frames), accent bg, round
- Points in each column: stagger fade-in (8 frames apart), bullet = colored dot
- Divider line: height animates from 0 to full (interpolate, concurrent with columns)
- Exit: columns slide apart (left→left, right→right)

- [ ] **Step 2: Commit**

```bash
git add remotion/src/compositions/TikTok/Explainer/scenes/VSCompare.tsx
git commit -m "feat(tiktok): add VSCompare scene component"
```

---

### Task 6: ScreenMockup scene

**Files:**
- Create: `remotion/src/compositions/TikTok/Explainer/scenes/ScreenMockup.tsx`

Animated mockup of a screen/phone with content inside.

- [ ] **Step 1: Create ScreenMockup.tsx**

Props interface:
```tsx
interface ScreenMockupProps {
  device: "phone" | "monitor" | "browser";
  title?: string;          // Text shown "on screen"
  lines?: string[];        // Lines of text/code shown inside
  highlightLine?: number;  // Which line to highlight
}
```

Animation behavior:
- Device frame: fade in + slight scale (0.95→1.0) with spring
- "Screen on" effect: inner area opacity 0→1 with slight delay (like screen powering on)
- Lines of text: typing effect (characters appear left-to-right, 2 chars/frame)
- Highlighted line: accent background color pulse
- Phone frame: rounded rect with notch at top
- Monitor frame: rect with stand at bottom
- Browser frame: rect with URL bar at top (3 colored dots + gray bar)
- Exit: frame slides up and off screen

- [ ] **Step 2: Commit**

```bash
git add remotion/src/compositions/TikTok/Explainer/scenes/ScreenMockup.tsx
git commit -m "feat(tiktok): add ScreenMockup scene component"
```

---

### Task 7: CTACard scene

**Files:**
- Create: `remotion/src/compositions/TikTok/Explainer/scenes/CTACard.tsx`

Dokodu-branded ending card. Different from existing TikTokCTA — this one is for explainers (no talking head context).

- [ ] **Step 1: Create CTACard.tsx**

Props interface:
```tsx
interface CTACardProps {
  text?: string;           // CTA text, default: "Obserwuj po więcej"
  handle?: string;         // Default: "@kacpersieradzinski"
  showLogo?: boolean;      // Default: true
}
```

Animation behavior:
- Background: subtle gradient (dark → slightly lighter, animated angle rotation)
- "DOKODU" text or accent line: drops from top with spring bounce
- CTA text: fades in + scale from 0.9→1.0
- Handle: fades in below with delay
- Arrow: bouncing animation pointing down (like existing TikTokCTA)
- No exit animation (last scene, holds)

- [ ] **Step 2: Commit**

```bash
git add remotion/src/compositions/TikTok/Explainer/scenes/CTACard.tsx
git commit -m "feat(tiktok): add CTACard scene component"
```

---

### Task 8: ExplainerVideo root composition

**Files:**
- Create: `remotion/src/compositions/TikTok/Explainer/ExplainerVideo.tsx`

Root composition that reads JSON inputProps and assembles scenes into a `<Series>`.

- [ ] **Step 1: Create ExplainerVideo.tsx**

```tsx
// Props: { scenes: SceneConfig[] }
// where SceneConfig = { type: string, duration?: number, transition?: string, ...sceneProps }
//
// Logic:
// 1. Map each scene config to the correct component (KineticText, SlideCard, etc.)
// 2. Use Remotion <Series> to sequence them
// 3. Wrap each in <TransitionWrapper> with the specified transition type
// 4. Default transition rotation: swipeUp → zoom → dissolve → swipeUp → ...
// 5. Default durations per scene type (in seconds): KineticText=3, SlideCard=5, ScreenMockup=6, StatCounter=4, VSCompare=7, CTACard=3
// 6. Calculate total durationInFrames = sum of all scene durations * fps
```

Scene registry map:
```tsx
const SCENES = {
  KineticText,
  SlideCard,
  ScreenMockup,
  StatCounter,
  VSCompare,
  CTACard,
} as const;

const DEFAULT_DURATIONS: Record<string, number> = {
  KineticText: 3,
  SlideCard: 5,
  ScreenMockup: 6,
  StatCounter: 4,
  VSCompare: 7,
  CTACard: 3,
};

const TRANSITION_ROTATION = ["swipeUp", "zoom", "dissolve", "glitch", "cut"];
```

- [ ] **Step 2: Commit**

```bash
git add remotion/src/compositions/TikTok/Explainer/ExplainerVideo.tsx
git commit -m "feat(tiktok): add ExplainerVideo root composition with Series assembly"
```

---

### Task 9: Lookbook composition

**Files:**
- Create: `remotion/src/compositions/TikTok/Explainer/Lookbook.tsx`

Demo reel showing every scene with every transition. For Kacper's visual approval.

- [ ] **Step 1: Create Lookbook.tsx**

Structure (~90s total):
```
Section 1: KineticText × 3 variants (different text, layouts, transitions)  ~9s
Section 2: SlideCard × 2 variants                                          ~10s
Section 3: StatCounter × 2 variants                                        ~8s
Section 4: VSCompare × 2 variants                                          ~14s
Section 5: ScreenMockup × 2 variants (phone + browser)                     ~12s
Section 6: CTACard × 1                                                     ~3s
Section 7: Full example explainer (T-033 ChatGPT vs Claude vs Gemini)       ~30s
```

Uses ExplainerVideo internally for Section 7 (proves the full pipeline works).

- [ ] **Step 2: Commit**

```bash
git add remotion/src/compositions/TikTok/Explainer/Lookbook.tsx
git commit -m "feat(tiktok): add Lookbook demo reel composition"
```

---

### Task 10: Register compositions in Root.tsx

**Files:**
- Modify: `remotion/src/Root.tsx`

- [ ] **Step 1: Add imports and Composition entries**

Add to Root.tsx:
- Import `ExplainerVideo` and `Lookbook`
- Add `<Composition>` for `TikTok-Explainer` (dynamic duration via `calculateMetadata`)
- Add `<Composition>` for `TikTok-Lookbook` (fixed duration for demo reel)
- Default props for TikTok-Explainer: sample T-033 scenario JSON

- [ ] **Step 2: Test in Remotion Studio**

```bash
cd /home/kacper/DOKODU_BRAIN/remotion && npx remotion studio
```

Open browser → verify both `TikTok-Explainer` and `TikTok-Lookbook` appear in sidebar and render without errors.

- [ ] **Step 3: Commit**

```bash
git add remotion/src/Root.tsx
git commit -m "feat(tiktok): register ExplainerVideo and Lookbook in Root"
```

---

### Task 11: Render test lookbook MP4

**Files:**
- Create: `tiktok_publish/scenarios/lookbook.json` (sample scenario for the full example in Lookbook Section 7)

- [ ] **Step 1: Create sample scenario JSON**

```json
{
  "id": "T-033",
  "title": "ChatGPT vs Claude vs Gemini",
  "scenes": [
    { "type": "KineticText", "text": "Który AI\nwybrać?", "emphasis": "wybrać", "duration": 3 },
    { "type": "VSCompare", "left": { "title": "ChatGPT", "points": ["Obrazy", "Browsing", "Popularność"] }, "right": { "title": "Claude", "points": ["Dokumenty", "Kod", "Analiza"] }, "duration": 8 },
    { "type": "SlideCard", "title": "Gemini", "icon": "🔍", "bullets": ["Google ekosystem", "Duży kontekst", "Integracja z Workspace"], "duration": 5 },
    { "type": "StatCounter", "value": 3, "label": "narzędzia, 3 różne zastosowania", "duration": 4 },
    { "type": "KineticText", "text": "Nie który lepszy.\nKtóry do CZEGO.", "emphasis": "CZEGO", "duration": 4, "transition": "glitch" },
    { "type": "CTACard", "duration": 3 }
  ]
}
```

- [ ] **Step 2: Render the lookbook**

```bash
cd /home/kacper/DOKODU_BRAIN/remotion && npx remotion render TikTok-Lookbook --output ../tiktok_publish/lookbook.mp4
```

- [ ] **Step 3: Verify output**

Check file exists and is reasonable size:
```bash
ls -lh /home/kacper/DOKODU_BRAIN/tiktok_publish/lookbook.mp4
```

- [ ] **Step 4: Commit**

```bash
git add tiktok_publish/scenarios/lookbook.json
git commit -m "feat(tiktok): render lookbook demo reel for visual approval"
```

---

### Task 12: Pipeline CLI extension (explainer command)

**Files:**
- Modify: `scripts/tiktok_pipeline.py`

- [ ] **Step 1: Add `explainer` subcommand**

Add to CLI after the `scenarios` subparser:

```python
# explainer — render explainer from JSON scenario
p_exp = subparsers.add_parser("explainer", help="Renderuj explainera z JSON scenariusza")
p_exp.add_argument("scenario", type=Path, help="Ścieżka do pliku JSON scenariusza")
p_exp.add_argument("--output", "-o", type=Path, default=TIKTOK_DIR)
```

Add handler function `render_explainer(scenario_path, output_dir)`:
1. Read and validate JSON
2. Call `npx remotion render TikTok-Explainer --output <path> --props <json>`
3. Generate description + hashtags from scenario title
4. Save to `tiktok_publish/<id>/`

- [ ] **Step 2: Add `lookbook` subcommand**

```python
p_look = subparsers.add_parser("lookbook", help="Renderuj lookbook (katalog scen)")
p_look.add_argument("--output", "-o", type=Path, default=TIKTOK_DIR / "lookbook.mp4")
```

Handler: calls `npx remotion render TikTok-Lookbook --output <path>`

- [ ] **Step 3: Test CLI**

```bash
cd /home/kacper/DOKODU_BRAIN
python3 scripts/tiktok_pipeline.py explainer tiktok_publish/scenarios/lookbook.json
python3 scripts/tiktok_pipeline.py lookbook
```

- [ ] **Step 4: Commit**

```bash
git add scripts/tiktok_pipeline.py
git commit -m "feat(tiktok): add explainer and lookbook CLI commands to pipeline"
```

---

### Task 13: Update skill SKILL.md

**Files:**
- Modify: `/home/kacper/DOKODU_BRAIN/.claude/skills/tiktok-pipeline/SKILL.md`

- [ ] **Step 1: Add Faza 1b (explainer scenarios) to skill**

Add after Faza 1 section:
- New section "Faza 1b: Pre-production (explainery)"
- Trigger: "zrób explainera", "explainer o X", "rolka bez nagrywania"
- Steps: pick topic → write JSON scenario → render via pipeline → show output path

- [ ] **Step 2: Update KOMENDY section**

Add `explainer` and `lookbook` commands to the KOMENDY section.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/tiktok-pipeline/SKILL.md
git commit -m "feat(tiktok): update skill with explainer pipeline phase"
```
