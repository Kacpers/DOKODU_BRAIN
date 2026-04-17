#!/usr/bin/env python3
"""
pracuj_scraper.py — Scraper firm z pracuj.pl szukających automatyzacji/SAP/AI
Wynik: CSV z nazwami firm + gotowe URL-e LinkedIn do prospectingu

Użycie:
    python3 pracuj_scraper.py
    python3 pracuj_scraper.py --output /tmp/leads.csv
    python3 pracuj_scraper.py --keywords "n8n automatyzacja" "RPA SAP" --max-pages 3
"""

import argparse
import csv
import json
import re
import sys
import time
import urllib.parse
from datetime import datetime
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("ERROR: Playwright nie jest zainstalowany. Uruchom: pip install playwright && playwright install chromium")
    sys.exit(1)

# Domyślne frazy kluczowe — firmy szukające automatyzacji/AI/SAP
DEFAULT_KEYWORDS = [
    "automatyzacja procesów biznesowych",
    "RPA",
    "SAP",
    "Power Automate",
    "integracja systemów",
    "automatyzacja IT",
    "wdrożenie automatyzacji",
]

# Kategorie branżowe pracuj.pl (cc= param)
# 5002 = Produkcja przemysłowa, 5003 = Logistyka, 5004 = Finanse
CATEGORIES = {
    "produkcja": "5002",
    "logistyka": "5003",
    "it": "5013",
    "all": None,
}

# Stanowiska decydentów do szukania na LinkedIn
DECISION_MAKER_ROLES = [
    "IT Manager",
    "Operations Manager",
    "Dyrektor IT",
    "Kierownik IT",
    "Kierownik operacyjny",
    "CTO",
    "Head of Operations",
]


def make_browser_context(playwright):
    browser = playwright.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-blink-features=AutomationControlled"],
    )
    ctx = browser.new_context(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        viewport={"width": 1280, "height": 800},
        locale="pl-PL",
    )
    return browser, ctx


