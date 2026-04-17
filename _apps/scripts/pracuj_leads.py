#!/usr/bin/env python3
"""
pracuj_leads.py — Pobiera leady z Pracuj.pl (firmy rekrutujące na AI/RPA/automatyzację)

Generuje CSV z firmami szukającymi specjalistów od automatyzacji — gotowe linki
LinkedIn do prospectingu (firma + IT Manager + Operations Manager).

Użycie:
    # Podgląd — wyświetl wyniki bez zapisu
    python3 pracuj_leads.py

    # Zapisz CSV do BRAIN (20_AREAS/AREA_Marketing_Sales/Leads_Pracuj_YYYY-MM-DD.csv)
    python3 pracuj_leads.py --save

    # Ogłoszenia z ostatnich 7 dni
    python3 pracuj_leads.py --save --days 7

    # Własne słowa kluczowe
    python3 pracuj_leads.py --save --keywords "n8n,Make.com,Zapier"

    # Więcej stron wyników (domyślnie 3)
    python3 pracuj_leads.py --save --max-pages 5

Podejście techniczne:
    1. Próbuje requests + parsing __NEXT_DATA__ JSON (szybkie, bez przeglądarki)
    2. Jeśli Pracuj.pl blokuje (403/captcha) — fallback na Playwright (headless Chrome)

Wymagania:
    - requests, beautifulsoup4 (pip install requests beautifulsoup4)
    - playwright (opcjonalny fallback): pip install playwright && playwright install chromium
"""

import argparse
import csv
import json
import re
import sys
import time
import random
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Konfiguracja
# ---------------------------------------------------------------------------

DEFAULT_KEYWORDS = [
    "automatyzacja procesów biznesowych",
    "RPA",
    "Power Automate",
    "automatyzacja IT",
    "integracja systemów",
    "SAP",
    "wdrożenie automatyzacji",
]

CSV_FIELDNAMES = [
    "company_name",
    "sample_job_title",
    "last_posted",
    "source_keyword",
    "pracuj_profile",
    "linkedin_company",
    "linkedin_contact_1_IT_Manager",
    "linkedin_contact_2_Operations_Manager",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
}

BRAIN_DIR = Path(__file__).resolve().parent.parent
SALES_DIR = BRAIN_DIR / "20_AREAS" / "AREA_Marketing_Sales"


# ---------------------------------------------------------------------------
# LinkedIn URL builders
# ---------------------------------------------------------------------------

def linkedin_company_url(name: str) -> str:
    return f"https://www.linkedin.com/search/results/companies/?keywords={urllib.parse.quote(name)}"


def linkedin_person_url(role: str, company: str) -> str:
    return f"https://www.linkedin.com/search/results/people/?keywords={urllib.parse.quote(f'{role} {company}')}"


# ---------------------------------------------------------------------------
# Pracuj.pl URL builder
# ---------------------------------------------------------------------------

def build_search_url(keyword: str, page: int = 1) -> str:
    encoded = urllib.parse.quote(keyword)
    url = f"https://www.pracuj.pl/praca/{encoded};kw"
    if page > 1:
        url += f"?pn={page}"
    return url


# ---------------------------------------------------------------------------
# Metoda 1: requests + __NEXT_DATA__ JSON parsing
# ---------------------------------------------------------------------------

def extract_offers_from_html(html: str) -> list[dict]:
    """Parsuje __NEXT_DATA__ z HTML i wyciąga oferty pracy."""
    soup = BeautifulSoup(html, "html.parser")
    script = soup.find("script", id="__NEXT_DATA__")
    if not script or not script.string:
        return []

    try:
        data = json.loads(script.string)
    except json.JSONDecodeError:
        return []

    # Nawigacja po strukturze Next.js
    dehydrated = data.get("props", {}).get("pageProps", {}).get("dehydratedState", {})
    queries = dehydrated.get("queries", [])

    for q in queries:
        qk = q.get("queryKey", [])
        if qk and qk[0] == "jobOffers":
            state_data = q.get("state", {}).get("data", {})
            return state_data.get("groupedOffers", [])

    return []


