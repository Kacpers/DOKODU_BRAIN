# CRM Multi-Instance Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor `crm-new` so the same codebase can run as multiple isolated instances (`master`, `crm-pedrollo`, `crm-haba`, ...) on the same host, each with its own URL prefix, theme, modules, and database — with NO multi-tenancy in the code (each instance gets its own Postgres).

**Architecture:** Three layers of env-driven configuration. (1) `BASE_PATH` is a **build-time** arg passed via `Dockerfile ARG` → `next.config.ts` → Next.js `basePath`. (2) `THEME_CONFIG_PATH` is **runtime**, read at root layout render, contents injected as `<style>:root { ... }</style>` overriding Tailwind v4's `@theme {}` defaults. (3) `MODULES_ENABLED` is **runtime** comma-separated list, exposed via `isModuleEnabled()` helper. Plus a `/api/health` endpoint for orchestration healthchecks.

**Tech Stack:** Next.js 15 (App Router, standalone output), TypeScript strict mode, Prisma 7, Tailwind 4, shadcn/ui, vitest (added in Task 1) + @testing-library/react, Zod for env + theme validation.

**Working directory:** `/Users/ksieradzinski/Projects/dokodu/crm-new`

**Estimated effort:** 1-2 dni roboty, ~11 atomowych tasków. TDD na warstwie biblioteki (env/theme/modules), smoke testy na warstwie integracji (route, Docker build).

---

## File Structure

### Created
- `vitest.config.ts` — test runner config
- `vitest.setup.ts` — test environment setup
- `src/lib/env.ts` — Zod-validated env vars (single source of truth)
- `src/lib/__tests__/env.test.ts`
- `src/lib/theme.ts` — theme schema, loader, CSS-vars generator
- `src/lib/__tests__/theme.test.ts`
- `src/lib/modules.ts` — `isModuleEnabled()` helper
- `src/lib/__tests__/modules.test.ts`
- `src/app/api/health/route.ts` — healthcheck endpoint
- `src/app/api/health/__tests__/route.test.ts`
- `themes/default/theme.json` — Dokodu default theme (extracted from globals.css)
- `docker-compose.template.yml` — multi-instance compose template
- `docs/multi-instance.md` — operator documentation

### Modified
- `package.json` — add vitest deps + test scripts
- `tsconfig.json` — include vitest globals types, exclude themes/ from build
- `next.config.ts` — read `BASE_PATH` env, set `basePath`
- `src/app/globals.css` — keep `@theme {}` as default fallback (no change in logic, just comment)
- `src/app/layout.tsx` — load theme JSON, inject CSS variables, conditional fonts (Plan 1: hardcoded font, theme.typography ignored — flagged as future)
- `Dockerfile` — accept `BUILD_BASE_PATH` ARG, pass to Next build step
- `CLAUDE.md` — add multi-instance section

---

## Task 1: Set up vitest test infrastructure

**Why:** crm-new has zero tests today. We need TDD for the rest of this plan. Vitest is the lightest setup that works with Next.js + TypeScript and is faster than Jest.

**Files:**
- Create: `vitest.config.ts`
- Create: `vitest.setup.ts`
- Create: `src/__tests__/smoke.test.ts` (smoke test, deleted after Task 1)
- Modify: `package.json`
- Modify: `tsconfig.json`

- [ ] **Step 1: Install vitest + supporting libraries**

Run:
```bash
cd /Users/ksieradzinski/Projects/dokodu/crm-new
pnpm add -D vitest@^2 @vitejs/plugin-react@^4 jsdom@^25 @testing-library/react@^16 @testing-library/jest-dom@^6 @testing-library/dom@^10
```

Expected: packages installed, `pnpm-lock.yaml` updated, no errors.

- [ ] **Step 2: Create `vitest.config.ts`**

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./vitest.setup.ts'],
    globals: true,
    exclude: ['**/node_modules/**', '**/.next/**', '**/dist/**'],
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

- [ ] **Step 3: Create `vitest.setup.ts`**

```typescript
// vitest.setup.ts
import '@testing-library/jest-dom/vitest';
```

- [ ] **Step 4: Add test scripts to `package.json`**

In the `scripts` section, add three new lines (keep existing scripts):

```json
"scripts": {
  "dev": "next dev -p 3001",
  "build": "next build",
  "start": "next start -p 3001",
  "lint": "next lint",
  "db:push": "prisma db push",
  "db:seed": "npx prisma db seed",
  "db:studio": "npx prisma studio",
  "migrate:brain": "tsx scripts/migrate-brain-data.ts",
  "mcp:stdio": "tsx src/mcp/stdio.ts",
  "mcp:sse": "tsx src/mcp/sse.ts",
  "test": "vitest run",
  "test:watch": "vitest",
  "test:ui": "vitest --ui"
}
```

- [ ] **Step 5: Update `tsconfig.json` to include vitest types**

Add `"types": ["vitest/globals"]` to `compilerOptions`. Final shape:

```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "react-jsx",
    "incremental": true,
    "types": ["vitest/globals"],
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./src/*"] }
  },
  "include": [
    "next-env.d.ts",
    "**/*.ts",
    "**/*.tsx",
    ".next/types/**/*.ts",
    ".next/dev/types/**/*.ts"
  ],
  "exclude": ["node_modules", "prisma/seed.ts"]
}
```

- [ ] **Step 6: Verify vitest works with a smoke test**

Create `src/__tests__/smoke.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';

describe('vitest smoke', () => {
  it('runs', () => {
    expect(1 + 1).toBe(2);
  });
});
```

Run:
```bash
pnpm test
```

Expected output (last lines):
```
 ✓ src/__tests__/smoke.test.ts (1)
   ✓ vitest smoke
     ✓ runs

 Test Files  1 passed (1)
      Tests  1 passed (1)
```

- [ ] **Step 7: Delete smoke test (it served its purpose)**

```bash
rm src/__tests__/smoke.test.ts
rmdir src/__tests__ 2>/dev/null || true
```

- [ ] **Step 8: Commit**

