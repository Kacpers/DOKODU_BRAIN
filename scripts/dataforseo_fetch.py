#!/usr/bin/env python3
"""
DataForSEO API client for dokodu.it blog SEO research.

Usage:
    python3 dataforseo_fetch.py check
    python3 dataforseo_fetch.py suggestions n8n "automatyzacja ai" --save
    python3 dataforseo_fetch.py ideas "agent ai" --save
    python3 dataforseo_fetch.py ranked dokodu.it --save
    python3 dataforseo_fetch.py budget

Reads credentials from ~/.config/dokodu/dataforseo_credentials.
Logs every paid call to ~/.config/dokodu/dataforseo_budget.json.
Defaults: location_code=2616 (Poland), language_code=pl.
"""
import argparse
import base64
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CREDS_FILE = Path.home() / ".config/dokodu/dataforseo_credentials"
BUDGET_FILE = Path.home() / ".config/dokodu/dataforseo_budget.json"
SEEDS_FILE = Path.home() / ".config/dokodu/dataforseo_seeds.txt"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "20_AREAS/AREA_Blog_SEO/dataforseo"
WEEKLY_DIR = OUTPUT_DIR / "weekly"
API_BASE = "https://api.dataforseo.com"
LOCATION_PL = 2616
LANGUAGE_PL = "pl"

# Default seedy dla weekly research — można nadpisać przez ~/.config/dokodu/dataforseo_seeds.txt (jedna fraza per linia)
DEFAULT_SEEDS = [
    "n8n",
    "automatyzacja ai",
    "cursor",
    "claude code",
    "agent ai",
]
WEEKLY_SUGGESTION_LIMIT = 200
WEEKLY_RANKED_LIMIT = 500
WEEKLY_BUDGET_USD = 0.50  # twardy próg ostrzeżenia


def load_creds():
    if not CREDS_FILE.exists():
        sys.exit(f"Missing {CREDS_FILE}")
    creds = {}
    for line in CREDS_FILE.read_text().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            creds[k.strip()] = v.strip()
    return creds["DATAFORSEO_LOGIN"], creds["DATAFORSEO_PASSWORD"]