def fetch_page_requests(keyword: str, page: int = 1) -> list[dict]:
    """Pobiera jedną stronę wyników przez requests."""
    url = build_search_url(keyword, page)
    try:
        session = requests.Session()
        session.headers.update(HEADERS)
        resp = session.get(url, timeout=15)

        if resp.status_code == 403:
            return []  # Zablokowany — fallback na Playwright
        if resp.status_code != 200:
            print(f"  WARN: HTTP {resp.status_code} dla '{keyword}' strona {page}", file=sys.stderr)
            return []

        # Sprawdź czy to nie jest strona captcha/challenge
        if "challenge" in resp.text[:2000].lower() or len(resp.text) < 5000:
            return []

        return extract_offers_from_html(resp.text)

    except requests.RequestException as e:
        print(f"  WARN: request error: {e}", file=sys.stderr)
        return []


def scrape_with_requests(keywords: list[str], max_pages: int) -> tuple[dict, bool]:
    """
    Scrapuje przez requests. Zwraca (companies_dict, success).
    success=False oznacza że requests nie działa i trzeba fallback.
    """
    companies: dict[str, dict] = {}
    blocked = False

    for kw in keywords:
        print(f"\n  Szukam: '{kw}'...")
        for pn in range(1, max_pages + 1):
            offers = fetch_page_requests(kw, pn)

            if not offers and pn == 1:
                # Prawdopodobnie zablokowany
                blocked = True
                print(f"    Brak wynikow — prawdopodobnie zablokowany (403/captcha)")
                break

            new = 0
            for offer in offers:
                cname = offer.get("companyName", "").strip().strip('"')
                if not cname or cname in companies:
                    continue
                companies[cname] = {
                    "company_name": cname,
                    "sample_job_title": offer.get("jobTitle", ""),
                    "last_posted": (offer.get("lastPublicated", "") or "")[:10],
                    "source_keyword": kw,
                    "pracuj_profile": offer.get("companyProfileAbsoluteUri", ""),
                }
                new += 1

            print(f"    Strona {pn}: {len(offers)} ofert, {new} nowych firm")
            if len(offers) < 5:
                break
            time.sleep(random.uniform(1.0, 3.0))

        if blocked:
            break

    return companies, not blocked


# ---------------------------------------------------------------------------
# Metoda 2: Playwright fallback (headless Chrome)
# ---------------------------------------------------------------------------