```bash
git add vitest.config.ts vitest.setup.ts package.json pnpm-lock.yaml tsconfig.json
git commit -m "chore(crm): set up vitest test infrastructure"
```

---

## Task 2: Create Zod-validated env schema

**Why:** All multi-instance config flows through env vars. We want a single typed source of truth so misspellings/missing values fail at startup, not at runtime in production.

**Files:**
- Create: `src/lib/env.ts`
- Create: `src/lib/__tests__/env.test.ts`

- [ ] **Step 1: Write the failing test**

Create `src/lib/__tests__/env.test.ts`:

```typescript
import { describe, it, expect, beforeEach } from 'vitest';
import { parseEnv, type Env } from '@/lib/env';

describe('parseEnv', () => {
  it('returns parsed env when DATABASE_URL is provided', () => {
    const result = parseEnv({
      DATABASE_URL: 'postgresql://user:pass@localhost:5432/db',
    });
    expect(result.DATABASE_URL).toBe('postgresql://user:pass@localhost:5432/db');
    expect(result.BASE_PATH).toBe(''); // default
    expect(result.THEME_CONFIG_PATH).toBe('./themes/default/theme.json'); // default
    expect(result.MODULES_ENABLED).toEqual([]); // default
  });

  it('throws when DATABASE_URL is missing', () => {
    expect(() => parseEnv({})).toThrow(/DATABASE_URL/);
  });

  it('parses BASE_PATH and validates leading slash', () => {
    const result = parseEnv({
      DATABASE_URL: 'postgresql://x:y@localhost/z',
      BASE_PATH: '/crm-pedrollo',
    });
    expect(result.BASE_PATH).toBe('/crm-pedrollo');
  });

  it('rejects BASE_PATH without leading slash', () => {
    expect(() =>
      parseEnv({
        DATABASE_URL: 'postgresql://x:y@localhost/z',
        BASE_PATH: 'crm-pedrollo',
      })
    ).toThrow(/BASE_PATH/);
  });

  it('parses MODULES_ENABLED as comma-separated list', () => {
    const result = parseEnv({
      DATABASE_URL: 'postgresql://x:y@localhost/z',
      MODULES_ENABLED: 'allegro,ifirma,n8n',
    });
    expect(result.MODULES_ENABLED).toEqual(['allegro', 'ifirma', 'n8n']);
  });

  it('handles empty MODULES_ENABLED', () => {
    const result = parseEnv({
      DATABASE_URL: 'postgresql://x:y@localhost/z',
      MODULES_ENABLED: '',
    });
    expect(result.MODULES_ENABLED).toEqual([]);
  });

  it('trims whitespace in MODULES_ENABLED', () => {
    const result = parseEnv({
      DATABASE_URL: 'postgresql://x:y@localhost/z',
      MODULES_ENABLED: ' allegro , ifirma ',
    });
    expect(result.MODULES_ENABLED).toEqual(['allegro', 'ifirma']);
  });

  it('exports Env type', () => {
    const env: Env = parseEnv({ DATABASE_URL: 'postgresql://x:y@localhost/z' });
    expect(env).toBeDefined();
  });
});
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pnpm test src/lib/__tests__/env.test.ts
```

Expected: FAIL — module `@/lib/env` doesn't exist.

- [ ] **Step 3: Implement `src/lib/env.ts`**

```typescript
// src/lib/env.ts
import { z } from 'zod';

const EnvSchema = z.object({
  DATABASE_URL: z.string().min(1, 'DATABASE_URL is required'),
  BASE_PATH: z
    .string()
    .regex(/^(\/[a-z0-9-]+)?$/, 'BASE_PATH must start with / or be empty')
    .default(''),
  THEME_CONFIG_PATH: z.string().default('./themes/default/theme.json'),
  MODULES_ENABLED: z
    .string()
    .default('')
    .transform((s) =>
      s
        .split(',')
        .map((m) => m.trim())
        .filter(Boolean)
    ),
});

export type Env = z.infer<typeof EnvSchema>;

/**
 * Parse and validate environment variables.
 * Throws with descriptive error if validation fails.
 *
 * @param source - usually `process.env`, but tests can pass mock objects
 */
export function parseEnv(source: Record<string, string | undefined>): Env {
  const result = EnvSchema.safeParse(source);
  if (!result.success) {
    const issues = result.error.errors
      .map((e) => `  ${e.path.join('.')}: ${e.message}`)
      .join('\n');
    throw new Error(`Environment validation failed:\n${issues}`);
  }
  return result.data;
}

/**
 * Singleton parsed env from process.env. Module-level evaluation;
 * fails fast at startup if env is invalid.
 */
export const env: Env = parseEnv(process.env as Record<string, string | undefined>);
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pnpm test src/lib/__tests__/env.test.ts
```

Expected: all 8 tests PASS.

- [ ] **Step 5: Verify TypeScript compiles**

```bash
pnpm exec tsc --noEmit
```

Expected: no errors.

- [ ] **Step 6: Commit**

```bash
git add src/lib/env.ts src/lib/__tests__/env.test.ts
git commit -m "feat(crm): add Zod-validated env schema for multi-instance config"
```

---

## Task 3: Add BASE_PATH support to next.config.ts

**Why:** Each instance lives at a URL prefix (e.g., `dev.dokodu.it/crm-pedrollo`). Next.js handles this via `basePath`, which is a build-time setting read from env.

**Files:**
- Modify: `next.config.ts`

- [ ] **Step 1: Update `next.config.ts` to read BASE_PATH**

Replace the file contents with:

