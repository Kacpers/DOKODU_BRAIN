#!/usr/bin/env python3
"""
short_domain_finder.py — szuka wolnych krótkich domen pod shortener Dokodu.

Sprawdza dostępność przez RDAP (IANA bootstrap), a dla TLD bez RDAP
robi fallback przez DNS + WHOIS (port 43).

Output: CSV + posortowane wolne domeny w stdout.
"""
from __future__ import annotations

import csv
import json
import socket
import sys
import time
from pathlib import Path
from typing import Optional

import requests

# ---------- KONFIG ----------

CANDIDATES = [
    "dkd", "doko", "dkdu",
    "dko", "dku", "dok", "dkdo", "dokd",
    "kdu", "kod", "dkod", "dokk",
    "dko2", "go2dk",
]

# TLD pogrupowane wg charakteru. Ceny orientacyjne (renewal, PLN/rok, 2026).
TLDS = {
    "cheap-generic": {
        "xyz": 50, "online": 180, "site": 130, "shop": 200,
        "click": 35, "link": 50, "fun": 70, "icu": 35,
        "space": 40, "tech": 250, "store": 350,
    },
    "country-pl-eu": {
        "pl": 90, "com.pl": 50, "eu": 50, "de": 50,
        "it": 50, "co.uk": 50, "uk": 50, "es": 50,
    },
    "standard": {
        "com": 60, "net": 70, "org": 70, "info": 80, "biz": 80,
    },
    "shortener-friendly": {
        "co": 130, "io": 200, "me": 90, "to": 1500,
        "sh": 350, "ly": 400, "so": 350, "cc": 130,
        "tv": 200, "ai": 400, "app": 80, "dev": 70,
        "do": 600, "id": 200, "im": 150,
    },
}

IANA_RDAP_BOOTSTRAP = "https://data.iana.org/rdap/dns.json"
RDAP_CACHE = Path("/tmp/rdap_bootstrap.json")
CACHE_TTL = 86400  # 24h

# WHOIS endpoints dla TLD bez RDAP
WHOIS_SERVERS = {
    "pl": "whois.dns.pl",
    "com.pl": "whois.dns.pl",
    "to": "whois.tonic.to",
    "im": "whois.nic.im",
    "do": "whois.nic.do",
}

# Frazy w odpowiedzi WHOIS sugerujące, że domena jest WOLNA
WHOIS_FREE_MARKERS = [
    "no information available",
    "no match",
    "not found",
    "no entries found",
    "no data found",
    "available",
    "free",
    "status: available",
    "no object found",
    "domain not found",
]

# ---------- RDAP ----------

def load_rdap_bootstrap() -> dict:
    if RDAP_CACHE.exists() and (time.time() - RDAP_CACHE.stat().st_mtime) < CACHE_TTL:
        return json.loads(RDAP_CACHE.read_text())
    r = requests.get(IANA_RDAP_BOOTSTRAP, timeout=10)
    r.raise_for_status()
    RDAP_CACHE.write_text(r.text)
    return r.json()


def get_rdap_url(tld: str, bootstrap: dict) -> Optional[str]:
    # IANA bootstrap obsługuje tylko jednoczłonowe TLD (np. "pl", nie "com.pl")
    base_tld = tld.split(".")[-1]
    for service in bootstrap.get("services", []):
        tlds, urls = service[0], service[1]
        if base_tld in tlds and urls:
            return urls[0].rstrip("/")
    return None


def check_rdap(domain: str, rdap_url: str) -> tuple[Optional[bool], str]:
    try:
        r = requests.get(
            f"{rdap_url}/domain/{domain}",
            timeout=8,
            headers={"Accept": "application/rdap+json"},
        )
        if r.status_code == 404:
            return True, "RDAP-404"
        if r.status_code == 200:
            return False, "RDAP-200"
        if r.status_code == 429:
            return None, "RDAP-429-rate-limit"
        return None, f"RDAP-{r.status_code}"
    except requests.RequestException as e:
        return None, f"RDAP-error:{type(e).__name__}"


# ---------- WHOIS (port 43) ----------

def query_whois(domain: str, server: str) -> Optional[str]:
    try:
        with socket.create_connection((server, 43), timeout=8) as s:
            s.sendall(f"{domain}\r\n".encode())
            data = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                data += chunk
        return data.decode("utf-8", errors="replace")
    except (socket.error, OSError):
        return None