def call_api(method, path, body=None):
    login, password = load_creds()
    token = base64.b64encode(f"{login}:{password}".encode()).decode()
    headers = {"Authorization": f"Basic {token}", "Content-Type": "application/json"}
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(f"{API_BASE}{path}", data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def track_cost(label, cost, meta=None):
    BUDGET_FILE.parent.mkdir(parents=True, exist_ok=True)
    log = json.loads(BUDGET_FILE.read_text()) if BUDGET_FILE.exists() else []
    log.append({
        "ts": datetime.now(timezone.utc).isoformat(),
        "call": label,
        "cost": cost,
        "meta": meta or {},
    })
    BUDGET_FILE.write_text(json.dumps(log, indent=2))


def total_spent():
    if not BUDGET_FILE.exists():
        return 0.0
    return sum(e["cost"] for e in json.loads(BUDGET_FILE.read_text()))


def save_json(prefix, data):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    out = OUTPUT_DIR / f"{prefix}-{ts}.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    return out


def fmt_int(v):
    return f"{v:,}".replace(",", " ") if isinstance(v, (int, float)) else "—"


def cmd_check(args):
    res = call_api("GET", "/v3/appendix/user_data")
    r = res["tasks"][0]["result"][0]
    print(f"Login:   {r['login']}")
    print(f"Balance: ${r['money']['balance']:.4f} USD")
    print(f"Spent (this script): ${total_spent():.4f} USD")
    if BUDGET_FILE.exists():
        log = json.loads(BUDGET_FILE.read_text())
        print(f"Calls logged: {len(log)}")


def cmd_budget(args):
    if not BUDGET_FILE.exists():
        print("No calls logged yet.")
        return
    log = json.loads(BUDGET_FILE.read_text())
    by_call = {}
    for e in log:
        by_call.setdefault(e["call"].split(":")[0], 0)
        by_call[e["call"].split(":")[0]] += e["cost"]
    print(f"Total spent: ${total_spent():.4f}")
    print(f"Calls: {len(log)}")
    print("\nBy endpoint:")
    for k, v in sorted(by_call.items(), key=lambda x: -x[1]):
        print(f"  {k:30s} ${v:.4f}")
    print("\nLast 10 calls:")
    for e in log[-10:]:
        print(f"  {e['ts'][:19]} {e['call']:40s} ${e['cost']:.4f}")


def _flatten_keyword_item(item, seed=None):
    kw = item.get("keyword_info", {}) or {}
    si = item.get("search_intent_info", {}) or {}
    return {
        "seed": seed,
        "keyword": item.get("keyword"),
        "search_volume": kw.get("search_volume"),
        "cpc": kw.get("cpc"),
        "competition": kw.get("competition"),
        "competition_level": kw.get("competition_level"),
        "low_bid": kw.get("low_top_of_page_bid"),
        "high_bid": kw.get("high_top_of_page_bid"),
        "main_intent": si.get("main_intent"),
        "categories": kw.get("categories"),
    }


def cmd_suggestions(args):
    """Labs Keyword Suggestions: long-tail expansions containing the seed."""
    all_results = []
    total_cost = 0.0
    for seed in args.seeds:
        body = [{
            "keyword": seed,
            "location_code": LOCATION_PL,
            "language_code": LANGUAGE_PL,
            "include_seed_keyword": True,
            "include_serp_info": False,
            "limit": args.limit,
        }]
        res = call_api("POST", "/v3/dataforseo_labs/google/keyword_suggestions/live", body)
        cost = res.get("cost", 0)
        total_cost += cost
        track_cost(f"suggestions:{seed}", cost, {"limit": args.limit})
        if res["status_code"] != 20000:
            print(f"[{seed}] ERROR {res['status_code']}: {res['status_message']}", file=sys.stderr)
            continue
        task = res["tasks"][0]
        if task["status_code"] != 20000:
            print(f"[{seed}] task error: {task['status_message']}", file=sys.stderr)
            continue
        items = task["result"][0].get("items") or []
        print(f"[{seed:25s}] {len(items):4d} kw | cost ${cost:.4f}")
        for it in items:
            all_results.append(_flatten_keyword_item(it, seed=seed))

    print(f"\nTotal: {len(all_results)} keywords | cost ${total_cost:.4f}")
    if args.save:
        out = save_json("suggestions", all_results)
        print(f"Saved: {out}")
    return all_results


def cmd_ideas(args):
    """Labs Keyword Ideas: semantically related, broader pool."""
    body = [{
        "keywords": args.seeds,
        "location_code": LOCATION_PL,
        "language_code": LANGUAGE_PL,
        "limit": args.limit,
        "include_serp_info": False,
    }]
    res = call_api("POST", "/v3/dataforseo_labs/google/keyword_ideas/live", body)
    cost = res.get("cost", 0)
    track_cost(f"ideas:{','.join(args.seeds)}", cost, {"limit": args.limit})
    if res["status_code"] != 20000:
        sys.exit(f"ERROR: {res['status_message']}")
    items = res["tasks"][0]["result"][0].get("items") or []
    print(f"[ideas] {len(items)} keywords | cost ${cost:.4f}")
    flat = [_flatten_keyword_item(it) for it in items]
    if args.save:
        out = save_json("ideas", flat)
        print(f"Saved: {out}")
    return flat


def cmd_ranked(args):
    """Labs Ranked Keywords: which keywords a domain ranks for in Google PL."""
    body = [{
        "target": args.domain,
        "location_code": LOCATION_PL,
        "language_code": LANGUAGE_PL,
        "limit": args.limit,
        "load_rank_absolute": True,
        "ignore_synonyms": True,
        "filters": [["ranked_serp_element.serp_item.rank_absolute", "<=", 30]],
    }]
    res = call_api("POST", "/v3/dataforseo_labs/google/ranked_keywords/live", body)
    cost = res.get("cost", 0)
    track_cost(f"ranked:{args.domain}", cost, {"limit": args.limit})
    if res["status_code"] != 20000:
        sys.exit(f"ERROR: {res['status_message']}")
    task_result = res["tasks"][0]["result"][0]
    items = task_result.get("items") or []
    print(f"[{args.domain}] {len(items)} ranked keywords | cost ${cost:.4f}")
    print(f"Total ranked: {fmt_int(task_result.get('total_count'))}")
    flat = []
    for it in items:
        kw = it.get("keyword_data", {}).get("keyword_info", {}) or {}
        serp = it.get("ranked_serp_element", {}).get("serp_item", {}) or {}
        flat.append({
            "keyword": it.get("keyword_data", {}).get("keyword"),
            "rank": serp.get("rank_absolute"),
            "url": serp.get("url"),
            "search_volume": kw.get("search_volume"),
            "cpc": kw.get("cpc"),
            "competition": kw.get("competition"),
        })
    if args.save:
        out = save_json(f"ranked-{args.domain.replace('.', '_')}", flat)
        print(f"Saved: {out}")
    return flat


def load_seeds():
    if SEEDS_FILE.exists():
        seeds = [s.strip() for s in SEEDS_FILE.read_text().splitlines() if s.strip() and not s.startswith("#")]
        if seeds:
            return seeds
    return DEFAULT_SEEDS


def _iso_week():
    now = datetime.now()
    y, w, _ = now.isocalendar()
    return f"{y}-W{w:02d}", now.strftime("%Y-%m-%d")


def cmd_weekly(args):
    """Weekly DataForSEO research — suggestions per seed + ranked dokodu.it + raport MD."""
    seeds = load_seeds()
    week_id, today = _iso_week()
    WEEKLY_DIR.mkdir(parents=True, exist_ok=True)

    # 0. Balance + estymacja kosztu
    res = call_api("GET", "/v3/appendix/user_data")
    balance = res["tasks"][0]["result"][0]["money"]["balance"]
    est = len(seeds) * (0.0115 + WEEKLY_SUGGESTION_LIMIT * 0.0001) + (0.025 + WEEKLY_RANKED_LIMIT * 0.0001)
    print(f"Week: {week_id} | seeds: {len(seeds)} | balance: ${balance:.2f}")
    print(f"Estymowany koszt: ${est:.4f} (próg ostrzeżenia: ${WEEKLY_BUDGET_USD})")
    if est > WEEKLY_BUDGET_USD and not args.confirm:
        sys.exit(f"Estymowany koszt > ${WEEKLY_BUDGET_USD}. Dodaj --confirm jeśli OK.")
    if balance < est * 1.5:
        sys.exit(f"Balance ${balance:.2f} za niski na bezpieczne wykonanie (potrzeba ~${est*1.5:.2f}).")

    # 1. Suggestions per seed
    all_sugg = []
    for seed in seeds:
        body = [{
            "keyword": seed,
            "location_code": LOCATION_PL,
            "language_code": LANGUAGE_PL,
            "include_seed_keyword": True,
            "include_serp_info": False,
            "limit": WEEKLY_SUGGESTION_LIMIT,
        }]
        r = call_api("POST", "/v3/dataforseo_labs/google/keyword_suggestions/live", body)
        cost = r.get("cost", 0)
        track_cost(f"weekly-suggestions:{seed}", cost, {"week": week_id})
        if r["status_code"] != 20000:
            print(f"  [{seed}] ERROR: {r['status_message']}", file=sys.stderr)
            continue
        items = r["tasks"][0]["result"][0].get("items") or []
        for it in items:
            all_sugg.append(_flatten_keyword_item(it, seed=seed))
        print(f"  [{seed:25s}] {len(items):4d} kw | ${cost:.4f}")

    # 2. Ranked dokodu.it
    body = [{
        "target": "dokodu.it",
        "location_code": LOCATION_PL,
        "language_code": LANGUAGE_PL,
        "limit": WEEKLY_RANKED_LIMIT,
        "load_rank_absolute": True,
        "ignore_synonyms": True,
        "filters": [["ranked_serp_element.serp_item.rank_absolute", "<=", 30]],
    }]
    r = call_api("POST", "/v3/dataforseo_labs/google/ranked_keywords/live", body)
    cost = r.get("cost", 0)
    track_cost("weekly-ranked:dokodu.it", cost, {"week": week_id})
    ranked = []
    if r["status_code"] == 20000:
        for it in r["tasks"][0]["result"][0].get("items") or []:
            kw = it.get("keyword_data", {}).get("keyword_info", {}) or {}
            serp = it.get("ranked_serp_element", {}).get("serp_item", {}) or {}
            ranked.append({
                "keyword": it.get("keyword_data", {}).get("keyword"),
                "rank": serp.get("rank_absolute"),
                "url": serp.get("url"),
                "search_volume": kw.get("search_volume"),
                "cpc": kw.get("cpc"),
                "competition": kw.get("competition"),
            })
    print(f"  [ranked dokodu.it] {len(ranked)} kw | ${cost:.4f}")

    # 3. Raw JSON snapshot
    snapshot = {
        "week": week_id,
        "date": today,
        "seeds": seeds,
        "suggestions": all_sugg,
        "ranked": ranked,
    }
    raw_out = WEEKLY_DIR / f"{week_id}-raw.json"
    raw_out.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2))

    # 4. Analiza — gapy i top picks
    ranked_set = {r["keyword"].lower() for r in ranked}

    def is_useful(it):
        v = it.get("search_volume") or 0
        if v < 30:
            return False
        return it.get("main_intent") in ("commercial", "informational", "transactional")

    useful = [it for it in all_sugg if is_useful(it)]
    gaps = [it for it in useful if it["keyword"].lower() not in ranked_set]
    gaps_top = sorted(gaps, key=lambda x: -x["search_volume"])[:30]
    commercial_gaps = [it for it in gaps if it.get("main_intent") in ("commercial", "transactional")]
    commercial_top = sorted(commercial_gaps, key=lambda x: -x["search_volume"])[:15]
    ranked_sorted = sorted([r for r in ranked if r.get("rank")], key=lambda x: x["rank"])[:20]

    # 5. Raport MD
    total_cost = sum(e["cost"] for e in json.loads(BUDGET_FILE.read_text()) if e.get("meta", {}).get("week") == week_id)
    md = []
    md.append(f"---")
    md.append(f"type: report")
    md.append(f"source: dataforseo")
    md.append(f"week: {week_id}")
    md.append(f"generated: {today}")
    md.append(f"cost_usd: {total_cost:.4f}")
    md.append(f"---\n")
    md.append(f"# DataForSEO Weekly — {week_id}\n")
    md.append(f"**Data:** {today} | **Seedy:** {', '.join(seeds)} | **Koszt tygodnia:** ${total_cost:.4f}\n")
    md.append(f"- Suggestions zebranych: {len(all_sugg)}")
    md.append(f"- Sensownych (vol≥30, non-nav): {len(useful)}")
    md.append(f"- Gapy (nie rankujemy w top 30): {len(gaps)}")
    md.append(f"- Już rankujemy: {len(ranked)}\n")

    md.append("## 🎯 Top 30 GAPÓW — frazy do napisania\n")
    md.append("| Vol | Intent | Comp | CPC | Seed | Keyword |")
    md.append("|----:|--------|------|----:|------|---------|")
    for it in gaps_top:
        md.append(f"| {it['search_volume']} | {it.get('main_intent','-')} | {it.get('competition_level','-')} | ${it.get('cpc') or 0:.2f} | {it['seed']} | {it['keyword']} |")
    md.append("")

    md.append("## 💰 Top 15 COMMERCIAL/TRANSACTIONAL GAPS — lead gen\n")
    md.append("| Vol | CPC | Comp | Seed | Keyword |")
    md.append("|----:|----:|------|------|---------|")
    for it in commercial_top:
        md.append(f"| {it['search_volume']} | ${it.get('cpc') or 0:.2f} | {it.get('competition_level','-')} | {it['seed']} | {it['keyword']} |")
    md.append("")

    md.append("## 📈 Top 20 RANKED dokodu.it (top 30 SERP PL)\n")
    md.append("| # | Vol | Keyword | URL |")
    md.append("|---|----:|---------|-----|")
    for it in ranked_sorted:
        url = (it.get("url") or "").replace("https://dokodu.it", "")
        md.append(f"| #{it['rank']} | {it.get('search_volume') or '-'} | {it['keyword']} | {url} |")
    md.append("")

    md.append("## 🔄 Diff vs poprzedni tydzień\n")
    prev_files = sorted(WEEKLY_DIR.glob("*-raw.json"))
    prev_files = [p for p in prev_files if p.stem != f"{week_id}-raw"]
    if prev_files:
        prev = json.loads(prev_files[-1].read_text())
        prev_ranked = {r["keyword"]: r["rank"] for r in prev.get("ranked", [])}
        cur_ranked = {r["keyword"]: r["rank"] for r in ranked}
        new_kw = [k for k in cur_ranked if k not in prev_ranked]
        lost_kw = [k for k in prev_ranked if k not in cur_ranked]
        moved_up = [(k, prev_ranked[k], cur_ranked[k]) for k in cur_ranked if k in prev_ranked and cur_ranked[k] < prev_ranked[k]]
        moved_down = [(k, prev_ranked[k], cur_ranked[k]) for k in cur_ranked if k in prev_ranked and cur_ranked[k] > prev_ranked[k]]
        md.append(f"vs `{prev_files[-1].stem}`:\n")
        md.append(f"- ➕ Nowe w top 30: {len(new_kw)}")
        md.append(f"- ➖ Wypadły z top 30: {len(lost_kw)}")
        md.append(f"- ⬆️ Awans pozycji: {len(moved_up)}")
        md.append(f"- ⬇️ Spadek pozycji: {len(moved_down)}")
        if new_kw[:5]:
            md.append(f"\nNowe: {', '.join(new_kw[:5])}")
        if moved_up[:5]:
            md.append(f"Awansowały: {', '.join(f'{k} ({a}→{b})' for k,a,b in moved_up[:5])}")
        if moved_down[:5]:
            md.append(f"Spadły: {', '.join(f'{k} ({a}→{b})' for k,a,b in moved_down[:5])}")
    else:
        md.append("Brak poprzedniego snapshota — to pierwszy weekly run. Diff dostępny od następnego tygodnia.")

    md.append("\n## Następne kroki\n")
    md.append(f"1. Wybierz 2-3 frazy z **Top GAPS** → `/seo-plan-post [keyword]` → brief artykułu")
    md.append(f"2. Sprawdź czy któraś z **commercial gaps** koreluje z istniejącą propozycją w `SEO_Ideas_Bank.md`")
    md.append(f"3. Jeśli któraś rankująca fraza spadła → optymalizacja istniejącego artykułu")
    md.append(f"4. Zaplanuj kolejny weekly: `python3 scripts/dataforseo_fetch.py weekly` (piątek razem z `/seo-weekly`)\n")

    md_out = WEEKLY_DIR / f"{week_id}.md"
    md_out.write_text("\n".join(md))
    print(f"\n✅ Raw: {raw_out}")
    print(f"✅ Raport: {md_out}")
    print(f"💰 Koszt tygodnia: ${total_cost:.4f}")