```typescript
// next.config.ts
import type { NextConfig } from 'next';

// BASE_PATH is read at build time. To deploy multiple instances at different
// URL prefixes, build the Docker image with --build-arg BUILD_BASE_PATH=/crm-{slug}.
// Empty string = root path (default for master instance).
const basePath = process.env.BASE_PATH ?? '';

if (basePath !== '' && !basePath.startsWith('/')) {
  throw new Error(
    `BASE_PATH must start with "/" or be empty. Got: "${basePath}"`
  );
}

const securityHeaders = [
  { key: 'X-Frame-Options', value: 'DENY' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  { key: 'X-DNS-Prefetch-Control', value: 'on' },
  {
    key: 'Strict-Transport-Security',
    value: 'max-age=63072000; includeSubDomains; preload',
  },
  {
    key: 'Permissions-Policy',
    value: 'camera=(), microphone=(), geolocation=()',
  },
];

const nextConfig: NextConfig = {
  output: 'standalone',
  basePath: basePath || undefined,
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: securityHeaders,
      },
    ];
  },
};

export default nextConfig;
```

- [ ] **Step 2: Verify dev server still works (smoke test, no BASE_PATH)**

```bash
pnpm dev
```

Wait ~10 seconds for `Ready in Xms`. Open http://localhost:3001/ in browser. Expected: app loads at root.

Stop with Ctrl+C.

- [ ] **Step 3: Verify dev server works with BASE_PATH**

```bash
BASE_PATH=/crm-test pnpm dev
```

Wait for ready. Open http://localhost:3001/crm-test in browser. Expected: app loads at the prefix.

Stop with Ctrl+C.

- [ ] **Step 4: Verify build-time validation works**

```bash
BASE_PATH=invalid pnpm build
```

Expected: build fails with error containing `BASE_PATH must start with "/"`.

- [ ] **Step 5: Commit**

```bash
git add next.config.ts
git commit -m "feat(crm): support BASE_PATH env for multi-instance URL prefix"
```

---

## Task 4: Create theme schema, loader, CSS-vars generator

**Why:** Each instance needs its own brand. Theme is loaded at runtime from a JSON file, validated against a schema, and rendered as CSS variables that override Tailwind v4's `@theme {}` defaults.

**Files:**
- Create: `src/lib/theme.ts`
- Create: `src/lib/__tests__/theme.test.ts`

- [ ] **Step 1: Write the failing test**

Create `src/lib/__tests__/theme.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import { parseTheme, themeToCssVars, type Theme } from '@/lib/theme';

const validTheme: Theme = {
  brand: {
    name: 'Pedrollo',
    logoUrl: '/themes/pedrollo/logo.svg',
    favicon: '/themes/pedrollo/favicon.ico',
  },
  colors: {
    primary: '#0066cc',
    primaryForeground: '#ffffff',
    accent: '#ff6b35',
    accentForeground: '#ffffff',
    background: '#ffffff',
    foreground: '#0a0a0a',
    sidebar: '#0066cc',
    sidebarForeground: '#ffffff',
  },
  typography: {
    heading: 'Roboto',
    body: 'Inter',
  },
  radius: '0.5rem',
  darkMode: false,
};

describe('parseTheme', () => {
  it('parses a valid theme', () => {
    const result = parseTheme(validTheme);
    expect(result.brand.name).toBe('Pedrollo');
    expect(result.colors.primary).toBe('#0066cc');
  });

  it('rejects non-hex color', () => {
    expect(() =>
      parseTheme({
        ...validTheme,
        colors: { ...validTheme.colors, primary: 'rgb(0,0,0)' },
      })
    ).toThrow(/primary/);
  });

  it('rejects missing brand name', () => {
    expect(() =>
      parseTheme({
        ...validTheme,
        brand: { ...validTheme.brand, name: '' },
      })
    ).toThrow(/name/);
  });

  it('uses default radius when omitted', () => {
    const { radius, ...rest } = validTheme;
    void radius;
    const parsed = parseTheme(rest);
    expect(parsed.radius).toBe('0.5rem');
  });
});

describe('themeToCssVars', () => {
  it('generates CSS variable string with --color-* prefix', () => {
    const css = themeToCssVars(validTheme);
    expect(css).toContain('--color-primary: #0066cc;');
    expect(css).toContain('--color-accent: #ff6b35;');
    expect(css).toContain('--color-sidebar: #0066cc;');
  });

  it('generates --radius from radius', () => {
    const css = themeToCssVars(validTheme);
    expect(css).toContain('--radius: 0.5rem;');
  });

  it('handles camelCase keys → kebab-case CSS vars', () => {
    const css = themeToCssVars(validTheme);
    expect(css).toContain('--color-primary-foreground: #ffffff;');
    expect(css).toContain('--color-sidebar-foreground: #ffffff;');
  });

  it('output is valid as :root rule body (no leading semicolons)', () => {
    const css = themeToCssVars(validTheme);
    expect(css.trim().startsWith('--')).toBe(true);
    expect(css.trim().endsWith(';')).toBe(true);
  });
});
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pnpm test src/lib/__tests__/theme.test.ts
```

Expected: FAIL — module `@/lib/theme` doesn't exist.

- [ ] **Step 3: Implement `src/lib/theme.ts`**

```typescript
// src/lib/theme.ts
import { z } from 'zod';
import { readFileSync } from 'fs';
import { resolve } from 'path';

const HexColor = z.string().regex(/^#[0-9a-fA-F]{3,8}$/, 'must be hex color');

const ThemeSchema = z.object({
  brand: z.object({
    name: z.string().min(1, 'brand.name required'),
    logoUrl: z.string().min(1),
    logoDarkUrl: z.string().optional(),
    favicon: z.string().min(1),
  }),
  colors: z.object({
    primary: HexColor,
    primaryForeground: HexColor,
    accent: HexColor,
    accentForeground: HexColor,
    background: HexColor,
    foreground: HexColor,
    sidebar: HexColor,
    sidebarForeground: HexColor,
  }),
  typography: z
    .object({
      heading: z.string(),
      body: z.string(),
    })
    .optional(),
  radius: z.string().default('0.5rem'),
  darkMode: z.boolean().default(false),
});

export type Theme = z.infer<typeof ThemeSchema>;

export function parseTheme(input: unknown): Theme {
  const result = ThemeSchema.safeParse(input);
  if (!result.success) {
    const issues = result.error.errors
      .map((e) => `  ${e.path.join('.')}: ${e.message}`)
      .join('\n');
    throw new Error(`Theme validation failed:\n${issues}`);
  }
  return result.data;
}

/**
 * Loads and validates theme.json from disk.
 * Path can be relative (resolved from cwd) or absolute.
 */
export function loadTheme(path: string): Theme {
  const absolute = resolve(path);
  const raw = readFileSync(absolute, 'utf-8');
  const parsed = JSON.parse(raw);
  return parseTheme(parsed);
}

/**
 * Convert a Theme object to a string of CSS variable declarations
 * suitable for injection into a <style>:root { ... }</style> block.
 *
 * camelCase keys are converted to kebab-case (primaryForeground → primary-foreground).
 * Color keys get the --color- prefix; radius gets --radius.
 */
export function themeToCssVars(theme: Theme): string {
  const lines: string[] = [];

  for (const [key, value] of Object.entries(theme.colors)) {
    const cssKey = camelToKebab(key);
    lines.push(`  --color-${cssKey}: ${value};`);
  }

  lines.push(`  --radius: ${theme.radius};`);

  return lines.join('\n');
}

function camelToKebab(s: string): string {
  return s.replace(/([a-z0-9])([A-Z])/g, '$1-$2').toLowerCase();
}
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pnpm test src/lib/__tests__/theme.test.ts
```