def check_whois(domain: str, tld: str) -> tuple[Optional[bool], str]:
    server = WHOIS_SERVERS.get(tld)
    if not server:
        return None, "WHOIS-no-server"
    response = query_whois(domain, server)
    if response is None:
        return None, "WHOIS-error"
    response_lower = response.lower()
    if any(marker in response_lower for marker in WHOIS_FREE_MARKERS):
        return True, "WHOIS-free"
    # Heurystyka: jeśli widać "registrar" / "created" / "nserver" → zajęta
    if any(k in response_lower for k in ["registrar:", "created:", "nserver:", "name servers:"]):
        return False, "WHOIS-taken"
    return None, "WHOIS-?"


# ---------- DNS fallback ----------

def check_dns(domain: str) -> tuple[Optional[bool], str]:
    try:
        socket.gethostbyname(domain)
        return False, "DNS-A-record"
    except socket.gaierror:
        return None, "DNS-no-record"  # niepewne


# ---------- ORKIESTRACJA ----------

def check_domain(domain: str, tld: str, bootstrap: dict) -> tuple[Optional[bool], str]:
    rdap_url = get_rdap_url(tld, bootstrap)
    if rdap_url:
        result, method = check_rdap(domain, rdap_url)
        if result is not None:
            return result, method
    # Fallback do WHOIS
    if tld in WHOIS_SERVERS:
        result, method = check_whois(domain, tld)
        if result is not None:
            return result, method
    # Ostateczność: DNS (tylko mówi nam czy jest A; brak A != wolna)
    return check_dns(domain)


def main() -> int:
    print("Pobieram IANA RDAP bootstrap...", file=sys.stderr)
    bootstrap = load_rdap_bootstrap()

    all_tlds: list[tuple[str, str, int]] = []
    for group, tld_map in TLDS.items():
        for tld, price in tld_map.items():
            all_tlds.append((group, tld, price))

    total = len(CANDIDATES) * len(all_tlds)
    print(f"Sprawdzam {len(CANDIDATES)} kandydatow x {len(all_tlds)} TLD = {total} domen\n", file=sys.stderr)

    results: list[dict] = []
    i = 0
    for sld in CANDIDATES:
        for group, tld, price in all_tlds:
            i += 1
            domain = f"{sld}.{tld}"
            available, method = check_domain(domain, tld, bootstrap)
            status = "WOLNA" if available is True else ("zajeta" if available is False else "?    ")
            print(f"[{i:3}/{total}] {domain:<22} {status}  [{method}]", file=sys.stderr)
            results.append({
                "domain": domain,
                "sld": sld,
                "tld": tld,
                "group": group,
                "available": available,
                "method": method,
                "approx_price_pln": price,
            })
            time.sleep(0.25)

    # CSV
    out_path = Path(__file__).parent / "short_domains_results.csv"
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "domain", "sld", "tld", "group", "available", "method", "approx_price_pln",
        ])
        writer.writeheader()
        writer.writerows(results)

    # Podsumowanie
    free = [r for r in results if r["available"] is True]
    unknown = [r for r in results if r["available"] is None]
    free_sorted = sorted(free, key=lambda r: (r["approx_price_pln"], len(r["domain"])))

    print("\n" + "=" * 60)
    print(f"PODSUMOWANIE")
    print("=" * 60)
    print(f"Sprawdzonych:  {len(results)}")
    print(f"Wolnych:       {len(free)}")
    print(f"Niepewnych:    {len(unknown)}")
    print(f"Zajetych:      {len(results) - len(free) - len(unknown)}")
    print()
    print("WOLNE (sortowane po cenie):")
    for r in free_sorted:
        print(f"  {r['domain']:<22} ~{r['approx_price_pln']:>4} PLN/rok  [{r['group']}]")

    if unknown:
        print(f"\nNIEPEWNE (sprawdz recznie - prawdopodobnie zajete lub TLD bez RDAP):")
        for r in unknown[:20]:
            print(f"  {r['domain']:<22} [{r['method']}]")
        if len(unknown) > 20:
            print(f"  ... i {len(unknown) - 20} wiecej")

    print(f"\nCSV: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