def scrape_keyword(ctx, keyword, category_code=None, page_num=1):
    """Scrapuje jedną stronę wyników dla danego słowa kluczowego."""
    page = ctx.new_page()
    page.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    encoded_kw = urllib.parse.quote(keyword)
    url = f"https://www.pracuj.pl/praca/{encoded_kw};kw"
    if category_code:
        url += f"?cc={category_code}"
    if page_num > 1:
        sep = "&" if "?" in url else "?"
        url += f"{sep}pn={page_num}"

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
            } catch(e) {
                return [];
            }
        }""")

        return offers or []

    except Exception as e:
        print(f"  WARN: błąd dla '{keyword}': {e}", file=sys.stderr)
        return []
    finally:
        page.close()


def build_linkedin_search_url(company_name, role):
    """Generuje URL wyszukiwania osoby na LinkedIn."""
    query = urllib.parse.quote(f"{role} {company_name}")
    return f"https://www.linkedin.com/search/results/people/?keywords={query}"


def build_linkedin_company_url(company_name):
    """Generuje URL wyszukiwania firmy na LinkedIn."""
    query = urllib.parse.quote(company_name)
    return f"https://www.linkedin.com/search/results/companies/?keywords={query}"


def scrape_all(keywords, max_pages=2, category=None):
    """Główna funkcja scrapująca wszystkie słowa kluczowe."""
    category_code = CATEGORIES.get(category) if category else None

    all_companies = {}  # companyId -> dane firmy

    with sync_playwright() as pw:
        for kw in keywords:
            # Świeży kontekst dla każdego słowa kluczowego — unika problemów z cookies/CF
            browser, ctx = make_browser_context(pw)
            try:
                print(f"\n🔍 Szukam: '{kw}'...")
                for pn in range(1, max_pages + 1):
                    offers = scrape_keyword(ctx, kw, category_code, pn)
                    new_count = 0
                    for offer in offers:
                        cid = offer.get("companyId")
                        if not cid or cid in all_companies:
                            continue
                        all_companies[cid] = {
                            "company_name": offer.get("companyName", "").strip('"'),
                            "company_id": cid,
                            "pracuj_profile": offer.get("companyProfileAbsoluteUri", ""),
                            "sample_job_title": offer.get("jobTitle", ""),
                            "last_posted": offer.get("lastPublicated", "")[:10] if offer.get("lastPublicated") else "",
                            "source_keyword": kw,
                        }
                        new_count += 1

                    print(f"  Strona {pn}: {len(offers)} ofert, {new_count} nowych firm")
                    if len(offers) < 5:  # Mało wyników — nie ma sensu iść dalej
                        break
                    time.sleep(1.5)  # Grzeczny scraper
            finally:
                browser.close()

    return list(all_companies.values())


def enrich_with_linkedin(companies):
    """Dodaje LinkedIn URL-e dla każdej firmy."""
    for company in companies:
        name = company["company_name"]
        company["linkedin_company"] = build_linkedin_company_url(name)
        # Generuj URL-e dla top 2 ról
        for i, role in enumerate(DECISION_MAKER_ROLES[:2], 1):
            company[f"linkedin_contact_{i}_{role.replace(' ', '_')}"] = (
                build_linkedin_search_url(name, role)
            )
    return companies


def save_csv(companies, output_path):
    if not companies:
        print("Brak firm do zapisania.")
        return

    fieldnames = [
        "company_name",
        "sample_job_title",
        "last_posted",
        "source_keyword",
        "pracuj_profile",
        "linkedin_company",
    ] + [k for k in companies[0].keys() if k.startswith("linkedin_contact_")]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(companies)

    print(f"\n✅ Zapisano {len(companies)} firm do: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Scraper firm z pracuj.pl dla Dokodu prospectingu")
    parser.add_argument(
        "--keywords", nargs="+", default=DEFAULT_KEYWORDS,
        help="Frazy do wyszukania (domyślnie: automatyzacja SAP RPA n8n...)"
    )
    parser.add_argument(
        "--output", default=None,
        help="Ścieżka do pliku CSV (domyślnie: BRAIN/20_AREAS/AREA_Marketing_Sales/Leads_Pracuj_<data>.csv)"
    )
    parser.add_argument(
        "--max-pages", type=int, default=2,
        help="Max stron na frazę (domyślnie: 2)"
    )
    parser.add_argument(
        "--category", choices=list(CATEGORIES.keys()), default=None,
        help="Branża: produkcja, logistyka, it, all (domyślnie: all)"
    )
    args = parser.parse_args()

    # Domyślna ścieżka output
    if not args.output:
        brain_dir = Path(__file__).parent.parent
        sales_dir = brain_dir / "20_AREAS" / "AREA_Marketing_Sales"
        sales_dir.mkdir(parents=True, exist_ok=True)
        date_str = datetime.now().strftime("%Y-%m-%d")
        args.output = str(sales_dir / f"Leads_Pracuj_{date_str}.csv")

    print("=" * 60)
    print("DOKODU Prospecting Scraper — pracuj.pl")
    print(f"Frazy: {len(args.keywords)} | Max stron: {args.max_pages}")
    print("=" * 60)

    companies = scrape_all(args.keywords, max_pages=args.max_pages, category=args.category)

    if not companies:
        print("\n❌ Nie znaleziono żadnych firm. Spróbuj innych słów kluczowych.")
        return

    companies = enrich_with_linkedin(companies)

    # Posortuj po dacie (najnowsze pierwsze)
    companies.sort(key=lambda x: x.get("last_posted", ""), reverse=True)

    print(f"\n📊 Łącznie znaleziono: {len(companies)} unikalnych firm")
    print("\nTop 10 firm:")
    for i, c in enumerate(companies[:10], 1):
        print(f"  {i:2}. {c['company_name'][:50]:<50} | {c['sample_job_title'][:40]}")

    save_csv(companies, args.output)
    print(f"\nNastępny krok: otwórz CSV i kliknij LinkedIn URL-e żeby znaleźć kontakty.")


if __name__ == "__main__":
    main()