Expected: all 9 tests PASS.

- [ ] **Step 5: Verify TypeScript compiles**

```bash
pnpm exec tsc --noEmit
```

Expected: no errors.

- [ ] **Step 6: Commit**

```bash
git add src/lib/theme.ts src/lib/__tests__/theme.test.ts
git commit -m "feat(crm): add theme schema, loader, CSS-vars generator"
```

---

## Task 5: Create default theme.json (Dokodu)

**Why:** The current `globals.css` `@theme {}` block has Dokodu colors hardcoded. We extract those to `themes/default/theme.json` so master instance still works the same, but with the same theme-loading mechanism every other instance uses.

**Files:**
- Create: `themes/default/theme.json`
- Modify: `tsconfig.json` (exclude `themes/` from build)

- [ ] **Step 1: Create `themes/default/theme.json`**

Extract values from `src/app/globals.css` lines 4-32:

```json
{
  "brand": {
    "name": "Dokodu CRM",
    "logoUrl": "/logo.svg",
    "favicon": "/favicon.ico"
  },
  "colors": {
    "primary": "#0F2137",
    "primaryForeground": "#ffffff",
    "accent": "#E63946",
    "accentForeground": "#ffffff",
    "background": "#F8FAFC",
    "foreground": "#0F2137",
    "sidebar": "#0F2137",
    "sidebarForeground": "#CBD5E1"
  },
  "typography": {
    "heading": "Plus Jakarta Sans",
    "body": "Plus Jakarta Sans"
  },
  "radius": "0.5rem",
  "darkMode": false
}
```

- [ ] **Step 2: Update `tsconfig.json` exclude**

In `tsconfig.json`, add `"themes"` to `exclude`:

```json
"exclude": ["node_modules", "prisma/seed.ts", "themes"]
```

This prevents TS from picking up theme.json files and getting confused.

- [ ] **Step 3: Verify file is valid JSON via theme loader**

Add a quick smoke test inline (not committed, just verification):

```bash
node -e "const { loadTheme } = require('./src/lib/theme.ts'); console.log(loadTheme('./themes/default/theme.json'))"
```

If this fails because Node can't run TS directly:

```bash
pnpm exec tsx -e "import { loadTheme } from './src/lib/theme'; console.log(loadTheme('./themes/default/theme.json'))"
```

Expected: outputs the parsed theme object with all keys.

- [ ] **Step 4: Commit**

```bash
git add themes/default/theme.json tsconfig.json
git commit -m "feat(crm): extract Dokodu default theme to themes/default/theme.json"
```

---

## Task 6: Inject theme CSS variables in root layout

**Why:** The theme JSON needs to actually apply to the running app. Approach: load theme in the (Server Component) root layout, render `<style>:root { ... }</style>` in `<head>`, which overrides Tailwind v4's `@theme {}` defaults due to CSS specificity / source order.

**Files:**
- Modify: `src/app/layout.tsx`

- [ ] **Step 1: Update `src/app/layout.tsx`**

Replace contents:

```typescript
// src/app/layout.tsx
import type { Metadata } from 'next';
import { Plus_Jakarta_Sans } from 'next/font/google';
import { Toaster } from 'sonner';
import { loadTheme, themeToCssVars } from '@/lib/theme';
import { env } from '@/lib/env';
import './globals.css';

const plusJakarta = Plus_Jakarta_Sans({
  subsets: ['latin', 'latin-ext'],
  weight: ['400', '500', '600', '700'],
});

// Load theme once at module init (Server Component context).
// In dev, Next.js HMR will reload this; in prod, it's cached for process lifetime.
const theme = loadTheme(env.THEME_CONFIG_PATH);

export const metadata: Metadata = {
  title: theme.brand.name,
  description: 'CRM by Dokodu',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const cssVars = themeToCssVars(theme);

  return (
    <html lang="pl">
      <head>
        <link rel="icon" href={theme.brand.favicon} />
        <style
          // Theme CSS vars must come AFTER Tailwind globals to win specificity.
          // Tailwind v4 @theme {} block in globals.css emits :root { ... };
          // this :root block re-declares the same vars and overrides them.
          dangerouslySetInnerHTML={{
            __html: `:root {\n${cssVars}\n}`,
          }}
        />
      </head>
      <body className={plusJakarta.className}>
        {children}
        <Toaster richColors position="top-right" />
      </body>
    </html>
  );
}
```

- [ ] **Step 2: Verify dev server boots**

```bash
pnpm dev
```

Expected: `Ready in Xms`, no errors. Open http://localhost:3001 — app looks the same as before (because default theme matches the existing `@theme {}` values).

- [ ] **Step 3: Verify CSS variable is injected**

In browser DevTools (Inspect → Elements → `<html>`), confirm `<style>:root { --color-primary: #0F2137; ... }</style>` is present in `<head>`.

In DevTools Computed tab on `<body>`, confirm `--color-primary` resolves to `#0F2137`.

