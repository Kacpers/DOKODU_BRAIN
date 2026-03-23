---
type: area
status: active
owner: kacper
last_reviewed: 2026-03-23
tags: [n8n, infrastruktura, docker, vault, devops, standardy, presidio, neo4j, mcp]
---

# AREA: n8n Infrastructure — Dokodu Stack
> **Odpowiedzialny:** Kacper Sieradzinski
> **Cel:** Utrzymanie, standaryzacja i skalowanie infrastruktury n8n dla Dokodu i klientow.

---

## ROZSZERZONY STOS AI (Zero-Trust AI Architecture)

> Dokudo Stack Q2 2026 — "Compliance by Design" dla klientów enterprise.

| Komponent | Narzędzie | Rola | Gdzie uruchomiony |
| :--- | :--- | :--- | :--- |
| **Orkiestrator** | n8n | Logika biznesowa, agnostycyzm językowy | Docker (VPS) |
| **PII Redaction** | Microsoft Presidio | Maskowanie danych osobowych PRZED wyjściem do chmury | Docker (lokalnie) |
| **Pamięć wektorowa** | Qdrant / Milvus | RAG embeddingi | Docker |
| **Pamięć grafowa** | Neo4j (GraphRAG) | Logika systemowa, relacje dokumentów | Docker |
| **Lokalne LLM (>24GB VRAM)** | Ollama / vLLM | Modele lokalne bez wysyłania PII | GPU server |
| **AI → DB/K8s** | MCP (Model Context Protocol) | Bezpieczne łączenie AI z K8s i bazami (Read-Only + Human-in-the-loop) | Lokalnie |
| **AI Terminal Agent** | Claude Code | Automatyzacja kodu z regułami w CLAUDE.md | WSL / CLI |

### Presidio — PII Redaction (kluczowa tarcza danych)
```
Architektura:
[n8n Code Node] → [Presidio Analyzer] → [Presidio Anonymizer] → [LLM API]
                        ↓
              Custom recognizers:
              - Regex dla NIP, REGON, PESEL
              - Deny-listy: nazwy klientów, strategie, IDs
              - Maskowanie strategii i danych finansowych
```

### Neo4j GraphRAG (rozwiązanie dla dużego kontekstu)
- Problem: zapychanie okna kontekstowego w `memory.md` przy długich projektach
- Rozwiązanie: dokumenty → Neo4j → zapytania grafowe zamiast vector search
- Use case Animex: dokumentacja SharePoint jako graf wiedzy firmy

### MCP dla K8s i DB (Human-in-the-loop)
- Tryb: **Read-Only** domyślnie — żaden agent nie pisze do produkcji bez zatwierdzenia
- Zastosowanie: inspekcja infrastruktury klienta bez ryzyka zmian

---

---

## SRODOWISKA n8n (Live Registry)

| Srodowisko | URL | Wersja | Owner | Cel | Backup |
| :--- | :--- | :---: | :--- | :--- | :---: |
| Dokodu (prod) | n8n.dokodu.it | 1.XX | Kacper | Wewnetrzne automatyzacje | TAK |
| Corleonis (prod) | n8n.[client].pl | 1.XX | Kacper | Obieg dokumentow | TAK |
| Animex (demo) | demo-n8n.dokodu.it | 1.XX | Kacper | Szkolenia | NIE (reset co tydzien) |
| Dev/Sandbox | localhost:5678 | latest | Kacper | Prototypowanie | NIE |

---

## STANDARDY TECHNICZNE (Dokodu Engineering Standards)

### Nazewnictwo Workflowow
```
[KLIENT]_[OBSZAR]_[FUNKCJA]_v[NR]
Przyklad: CORLEONIS_DOCS_InvoiceParser_v2
Przyklad: DOKODU_SALES_LeadNotification_v1
```

### Struktura Workflowu (obowiazkowa)
```
[Trigger] → [Error Handler - pocz.] → [...logika...] → [Success Log] → [Error Log]
                                                                           ↓
                                                                  [Alert: Slack/Email]
```

### Error Handling (obowiazek w KAZDYM workflowie produkcyjnym)
```javascript
// Error Workflow — podlaczony do kazdego flow prod
{
  "workflow_name": "{{$workflow.name}}",
  "error_message": "{{$execution.error.message}}",
  "node_name": "{{$execution.error.node.name}}",
  "timestamp": "{{$now.toISO()}}",
  "execution_id": "{{$execution.id}}"
}
// → Slack #n8n-errors + email do kacper@dokodu.it
```

### Logowanie (Logging Standard v1)
```javascript
// Na poczatku kazdego waznego node
console.log(JSON.stringify({
  level: "INFO",  // INFO | WARN | ERROR
  timestamp: new Date().toISOString(),
  workflow: $workflow.name,
  node: $node.name,
  message: "Opis dzialania",
  data_count: $input.all().length,  // ile rekordow przetworzone
  // NIE loguj PII! Tylko liczby i IDy.
}));
```

---

## KONFIGURACJA SERWERA (Dokodu Prod)

### Serwer bazowy
- **Provider:** [VPS Provider — np. Hetzner / OVH / Contabo]
- **Spec:** 4 vCPU, 8 GB RAM, 80 GB SSD
- **OS:** Ubuntu 22.04 LTS
- **Region:** EU (Frankfurt lub Amsterdam dla RODO)