def scrape_with_playwright(keywords: list[str], max_pages: int) -> dict:
    """Fallback: scrapuje przez Playwright z headless Chrome."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "\nERROR: Requests zablokowany, a Playwright nie jest zainstalowany.\n"
            "Zainstaluj: pip install playwright && playwright install chromium\n"
            "Lub uzyj proxy/VPN.",
            file=sys.stderr,
        )
        sys.exit(1)

    companies: dict[str, dict] = {}

    with sync_playwright() as pw:
        for kw in keywords:
            browser = pw.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-blink-features=AutomationControlled"],
            )
            ctx = browser.new_context(
                user_agent=HEADERS["User-Agent"],
                viewport={"width": 1280, "height": 800},
                locale="pl-PL",
            )
            try:
                print(f"\n  [Playwright] Szukam: '{kw}'...")
                for pn in range(1, max_pages + 1):
                    page = ctx.new_page()
                    page.add_init_script(
                        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
                    )
                    url = build_search_url(kw, pn)
                    try:
                        page.goto(url, wait_until="domcontentloaded", timeout=30000)
                        page.wait_for_timeout(2500)

                        offers = page.evaluate("""() => {
                            try {
                                const el = document.getElementById("__NEXT_DATA__");
                                if (!el) return [];
                                const data = JSON.parse(el.textContent);
                                const ds = data.props.pageProps.dehydratedState;
                                if (!ds || !ds.queries) return [];
                                const q = ds.queries.find(q => q.queryKey[0] === "jobOffers");
                                if (!q || !q.state.data) return [];
                                return q.state.data.groupedOffers || [];
                            } catch(e) { return []; }
                        }""")

                        new = 0
                        for offer in (offers or []):
                            cname = offer.get("companyName", "").strip().strip('"')
                            if not cname or cname in companies:
                                continue
                            companies[cname] = {
                                "company_name": cname,
                                "sample_job_title": offer.get("jobTitle", ""),
                                "last_posted": (offer.get("lastPublicated", "") or "")[:10],
                                "source_keyword": kw,
                                "pracuj_profile": offer.get("companyProfileAbsoluteUri", ""),
                            }
                            new += 1

                        print(f"    Strona {pn}: {len(offers or [])} ofert, {new} nowych firm")
                        if len(offers or []) < 5:
                            break

                    except Exception as e:
                        print(f"    WARN: {e}", file=sys.stderr)
                    finally:
                        page.close()

                    time.sleep(random.uniform(1.0, 2.5))
            finally:
                browser.close()

    return companies


# ---------------------------------------------------------------------------
# Enrichment + filtering
# ---------------------------------------------------------------------------

def enrich_linkedin(companies: dict) -> list[dict]:
    """Dodaje linki LinkedIn do każdej firmy."""
    for c in companies.values():
        name = c["company_name"]
        c["linkedin_company"] = linkedin_company_url(name)
        c["linkedin_contact_1_IT_Manager"] = linkedin_person_url("IT Manager", name)
        c["linkedin_contact_2_Operations_Manager"] = linkedin_person_url("Operations Manager", name)
    return list(companies.values())


def filter_by_days(companies: list[dict], days: int) -> list[dict]:
    """Filtruje firmy po dacie publikacji ogłoszenia."""
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    filtered = [c for c in companies if c.get("last_posted", "") >= cutoff]
    if len(filtered) < len(companies):
        print(f"  Filtr dat: {len(companies)} -> {len(filtered)} (ostatnie {days} dni)")
    return filtered


# ---------------------------------------------------------------------------
# CSV output
# ---------------------------------------------------------------------------

def save_csv(companies: list[dict], output_path: str) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(companies)
    print(f"\nZapisano {len(companies)} firm do: {output_path}")


def print_summary(companies: list[dict]) -> None:
    print(f"\nZnaleziono {len(companies)} unikalnych firm:\n")
    for i, c in enumerate(companies[:20], 1):
        print(f"  {i:3}. {c['company_name'][:50]:<50} | {c['sample_job_title'][:45]}")
    if len(companies) > 20:
        print(f"  ... i {len(companies) - 20} wiecej")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Pobiera leady z Pracuj.pl — firmy rekrutujace na AI/RPA/automatyzacje"
    )
    parser.add_argument(
        "--save", action="store_true",
        help="Zapisz CSV do 20_AREAS/AREA_Marketing_Sales/Leads_Pracuj_YYYY-MM-DD.csv"
    )
    parser.add_argument(
        "--days", type=int, default=14,
        help="Ogłoszenia z ostatnich N dni (domyslnie: 14)"
    )
    parser.add_argument(
        "--keywords", type=str, default=None,
        help='Nadpisz slowa kluczowe, rozdzielone przecinkami: "RPA,SAP,n8n"'
    )
    parser.add_argument(
        "--max-pages", type=int, default=3,
        help="Max stron wynikow na fraze (domyslnie: 3)"
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="Nadpisz sciezke CSV (domyslnie: auto w BRAIN)"
    )
    parser.add_argument(
        "--force-playwright", action="store_true",
        help="Wymus uzycie Playwright zamiast requests"
    )
    args = parser.parse_args()

    # Parse keywords
    if args.keywords:
        keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    else:
        keywords = DEFAULT_KEYWORDS

    print("=" * 65)
    print("DOKODU Lead Scraper — Pracuj.pl")
    print(f"Frazy: {len(keywords)} | Max stron: {args.max_pages} | Dni: {args.days}")
    print("=" * 65)

    # Scraping — requests first, Playwright fallback
    if args.force_playwright:
        print("\n[Tryb: Playwright]")
        companies = scrape_with_playwright(keywords, args.max_pages)
    else:
        print("\n[Tryb: requests]")
        companies, success = scrape_with_requests(keywords, args.max_pages)
        if not success:
            print("\nRequests zablokowany — przelaczam na Playwright...")
            companies = scrape_with_playwright(keywords, args.max_pages)

    if not companies:
        print("\nNie znaleziono zadnych firm. Sprobuj innych slow kluczowych lub --force-playwright.")
        sys.exit(1)

    # Enrich + filter
    results = enrich_linkedin(companies)
    results = filter_by_days(results, args.days)

    # Sort — najnowsze pierwsze
    results.sort(key=lambda x: x.get("last_posted", ""), reverse=True)

    # Output
    print_summary(results)

    if args.save or args.output:
        if args.output:
            out_path = args.output
        else:
            date_str = datetime.now().strftime("%Y-%m-%d")
            out_path = str(SALES_DIR / f"Leads_Pracuj_{date_str}.csv")
        save_csv(results, out_path)
        print(f"\nNastepny krok: otworz CSV i kliknij LinkedIn URL-e zeby znalezc kontakty.")
    else:
        print(f"\nUzyj --save zeby zapisac CSV, lub --output /sciezka/plik.csv")


if __name__ == "__main__":
    main()