- [ ] **Step 4: Verify theme switching works (smoke)**

Create a temporary alt theme:

```bash
mkdir -p themes/test
cat > themes/test/theme.json <<'EOF'
{
  "brand": { "name": "TEST", "logoUrl": "/logo.svg", "favicon": "/favicon.ico" },
  "colors": {
    "primary": "#ff0000",
    "primaryForeground": "#ffffff",
    "accent": "#00ff00",
    "accentForeground": "#000000",
    "background": "#ffffff",
    "foreground": "#000000",
    "sidebar": "#ff0000",
    "sidebarForeground": "#ffffff"
  },
  "radius": "0.5rem",
  "darkMode": false
}
EOF
```

Restart dev server with this theme:

```bash
THEME_CONFIG_PATH=./themes/test/theme.json pnpm dev
```

Open http://localhost:3001. Sidebar should be RED (where it was navy). Tab title should say "TEST".

Stop server with Ctrl+C. Clean up:

```bash
rm -rf themes/test
```

- [ ] **Step 5: Verify TypeScript still compiles**

```bash
pnpm exec tsc --noEmit
```

Expected: no errors.

- [ ] **Step 6: Commit**

```bash
git add src/app/layout.tsx
git commit -m "feat(crm): inject theme CSS variables in root layout from theme.json"
```

---

## Task 7: Module feature flag helper

**Why:** Each instance has a different set of modules enabled. We need a single helper to check at runtime: `isModuleEnabled('allegro')`. This will be used in Plan 3 to gate routes/UI; in Plan 1 we just build the helper.

**Files:**
- Create: `src/lib/modules.ts`
- Create: `src/lib/__tests__/modules.test.ts`

- [ ] **Step 1: Write the failing test**

Create `src/lib/__tests__/modules.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import { createModuleRegistry } from '@/lib/modules';

describe('createModuleRegistry', () => {
  it('reports enabled module as enabled', () => {
    const reg = createModuleRegistry(['allegro', 'ifirma']);
    expect(reg.isEnabled('allegro')).toBe(true);
  });

  it('reports disabled module as disabled', () => {
    const reg = createModuleRegistry(['allegro']);
    expect(reg.isEnabled('ifirma')).toBe(false);
  });

  it('returns the list of enabled modules', () => {
    const reg = createModuleRegistry(['allegro', 'ifirma']);
    expect(reg.list()).toEqual(['allegro', 'ifirma']);
  });

  it('handles empty registry', () => {
    const reg = createModuleRegistry([]);
    expect(reg.isEnabled('anything')).toBe(false);
    expect(reg.list()).toEqual([]);
  });

  it('is case-sensitive', () => {
    const reg = createModuleRegistry(['allegro']);
    expect(reg.isEnabled('Allegro')).toBe(false);
    expect(reg.isEnabled('allegro')).toBe(true);
  });

  it('module names must match registered modules exactly', () => {
    const reg = createModuleRegistry(['n8n-connector']);
    expect(reg.isEnabled('n8n-connector')).toBe(true);
    expect(reg.isEnabled('n8n')).toBe(false);
  });
});
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pnpm test src/lib/__tests__/modules.test.ts
```

Expected: FAIL — module `@/lib/modules` doesn't exist.

- [ ] **Step 3: Implement `src/lib/modules.ts`**

```typescript
// src/lib/modules.ts
import { env } from '@/lib/env';

export interface ModuleRegistry {
  isEnabled(name: string): boolean;
  list(): readonly string[];
}

/**
 * Creates a module registry from a list of enabled module names.
 *
 * Use this directly in tests; in app code, prefer the singleton `modules` export below.
 */
export function createModuleRegistry(enabled: string[]): ModuleRegistry {
  const set = new Set(enabled);
  const sorted = [...enabled];

  return {
    isEnabled(name: string): boolean {
      return set.has(name);
    },
    list(): readonly string[] {
      return sorted;
    },
  };
}

/**
 * Singleton registry derived from MODULES_ENABLED env var.
 */
export const modules: ModuleRegistry = createModuleRegistry(env.MODULES_ENABLED);
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pnpm test src/lib/__tests__/modules.test.ts
```

Expected: all 6 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/lib/modules.ts src/lib/__tests__/modules.test.ts
git commit -m "feat(crm): add module registry with isEnabled() helper"
```

---

## Task 8: /api/health endpoint

**Why:** Reverse-nginx (Plan 2) and Uptime Kuma (Plan 7) need a healthcheck. Returns 200 if the app is up AND Postgres is reachable, 503 otherwise.

**Files:**
- Create: `src/app/api/health/route.ts`
- Create: `src/app/api/health/__tests__/route.test.ts`

- [ ] **Step 1: Find the existing Prisma client export**

Check where Prisma client is instantiated:

```bash
grep -r "PrismaClient" src/lib/ src/app/ --include="*.ts" --include="*.tsx" | head -20
```

Expected: there's already a singleton (likely `src/lib/prisma.ts` or `src/lib/db.ts`). Note the import path. If none exists, the implementation in Step 3 instantiates one inline (not ideal — flag in commit message).

- [ ] **Step 2: Write the failing test**

Create `src/app/api/health/__tests__/route.test.ts`:

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock Prisma client BEFORE importing the route handler
const mockQueryRaw = vi.fn();
vi.mock('@/lib/prisma', () => ({
  prisma: {
    $queryRaw: mockQueryRaw,
  },
}));

describe('/api/health route', () => {
  beforeEach(() => {
    mockQueryRaw.mockReset();
  });

  it('returns 200 with status:ok when DB is reachable', async () => {
    mockQueryRaw.mockResolvedValueOnce([{ ok: 1 }]);

    const { GET } = await import('@/app/api/health/route');
    const res = await GET();

    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body.status).toBe('ok');
    expect(body.db).toBe('up');
  });

  it('returns 503 with status:error when DB is unreachable', async () => {
    mockQueryRaw.mockRejectedValueOnce(new Error('connection refused'));

    const { GET } = await import('@/app/api/health/route');
    const res = await GET();

    expect(res.status).toBe(503);
    const body = await res.json();
    expect(body.status).toBe('error');
    expect(body.db).toBe('down');
  });
});
```