### Docker Compose (minimalna konfiguracja prod)
```yaml
version: "3.8"
services:
  n8n:
    image: n8nio/n8n:latest
    restart: always
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=${N8N_USER}
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASS}
      - N8N_HOST=${N8N_HOST}
      - N8N_PORT=5678
      - N8N_PROTOCOL=https
      - WEBHOOK_URL=https://${N8N_HOST}/
      - GENERIC_TIMEZONE=Europe/Warsaw
      - N8N_LOG_LEVEL=warn
      - N8N_LOG_OUTPUT=console
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_USER=${DB_USER}
      - DB_POSTGRESDB_PASSWORD=${DB_PASS}
      - DB_POSTGRESDB_DATABASE=n8n
      - EXECUTIONS_DATA_SAVE_ON_ERROR=all
      - EXECUTIONS_DATA_SAVE_ON_SUCCESS=none  # nie zapisuj PII!
      - EXECUTIONS_DATA_MAX_AGE=30  # dni retencji
    volumes:
      - n8n_data:/home/node/.n8n

  postgres:
    image: postgres:15
    restart: always
    environment:
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASS}
      - POSTGRES_DB=n8n
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  n8n_data:
  postgres_data:
```

### Nginx Reverse Proxy (SSL)
```nginx
server {
    listen 443 ssl;
    server_name n8n.dokodu.it;

    ssl_certificate /etc/letsencrypt/live/n8n.dokodu.it/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/n8n.dokodu.it/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;

    location / {
        proxy_pass http://localhost:5678;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        chunked_transfer_encoding on;
        proxy_buffering off;
    }
}
```

---

## VAULT — ZARZADZANIE SEKRETAMI

### Hierarchia sekretow
```
vault/
├── dokodu/
│   ├── apis/
│   │   ├── openai_key
│   │   ├── google_ai_key
│   │   ├── anthropic_key
│   │   └── linkedin_ads_token
│   └── infrastructure/
│       ├── postgres_pass
│       └── n8n_encryption_key
└── clients/
    ├── corleonis/
    │   ├── comarch_api_key
    │   ├── smtp_password
    │   └── s3_access_key
    └── animex/
        └── demo_credentials
```

### Rotacja kluczy (obowiazek)
- API klucze zewnetrzne: co 90 dni
- Hasla systemowe: co 180 dni
- Trigger rotacji: n8n Scheduled Workflow → Vault API → alert na Slack

---

## PROCEDURY OPERACYJNE

### Wdrozenie nowego workflow na prod
1. Przetestuj w Dev/Sandbox (min. 10 udan wykonan)
2. Code review (sprawdz: error handling, logowanie, brak hardcoded secrets)
3. Export JSON → zapis w [[30_RESOURCES/RES_n8n_Blueprints/N8N_Blueprints]]
4. Import na prod → TEST z jednym realnym rekordem
5. Monitoruj przez 24h po wdrozeniu

### Backup workflow (co tydzien — piatek)
```bash
# Eksport wszystkich workflowow przez n8n CLI
n8n export:workflow --all --output=/backup/workflows-$(date +%Y%m%d).json
# Wgraj na zewnetrzny storage (S3 / Google Drive)
```

### Aktualizacja n8n (procedura)
1. Sprawdz changelog: github.com/n8n-io/n8n/releases
2. Test na srodowisku Dev najpierw (uruchom krytyczne workflows)
3. Backup Prod DB przed aktualizacja
4. Aktualizacja Prod w oknie: sobota 02:00-04:00 (minimalny ruch)
5. Monitoring przez 48h po aktualizacji

---

## MONITORING I ALERTOWANIE

### Co monitorujemy
- Dostepnosc n8n (health endpoint: /healthz) — ping co 5 min
- Bledy wykonan (error rate) — alert przy >5% w ciagu 1h
- Zuzycie CPU/RAM serwera — alert przy >80%
- Disk usage — alert przy >75%

### Narzedzia
- Monitoring dostepnosci: UptimeRobot (free tier) lub BetterStack
- Metryki serwera: netdata lub Grafana + Prometheus
- Logi n8n: CloudWatch / Papertrail / self-hosted Loki

---

## TROUBLESHOOTING (Najczestsze problemy)

| Problem | Przyczyna | Rozwiazanie |
| :--- | :--- | :--- |
| Workflow zawiesza sie | Memory leak w Code Node | Sprawdz petlę — uzyj pagination |
| Webhook nie dziala | Zly URL, brak SSL | Sprawdz WEBHOOK_URL env variable |
| OAuth2 token wygasl | Brak refresh | Sprawdz "Refresh token" w credentials |
| DB connection error | Postgres down | `docker compose restart postgres` |
| API rate limit | Za duzo requestow | Dodaj "Wait" node (200ms) miedzy requestami |
| PII w logach | Brak anonimizacji | Code Node z anonymize() przed logiem |
| Duplicate execution | Idempotency brak | Dodaj sprawdzenie klucza idempotentnosci |

---

## LINKI
- n8n Docs: https://docs.n8n.io
- n8n Community Forum: https://community.n8n.io
- n8n Releases: https://github.com/n8n-io/n8n/releases
- [[30_RESOURCES/RES_n8n_Blueprints/N8N_Blueprints]] — gotowe przeplywy do ponownego uzycia
