#!/usr/bin/env python3
"""
Tworzy drafty kampanii email n8n Launch 2026-05-06 w MailerLite.
Uruchom raz — tworzy 10 draftów gotowych do edycji przez Kacpra.
"""
import sys, json, urllib.request, urllib.parse, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import mailerlite_fetch as ml

API_BASE = "https://api.mailerlite.com/api/v2"
GROUPS = [113015717, 113077084]  # Transformacja (634) + Zapisy webinar automatyzacja (289)

def ml_request(method, path, payload):
    api_key = ml.get_api_key()
    req = urllib.request.Request(
        f"{API_BASE}/{path.lstrip('/')}",
        data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
        headers={
            'X-MailerLite-ApiKey': api_key,
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'curl/7.88.1'
        },
        method=method
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise Exception(f"HTTP {e.code}: {e.read().decode()[:300]}")

def ml_post(path, payload):
    return ml_request('POST', path, payload)

def ml_put(path, payload):
    return ml_request('PUT', path, payload)

UNSUB = '{$unsubscribe}'
URL_VAR = '{$url}'

def html_email(body_html):
    return (
        '<!DOCTYPE html><html>'
        '<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>'
        '<body style="margin:0;padding:0;background:#f4f4f4;font-family:Georgia,serif;">'
        '<table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:30px 0;">'
        '<tr><td align="center">'
        '<table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:4px;overflow:hidden;max-width:600px;width:100%;">'
        '<tr><td style="padding:40px 48px 32px;font-size:16px;line-height:1.7;color:#222222;">'
        + body_html +
        '<hr style="border:none;border-top:1px solid #eeeeee;margin:32px 0;">'
        '<p style="font-size:13px;color:#888888;margin:0;">'
        'Dokodu sp. z o.o. | kacper@dokodu.it<br>'
        'Chcesz wypisać się z listy? <a href="' + UNSUB + '" style="color:#888888;">Kliknij tutaj</a>'
        '</p>'
        '</td></tr></table></td></tr></table></body></html>'
    )

def p(text):
    return f'<p style="margin:0 0 20px;">{text}</p>'

def h(text):
    return f'<p style="margin:0 0 20px;font-size:18px;font-weight:bold;color:#111;">{text}</p>'

def btn(text, url):
    return f'''<p style="margin:28px 0;"><a href="{url}" style="background:#1a1a1a;color:#ffffff;padding:14px 28px;border-radius:4px;text-decoration:none;font-size:15px;font-weight:bold;display:inline-block;">{text}</a></p>'''

def bold(text):
    return f'<strong>{text}</strong>'

def link(text, url):
    return f'<a href="{url}" style="color:#1a1a1a;">{text}</a>'

# ══════════════════════════════════════════════
# EMAILE
# ══════════════════════════════════════════════

EMAILS = [

    {
        "name": "n8n #1 — To narzędzie zmienia sposób pracy polskich firm [31.03]",
        "subject_a": "To narzędzie właśnie wyprzedza Zapiera i Make razem wziętych",
        "subject_b": "Polskie firmy zaczęły używać czegoś, o czym większość nie słyszała",
        "body": html_email(
            p("Cześć,") +
            p("jakiś czas temu pobrałeś/aś materiały o automatyzacji albo byłeś/aś na jednym z moich webinarów. "
              "Cieszę się, że ten temat Cię interesuje — bo właśnie dzieje się coś ciekawego.") +
            p("W ostatnich miesiącach wdrażałem automatyzacje dla kilku polskich firm. "
              "Za każdym razem używałem jednego narzędzia: " + bold("n8n.")) +
            p("Nie Zapiera. Nie Make'a. n8n.") +
            p("Trzy powody, które zadecydowały:") +
            p(bold("1. Zero abonamentu za operacje.") + "<br>"
              "Zapier i Make liczą każde zadanie które wykonują. Przy 10 000 operacji miesięcznie — płacisz. "
              "n8n self-hosted działa na Twoim serwerze za ~20 zł/miesiąc. Tyle.") +
            p(bold("2. Pełna kontrola danych.") + "<br>"
              "Twoje dane nie wychodzą do zewnętrznych chmur. "
              "Ważne przy RODO i AI Act, który od sierpnia 2026 zaczyna mieć zęby.") +
            p(bold("3. AI wbudowane w workflow.") + "<br>"
              "GPT-4o, Gemini, Claude — wpinasz bezpośrednio w przepływ pracy. Bez API gymnastics.") +
            p("Wiem, że brzmi technicznie — ale naprawdę nie musisz być programistą, żeby to uruchomić. "
              "Nagrałem film który to pokazuje (ponad 119 000 osób już widziało):") +
            btn("▶ Obejrzyj: Jak zyskać kilka godzin tygodniowo dzięki automatyzacji",
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ") +  # TODO: podmień na właściwy URL
            p("Za tydzień pokażę Ci konkretny przykład z życia — jak jeden dział w polskiej firmie "
              "przestał tracić 200 godzin rocznie na ręcznym przetwarzaniu maili.") +
            p("Na razie jedno pytanie: " + bold("co u Ciebie jest najbardziej powtarzalnym, nudnym procesem w pracy?") +
              " Odpisz — czytam każdą odpowiedź.") +
            p("Kacper")
        )
    },

    {
        "name": "n8n #2 — Webinar: jak wdrożyć AI legalnie [07.04]",
        "subject_a": "Nagranie webinaru dla firm: AI + automatyzacja + RODO w jednym miejscu",
        "subject_b": "106 000 osób obejrzało ten webinar. Masz go za darmo.",
        "body": html_email(
            p("Cześć,") +
            p("w zeszłym tygodniu pisałem o n8n — narzędziu, które wyprzedza Zapiera i Make. "
              "Kilka osób odpisało z pytaniem: " + bold("\"ale czy to jest legalne i bezpieczne?\"")) +
            p("Dobre pytanie. I mam na nie gotową odpowiedź.") +
            p("Kilka miesięcy temu przeprowadziłem webinar specjalnie dla właścicieli firm i managerów: " +
              bold("\"Jak wdrożyć AI w firmie legalnie i bezpiecznie.\"") +
              " Obejrzało go ponad 106 000 osób.") +
            p("W ciągu 90 minut omawiamy:") +
            p("→ Co AI Act mówi o automatyzacji w Twojej firmie (i kiedy grożą kary)<br>"
              "→ Jak przechowywać dane klientów, żeby nie narazić się na RODO<br>"
              "→ Jak zbudować automatyzację, która nie wysyła danych do zewnętrznych chmur<br>"
              "→ Praktyczne demo n8n self-hosted — krok po kroku") +
            btn("▶ Obejrzyj nagranie webinaru (bezpłatnie)",
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ") +  # TODO: podmień URL
            p("Za trzy dni (piątek) wyślę Ci case study — jak konkretna polska firma "
              "zautomatyzowała swój dział obsługi klienta i co z tego wyszło.") +
            p("Kacper")
        )
    },

    {
        "name": "n8n #3 — Case study: BOK i 200h rocznie [10.04]",
        "subject_a": "200 godzin rocznie na przepisywanie maili. Skończyło się.",
        "subject_b": "Zrobiłem szkolenie dla 70 osób z jednej firmy. Oto co się stało.",
        "body": html_email(
            p("Cześć,") +
            p("dziś konkrety.") +
            p("Przez ostatnie tygodnie przeprowadzałem szkolenia dla dużego polskiego zakładu produkcyjnego. "
              "70 osób z działu obsługi klienta — pięć grup, każda po dwa dni.") +
            p("Ich problem był prosty i bolesny: dział obsługiwał ~200 zgłoszeń miesięcznie. "
              "Każde — ręcznie. Outlook, Excel, kopiuj-wklej do systemu. "
              "Menedżer tracił 15 godzin miesięcznie tylko na raporty.") +
            h("Co zrobiliśmy?") +
            p("Nauczyliśmy ich budować " + bold("agentów AI w n8n:") + "<br>"
              "→ Agent czyta maila i rozumie o co chodzi<br>"
              "→ Kategoryzuje zgłoszenie i nadaje priorytet<br>"
              "→ Sugeruje odpowiedź dopasowaną do historii klienta<br>"
              "→ Raport tygodniowy generuje się sam, bez niczyjego udziału") +
            h("Wyniki ankiet po szkoleniu:") +
            p(bold("4.8/5") + " — ogólna ocena szkolenia<br>"
              + bold("4.9/5") + " — ocena trenera<br>"
              "69 na 70 osób wypełniło ankietę dobrowolnie.") +
            p("Najczęstszy komentarz uczestników: "
              "<em>\"wychodzę z konkretnymi pomysłami na wdrożenia.\"</em>") +
            p("To nie jest magia. To workflow w n8n, który można zbudować w jeden dzień — "
              "bez umiejętności programistycznych.") +
            p("Za kilka dni powiem Ci o czymś, nad czym pracuję — kursie który uczy "
              "dokładnie tego samego, ale w Twoim tempie i z Twojego biurka.") +
            p("Kacper")
        )
    },

    {
        "name": "n8n #4 — Czy trzeba umieć programować? [14.04]",
        "subject_a": "Nie. Nie musisz umieć programować. (ale jest jeden haczyk)",
        "subject_b": "Pytasz: \"Czy dam radę?\" Odpowiadam szczerze.",
        "body": html_email(
            p("Cześć,") +
            p("od kilku tygodni piszę o automatyzacji i n8n. Dostałem sporo odpowiedzi. "
              "Najczęstsze pytanie brzmiało tak:") +
            p("<em>\"Brzmi świetnie, ale czy ja — bez technicznego backgroundu — dam radę?\"</em>") +
            p(bold("Krótka odpowiedź: tak.")) +
            p("Długa odpowiedź: n8n to narzędzie wizualne. Łączysz bloki jak klocki Lego. "
              "Każdy blok robi jedną rzecz — pobierz mail, wyślij do AI, zapisz w Excelu. "
              "Nie piszesz kodu. Budujesz logikę.") +
            p("Jedyna rzecz której potrzebujesz to umiejętność myślenia procesami: "
              "<em>\"Co się dzieje najpierw? Co potem? Co jeśli coś pójdzie nie tak?\"</em> "
              "To jest 80% automatyzacji.") +
            p("Nagrałem o tym film — 40 000 osób już go widziało:") +
            btn("▶ Jak automatyzować z AI bez kodowania",
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ") +  # TODO: podmień URL
            p("Wspominam o tym, bo za tydzień ogłaszam coś ważnego. "
              "Pracuję nad kursem który uczy n8n od zera — z perspektywy osoby która "
              "chce wdrożyć to w swojej firmie lub oferować klientom. Nie tutorial. Metodologia.") +
            p("Jeśli chcesz wiedzieć jako pierwszy — zapisz się na listę oczekujących:") +
            btn("→ Chcę być na liście oczekujących", "https://dokodu.it/kursy/n8n") +
            p("Kacper")
        )
    },

    {
        "name": "n8n #5 — Soft announcement [17.04]",
        "subject_a": "Powiem Ci coś, czego jeszcze nie ogłaszałem publicznie",
        "subject_b": "Pracuję nad czymś. Masz pierwszeństwo.",
        "body": html_email(
            p("Cześć,") +
            p("chcę Ci powiedzieć coś zanim ogłoszę to publicznie.") +
            p("Od kilku miesięcy uczę n8n — na warsztatach, szkoleniach firmowych, webinarach. "
              "Za każdym razem słyszę to samo: " +
              bold("\"Szkoda że nie ma kursu który przerabia to krok po kroku, z prawdziwymi projektami.\"")) +
            p("Postanowiłem go zrobić.") +
            h("n8n dla Agencji i Firm — od Zera do Automatyzacji Produkcyjnej") +
            p("7 tygodni. 7 gotowych systemów AI które budujesz razem ze mną:<br>"
              "→ System przechwytywania i kwalifikacji leadów<br>"
              "→ Automatyczny pipeline fakturowania<br>"
              "→ Asystent AI w Slacku który zna Twoje dane<br>"
              "→ Autonomiczny agent leadów<br>"
              "→ System RAG — AI który czyta Twoje dokumenty<br>"
              "→ i więcej") +
            p("Format: sesje live + nagrania. Jeden moduł co dwa tygodnie — uczysz się i wdrażasz.") +
            p(bold("Przedsprzedaż startuje 6 maja.") + " Cena pre-sale: " + bold("1 490 PLN netto.") +
              " Po otwarciu koszyka cena rośnie do 2 490 PLN po 72 godzinach.") +
            p("Limit: " + bold("50 miejsc") + " w pierwszej kohorcie.") +
            p("Jeśli chcesz mieć pewność że jesteś na liście — zapisz się teraz:") +
            btn("→ Zapisuję się na listę oczekujących", "https://dokodu.it/kursy/n8n") +
            p("Za tydzień ogłoszę to oficjalnie. Ty wiesz jako pierwszy.") +
            p("Kacper")
        )
    },

    {
        "name": "n8n #6 — Ogłoszenie przedsprzedaży [22.04]",
        "subject_a": "Ogłaszam. Przedsprzedaż kursu n8n startuje 6 maja.",
        "subject_b": "6 maja, 10:00. 50 miejsc. Cena pre-sale przez 72h.",
        "body": html_email(
            p("Cześć,") +
            p("czas powiedzieć wprost.") +
            h("6 maja 2026 o 10:00 otwieram przedsprzedaż kursu:") +
            p("<strong style='font-size:18px;'>n8n dla Agencji i Firm — od Zera do Automatyzacji Produkcyjnej</strong>") +
            p("7 tygodni, 7 systemów AI które budujesz i wdrażasz razem ze mną. "
              "Jeden moduł co dwa tygodnie — żadnego czekania na \"pełny kurs\", zaczynasz działać od razu.") +
            p(bold("Cena przedsprzedaży: 1 490 PLN netto") + "<br>"
              "Cena regularna (po 72h od otwarcia): 2 490 PLN netto<br>"
              "Limit: 50 miejsc w pierwszej kohorcie.") +
            p("Jeśli jesteś na liście oczekujących — dostajesz dostęp 24h wcześniej (5 maja) i "
              "masz gwarancję ceny pre-sale niezależnie od tego kiedy sfinalizujesz zakup.") +
            p("Jeśli jeszcze nie jesteś na liście — dołącz teraz:") +
            btn("→ Chcę być na liście oczekujących (dostęp 5 maja)", "https://dokodu.it/kursy/n8n") +
            p("Kacper") +
            p("<em style='font-size:14px;color:#555;'>P.S. Masz pytania przed zakupem? "
              "Za trzy dni wyślę FAQ — odpisz teraz jeśli chcesz żebym uwzględnił Twoje pytanie.</em>")
        )
    },

    {
        "name": "n8n #7 — FAQ przed zakupem [25.04]",
        "subject_a": "Najczęstsze pytania przed zapisem na kurs n8n — odpowiadam",
        "subject_b": "\"Czy dam radę?\", \"Ile czasu?\", \"Co jeśli nie spodoba mi się?\" — odpowiadam.",
        "body": html_email(
            p("Cześć,") +
            p("przed 6 maja zebrałem najczęstsze pytania które dostaję. Odpowiadam krótko i szczerze.") +
            h("Czy muszę umieć programować?") +
            p("Nie. n8n to narzędzie wizualne. Budujesz logikę, nie piszesz kodu. "
              "Na poprzednich szkoleniach uczyłem ludzi z działów BOK, logistyki, HR — żaden nie był programistą.") +
            h("Ile czasu tygodniowo?") +
            p("Zakładam 3-4 godziny na moduł. Jeden moduł co dwa tygodnie. "
              "Sesja live + nagranie + projekt do wdrożenia. Możesz wrócić do nagrań kiedy chcesz.") +
            h("Co jeśli nie zdążę z jakimś modułem?") +
            p("Nic się nie dzieje. Nagrania zostają z Tobą na zawsze. "
              "Uczysz się we własnym tempie — kurs nie znika po 7 tygodniach.") +
            h("Czy jest gwarancja zwrotu?") +
            p("Tak. 14 dni bez podawania przyczyny — zgodnie z ustawą konsumencką.") +
            h("Czym różni się ten kurs od tutoriali na YouTube?") +
            p("Tutorial pokazuje jak coś działa. Ten kurs uczy jak to sprzedać, wdrożyć i utrzymać "
              "dla klienta lub w swojej firmie. Dostajesz metodologię, nie tylko kliknięcia.") +
            p("Masz inne pytanie? Odpisz na tego maila — czytam przed 6 maja.") +
            btn("→ Zapisz się na listę oczekujących", "https://dokodu.it/kursy/n8n") +
            p("Kacper")
        )
    },

    {
        "name": "n8n #8 — 7 dni do końca ceny pre-sale [29.04]",
        "subject_a": "Zostało 7 dni. Potem cena rośnie o 1 000 PLN.",
        "subject_b": "6 maja cena 1 490 PLN. 9 maja — 2 490 PLN. Masz tydzień.",
        "body": html_email(
            p("Cześć,") +
            p("krótko.") +
            p(bold("6 maja o 10:00") + " otwieramy przedsprzedaż kursu n8n.") +
            p("Cena pre-sale: " + bold("1 490 PLN netto") + " — obowiązuje przez pierwsze 72 godziny.<br>"
              "Po tym czasie: 2 490 PLN netto.") +
            p("Jeśli jesteś na liście oczekujących — dostajesz dostęp do koszyka " +
              bold("5 maja o 10:00") + " (dzień wcześniej) i masz gwarancję ceny pre-sale.") +
            p("Jeśli jeszcze nie jesteś na liście:") +
            btn("→ Dołącz do listy oczekujących", "https://dokodu.it/kursy/n8n") +
            p("7 dni. Potem cena rośnie.") +
            p("Kacper")
        )
    },

    {
        "name": "n8n #9 — Jutro otwieramy [05.05]",
        "subject_a": "Jutro o 10:00. Ty masz dostęp godzinę wcześniej.",
        "subject_b": "Koszyk otwiera się jutro. Ostatnia szansa na 1 490 PLN.",
        "body": html_email(
            p("Cześć,") +
            p("jutro o 10:00 otwieramy koszyk kursu n8n.") +
            p("Jeśli jesteś na tej liście — oznacza to że zapisałeś/aś się na listę oczekujących. "
              "Dostajesz dostęp " + bold("dziś o 10:00") + " — godzinę przed resztą.") +
            p("Cena pre-sale " + bold("1 490 PLN netto") + " obowiązuje przez pierwsze 72h od otwarcia. "
              "Potem: 2 490 PLN.") +
            p("Limit: 50 miejsc. Bez wyjątków.") +
            btn("→ Wchodzę w cenie pre-sale", "https://dokodu.it/kursy/n8n") +
            p("Jeśli masz jeszcze jakieś pytanie — odpisz teraz. Czytam.") +
            p("Kacper") +
            p("<em style='font-size:14px;color:#555;'>P.S. Pierwszy moduł dostępny od razu po zakupie. "
              "Zaczynasz już jutro.</em>")
        )
    },

    {
        "name": "n8n #10 — LAUNCH: Koszyk otwarty [06.05]",
        "subject_a": "🟢 Koszyk otwarty. 50 miejsc. Zaczynamy.",
        "subject_b": "Startujemy. Moduł 1 czeka na Ciebie od teraz.",
        "body": html_email(
            p("Cześć,") +
            p("koszyk otwarty.") +
            h("n8n dla Agencji i Firm — Moduł 1 dostępny od dziś.") +
            p("Kupujesz teraz → Moduł 1 dostępny natychmiast → kolejne moduły co 2 tygodnie.<br>"
              "Nie czekasz. Zaczynasz.") +
            p(bold("Cena pre-sale: 1 490 PLN netto") + "<br>"
              "Obowiązuje do 9 maja (72h od otwarcia).<br>"
              "Limit: 50 miejsc.") +
            btn("→ Kupuję w cenie pre-sale", "https://dokodu.it/kursy/n8n") +
            p("Kacper") +
            p("<em style='font-size:14px;color:#555;'>Pytania? Odpisz na tego maila lub napisz na kacper@dokodu.it</em>")
        )
    },

]

def main():
    created = []
    for i, email in enumerate(EMAILS, 1):
        print(f"Tworzę email {i}/10: {email['name'][:50]}...")
        try:
            result = ml_post("campaigns", {
                "subject": email["subject_a"],
                "from": "kacper@dokodu.it",
                "from_name": "Kacper",
                "groups": GROUPS,
                "type": "regular"
            })
            campaign_id = result["id"]

            # Dodaj content
            ml_put(f"campaigns/{campaign_id}/content", {
                "html": email["body"],
                "plain": "Wersja tekstowa emaila. Otwórz w przeglądarce: " + URL_VAR + "\n\nWypisz się z listy: " + UNSUB
            })

            created.append({"id": campaign_id, "name": email["name"]})
            print(f"  ✅ ID: {campaign_id}")
            time.sleep(0.5)

        except Exception as e:
            print(f"  ❌ Błąd: {e}")

    print(f"\nGotowe! Utworzono {len(created)}/10 draftów w MailerLite.")
    print("Pamiętaj żeby podmienić URL-e filmów YT (zaznaczone jako TODO) przed wysyłką.")
    for c in created:
        print(f"  - {c['name']} (ID: {c['id']})")

if __name__ == "__main__":
    main()