- [ ] **Step 3: Run tests to verify they fail**

```bash
pnpm test src/app/api/health/__tests__/route.test.ts
```

Expected: FAIL — module `@/app/api/health/route` doesn't exist.

- [ ] **Step 4: Implement `src/app/api/health/route.ts`**

If `@/lib/prisma` exists (from Step 1), use it. Otherwise create it first:

```typescript
// src/lib/prisma.ts (only if it doesn't exist yet)
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as { prisma?: PrismaClient };

export const prisma = globalForPrisma.prisma ?? new PrismaClient();

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;
```

Then the route:

```typescript
// src/app/api/health/route.ts
import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export const dynamic = 'force-dynamic';
export const revalidate = 0;

export async function GET() {
  try {
    await prisma.$queryRaw`SELECT 1 AS ok`;
    return NextResponse.json(
      { status: 'ok', db: 'up', timestamp: new Date().toISOString() },
      { status: 200 }
    );
  } catch (err) {
    return NextResponse.json(
      {
        status: 'error',
        db: 'down',
        error: err instanceof Error ? err.message : 'unknown',
        timestamp: new Date().toISOString(),
      },
      { status: 503 }
    );
  }
}
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
pnpm test src/app/api/health/__tests__/route.test.ts
```

Expected: both tests PASS.

- [ ] **Step 6: Smoke test the endpoint live**

Start the app (assumes Postgres is running locally — if not, use `docker compose up crm-db`):

```bash
pnpm dev
```

In another terminal:

```bash
curl -s http://localhost:3001/api/health | jq
```

Expected response:
```json
{
  "status": "ok",
  "db": "up",
  "timestamp": "2026-..."
}
```

Stop dev server.

- [ ] **Step 7: Commit**

```bash
git add src/app/api/health/route.ts src/app/api/health/__tests__/route.test.ts
# Include src/lib/prisma.ts only if you created it in Step 4
[ -f src/lib/prisma.ts ] && git add src/lib/prisma.ts || true
git commit -m "feat(crm): add /api/health endpoint with DB readiness check"
```

---

## Task 9: Update Dockerfile for BASE_PATH build arg

**Why:** Each instance is built with its own BASE_PATH. Dockerfile needs to accept the arg and pass it to the Next build step as env.

**Files:**
- Modify: `Dockerfile`

- [ ] **Step 1: Update `Dockerfile`**

Replace contents:

```dockerfile
# ─────────────────────────────────────────
# Stage 1: Install dependencies
# ─────────────────────────────────────────
FROM node:20-alpine AS deps
RUN corepack enable
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# ─────────────────────────────────────────
# Stage 2: Build application
# ─────────────────────────────────────────
FROM node:20-alpine AS builder
RUN corepack enable
WORKDIR /app

# BUILD_BASE_PATH is consumed by next.config.ts at build time.
# Empty string (default) = root path. Otherwise must start with /.
# Example: docker build --build-arg BUILD_BASE_PATH=/crm-pedrollo .
ARG BUILD_BASE_PATH=""
ENV BASE_PATH=${BUILD_BASE_PATH}

COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npx prisma generate
RUN pnpm build

# ─────────────────────────────────────────
# Stage 3: Production runner
# ─────────────────────────────────────────
FROM node:20-alpine AS runner
RUN corepack enable
WORKDIR /app
ENV NODE_ENV=production

# Re-declare BASE_PATH at runtime so app code (e.g. links built dynamically)
# can read it. Keeps build-time and runtime values consistent.
ARG BUILD_BASE_PATH=""
ENV BASE_PATH=${BUILD_BASE_PATH}

# Copy standalone Next.js output
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

# Theme config (mountable at runtime via volume too)
COPY --from=builder /app/themes ./themes

# Prisma client + schema
COPY --from=builder /app/prisma ./prisma

# Full node_modules (needed by MCP server, seed, prisma)
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

# MCP server source + shared libs
COPY --from=builder /app/src/mcp ./src/mcp
COPY --from=builder /app/src/lib ./src/lib

EXPOSE 3001
ENV PORT=3001

# Healthcheck: hits /api/health, includes basePath if set
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD wget --quiet --tries=1 --spider "http://127.0.0.1:3001${BASE_PATH}/api/health" || exit 1

CMD ["node", "server.js"]
```

- [ ] **Step 2: Build the image with no BASE_PATH (default)**

```bash
docker build -t dokodu-crm:latest .
```

Expected: build succeeds in 1-3 minutes. No errors.

- [ ] **Step 3: Build the image with BASE_PATH**

```bash
docker build --build-arg BUILD_BASE_PATH=/crm-test -t dokodu-crm:test .
```

Expected: build succeeds.

- [ ] **Step 4: Verify the image starts (skip if no DB available)**

This is optional — full smoke test happens in Plan 2 with docker-compose. For Plan 1, just check the image exists:

```bash
docker images | grep dokodu-crm
```

Expected: two tags listed (`latest` and `test`).

- [ ] **Step 5: Cleanup test images**

```bash
docker rmi dokodu-crm:test
```

- [ ] **Step 6: Commit**

```bash
git add Dockerfile
git commit -m "feat(crm): accept BUILD_BASE_PATH build arg in Dockerfile"
```

---

## Task 10: Create docker-compose template

**Why:** Plan 2's `/crm-new-demo` skill will need a way to instantiate the compose stack per slug. We create a parameterized template now.

**Files:**
- Create: `docker-compose.template.yml`

- [ ] **Step 1: Create `docker-compose.template.yml`**