def main():
    ap = argparse.ArgumentParser(description="DataForSEO client for dokodu.it")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("check", help="Account balance + cumulative spending").set_defaults(func=cmd_check)
    sub.add_parser("budget", help="Show local cost log").set_defaults(func=cmd_budget)

    sp = sub.add_parser("weekly", help="Weekly research: suggestions + ranked + report")
    sp.add_argument("--confirm", action="store_true", help="Required if estimated cost > threshold")
    sp.set_defaults(func=cmd_weekly)

    sp = sub.add_parser("suggestions", help="Long-tail keyword suggestions (Labs)")
    sp.add_argument("seeds", nargs="+")
    sp.add_argument("--limit", type=int, default=700)
    sp.add_argument("--save", action="store_true")
    sp.set_defaults(func=cmd_suggestions)

    sp = sub.add_parser("ideas", help="Semantic keyword ideas (Labs, batch seeds)")
    sp.add_argument("seeds", nargs="+")
    sp.add_argument("--limit", type=int, default=700)
    sp.add_argument("--save", action="store_true")
    sp.set_defaults(func=cmd_ideas)

    sp = sub.add_parser("ranked", help="Keywords a domain ranks for (Labs)")
    sp.add_argument("domain")
    sp.add_argument("--limit", type=int, default=500)
    sp.add_argument("--save", action="store_true")
    sp.set_defaults(func=cmd_ranked)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