```yaml
# docker-compose.template.yml — multi-instance template
#
# Variables to substitute (envsubst-style):
#   ${SLUG}            — instance slug, e.g. "pedrollo" or "haba"
#   ${BASE_PATH}       — URL prefix, e.g. "/crm-pedrollo" (must match container build)
#   ${THEME_PATH}      — host path to theme.json, e.g. "./themes/pedrollo/theme.json"
#   ${MODULES_ENABLED} — comma-separated, e.g. "core,allegro,ifirma"
#   ${DB_PASSWORD}     — generated random per instance
#   ${NEXTAUTH_SECRET} — generated random per instance
#   ${NEXTAUTH_URL}    — full URL, e.g. "https://dev.dokodu.it/crm-pedrollo"
#
# Usage from /crm-new-demo skill:
#   envsubst < docker-compose.template.yml > docker-compose.${SLUG}.yml
#   docker compose -f docker-compose.${SLUG}.yml -p crm-${SLUG} up -d

services:
  crm:
    build:
      context: .
      args:
        BUILD_BASE_PATH: ${BASE_PATH}
    container_name: crm-${SLUG}
    restart: unless-stopped
    environment:
      DATABASE_URL: "postgresql://crm:${DB_PASSWORD}@crm-db-${SLUG}:5432/crm"
      BASE_PATH: ${BASE_PATH}
      THEME_CONFIG_PATH: /app/themes/${SLUG}/theme.json
      MODULES_ENABLED: ${MODULES_ENABLED}
      NEXTAUTH_SECRET: ${NEXTAUTH_SECRET}
      NEXTAUTH_URL: ${NEXTAUTH_URL}
      HOSTNAME: "0.0.0.0"
      AUTH_TRUST_HOST: "true"
    depends_on:
      crm-db-${SLUG}:
        condition: service_healthy
    volumes:
      - ${THEME_PATH}:/app/themes/${SLUG}/theme.json:ro
      - uploads-${SLUG}:/app/uploads
    networks:
      - web
      - crm-${SLUG}-internal
    labels:
      - "dokodu.crm.slug=${SLUG}"
      - "dokodu.crm.instance=true"

  crm-db-${SLUG}:
    image: postgres:16-alpine
    container_name: crm-db-${SLUG}
    restart: unless-stopped
    environment:
      POSTGRES_DB: crm
      POSTGRES_USER: crm
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - crm-pgdata-${SLUG}:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U crm -d crm"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - crm-${SLUG}-internal
    labels:
      - "dokodu.crm.slug=${SLUG}"

  crm-migrate-${SLUG}:
    build:
      context: .
      args:
        BUILD_BASE_PATH: ${BASE_PATH}
    container_name: crm-migrate-${SLUG}
    environment:
      DATABASE_URL: "postgresql://crm:${DB_PASSWORD}@crm-db-${SLUG}:5432/crm"
    depends_on:
      crm-db-${SLUG}:
        condition: service_healthy
    entrypoint: ["sh", "-c", "npx prisma db push && npx prisma db seed"]
    networks:
      - crm-${SLUG}-internal
    profiles:
      - migrate

volumes:
  crm-pgdata-${SLUG}:
  uploads-${SLUG}:

networks:
  web:
    external: true
  crm-${SLUG}-internal:
```

- [ ] **Step 2: Validate the template syntax**

The template uses `${VAR}` which docker compose itself will try to substitute from the shell. We use `envsubst` upstream (in Plan 2's skill) to substitute first. For Plan 1, just verify YAML is valid:

```bash
SLUG=test BASE_PATH=/crm-test THEME_PATH=./themes/default/theme.json \
  MODULES_ENABLED=core DB_PASSWORD=x NEXTAUTH_SECRET=y \
  NEXTAUTH_URL=http://localhost:3001/crm-test \
  envsubst < docker-compose.template.yml > /tmp/dctest.yml

docker compose -f /tmp/dctest.yml config > /dev/null
echo "Template valid: $?"
```

Expected: `Template valid: 0`. If `envsubst` is missing on macOS, install: `brew install gettext && brew link --force gettext`.

Cleanup:
```bash
rm /tmp/dctest.yml
```

- [ ] **Step 3: Commit**

```bash
git add docker-compose.template.yml
git commit -m "feat(crm): add docker-compose template for multi-instance deploys"
```

---

## Task 11: Operator documentation

**Why:** A future Kacper (or Dokodu engineer) needs to know how this works. Without docs, the multi-instance pattern is opaque.

**Files:**
- Create: `docs/multi-instance.md`
- Modify: `CLAUDE.md`

- [ ] **Step 1: Create `docs/multi-instance.md`**

```markdown
# Multi-Instance Deployment

`crm-new` is designed to run as multiple isolated instances on the same host
(e.g., `dev.dokodu.it/crm`, `dev.dokodu.it/crm-pedrollo`, `dev.dokodu.it/crm-haba`).

This document describes the configuration model. The orchestration tooling
(`/crm-new-demo` BRAIN skill, reverse-nginx routing, theme generator) is
implemented in Plan 2.

## Configuration layers

| Var | When read | Purpose |
|---|---|---|
| `BASE_PATH` | **build time** | Next.js URL prefix. Empty = root. Must start with `/`. |
| `THEME_CONFIG_PATH` | **runtime** | Path to theme.json (loaded by `src/app/layout.tsx`) |
| `MODULES_ENABLED` | **runtime** | Comma-separated list of enabled module names |
| `DATABASE_URL` | **runtime** | Postgres connection string (each instance has its own DB) |
| `NEXTAUTH_SECRET` | **runtime** | Auth secret (generated per instance) |
| `NEXTAUTH_URL` | **runtime** | Full external URL (`https://dev.dokodu.it/crm-{slug}`) |

## Why BASE_PATH is build-time

Next.js reads `basePath` from `next.config.ts` at build time. Internal links,
asset URLs, and route segments are baked in. To change `BASE_PATH` you must
rebuild. This means: **one Docker image per instance**.

This is acceptable: build is ~2 min, image storage is cheap, the simplicity
of "no runtime URL rewriting" is worth it. Alternative (reverse-proxy path
stripping) was considered and rejected as fragile.

## Why theme is runtime

The theme is read in the root layout's render path (`src/app/layout.tsx`).
On startup, the file at `THEME_CONFIG_PATH` is loaded, validated against the
Zod schema in `src/lib/theme.ts`, and emitted as CSS variables on `:root`.

This means changing the theme requires a container restart, not a rebuild.
The same Docker image can serve any number of brands.

## Default theme

If `THEME_CONFIG_PATH` is unset, defaults to `./themes/default/theme.json`
(Dokodu navy + red).

## Theme schema

See `src/lib/theme.ts` for the canonical Zod schema. Required fields:

- `brand`: name, logoUrl, favicon
- `colors`: primary, primaryForeground, accent, accentForeground, background,
  foreground, sidebar, sidebarForeground (all hex)
- `radius`: CSS rem value (default `0.5rem`)
- `darkMode`: boolean (default false)

Tailwind v4's `@theme {}` block in `src/app/globals.css` provides defaults;
the layout's injected `:root { ... }` block overrides per instance.

## Module flag check

```ts
import { modules } from '@/lib/modules';

if (modules.isEnabled('allegro')) {
  // render Allegro UI
}
```

Module names are exact-match, case-sensitive. List of enabled modules:

```ts
modules.list(); // ['core', 'allegro', 'ifirma']
```

## Healthcheck

`GET /api/health` returns `200 { status: 'ok', db: 'up' }` when DB reachable,
`503 { status: 'error', db: 'down' }` otherwise. Used by Docker HEALTHCHECK
and (in Plan 7) Uptime Kuma.

## Local multi-instance development

Run two instances side-by-side:

```bash
# Terminal 1 — master
THEME_CONFIG_PATH=./themes/default/theme.json pnpm dev
# → http://localhost:3001

# Terminal 2 — different theme (must use different port)
PORT=3002 THEME_CONFIG_PATH=./themes/test/theme.json pnpm dev -p 3002
# → http://localhost:3002

# Note: BASE_PATH simulation locally requires `next dev` flags; in production
# each instance is its own container with its own build.
```

## Production deployment

Out of scope for Plan 1 — see Plan 2 (`docker-compose.template.yml` +
`/crm-new-demo` skill + reverse-nginx routing).
```

- [ ] **Step 2: Add multi-instance section to `CLAUDE.md`**

Append to the end of `/Users/ksieradzinski/Projects/dokodu/crm-new/CLAUDE.md`:

```markdown

## Multi-instance deployment

This codebase supports multi-instance deploys driven by env vars + theme JSON.
Each prospect/client gets their own Docker container, Postgres DB, theme,
and (optionally) module set — sharing one image-build per BASE_PATH.

See `docs/multi-instance.md` for full operator docs.

Key env vars:
- `BASE_PATH` (build-time) — URL prefix, e.g. `/crm-pedrollo`
- `THEME_CONFIG_PATH` (runtime) — path to theme.json (default `./themes/default/theme.json`)
- `MODULES_ENABLED` (runtime) — comma list of module names

Theme schema: `src/lib/theme.ts`. Module helper: `src/lib/modules.ts`.
Healthcheck: `/api/health`.
```

- [ ] **Step 3: Commit**

```bash
git add docs/multi-instance.md CLAUDE.md
git commit -m "docs(crm): document multi-instance config model"
```

---

## Final verification

After all 11 tasks done, run a full check:

- [ ] **Step 1: All tests pass**

```bash
pnpm test
```

Expected: all tests pass (env: 8, theme: 9, modules: 6, health: 2 = 25 total).

- [ ] **Step 2: TypeScript compiles**

```bash
pnpm exec tsc --noEmit
```

Expected: no errors.

- [ ] **Step 3: Lint passes**

```bash
pnpm lint
```

Expected: no errors. Warnings OK to acknowledge.

- [ ] **Step 4: Production build works (default theme, no BASE_PATH)**

```bash
pnpm build
```

Expected: build completes, `.next/standalone` exists.

- [ ] **Step 5: Production build works (with BASE_PATH)**

```bash
BASE_PATH=/crm-test pnpm build
```

Expected: build completes.

- [ ] **Step 6: Docker build (default)**

```bash
docker build -t dokodu-crm:foundation-test .
docker rmi dokodu-crm:foundation-test
```

Expected: build succeeds.

- [ ] **Step 7: Verify commit log is clean**

```bash
git log --oneline | head -15
```

Expected: 11 commits in order, each focused, each green.

---

## Out of scope (NEXT plans, NOT this one)

- Theme-from-URL CLI script (Plan 2)
- Reverse-nginx routing config (Plan 2)
- BRAIN `/crm-new-demo` skill (Plan 2)
- Pedrollo/HABA seed bundles (Plan 2)
- `/crm-fork-prospekt` and other operational skille (Plan 3)
- Cmd+K AI parser (Plan 4)
- Drawer + multi-view UX (Plan 5)
- Bulletproof PII inventory codegen (Plan 6)
- Backup/monitoring/deploy infra (Plan 7)

## Open questions surfaced during planning

1. **Prisma client singleton location** — Task 8 Step 1 grep'uje istniejący export. Jeśli go nie ma, Task 8 Step 4 tworzy `src/lib/prisma.ts`. Po Task 8 należy SPRAWDZIĆ czy reszta API routes używa tego samego importu — jeśli nie, wymaga refactoru (osobny commit).

2. **Theme typography (font loading)** — Plan 1 trzyma hardcoded `Plus_Jakarta_Sans`. `theme.typography.heading/body` jest w schemacie ale ignorowane przy renderowaniu. Dynamic Google Fonts loading jest osobnym małym Plan-em (lub task w Plan 2/5).

3. **Theme dark mode** — flaga `darkMode: false` jest w schemacie ale nie jest jeszcze wykorzystywana w UI. Do podpięcia w Plan 5 (UX framework refresh) razem z prefer-color-scheme.

4. **MCP server `BASE_PATH`** — `crm-mcp` container w docker-compose używa innego entrypoint (`mcp:sse`). Czy jego routing też potrzebuje BASE_PATH? Jeśli MCP też ma być per-instance, trzeba rozważyć w Plan 2. Plan 1 zakłada że MCP jest singleton (jeden na całą Dokodu, nie per klient).
