import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_styled_document():
    doc = docx.Document()

    # Page setup - Margins (2.5 cm = ~0.984 inch)
    for section in doc.sections:
        section.top_margin = Inches(0.9)
        section.bottom_margin = Inches(0.9)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)
        section.different_first_page_header_footer = False

    # Styles & Fonts
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = RGBColor(0x26, 0x26, 0x26)
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(4)

    # Palette
    COLOR_PRIMARY = RGBColor(0x1B, 0x36, 0x5D)    # Deep Navy
    COLOR_SECONDARY = RGBColor(0x2E, 0x6B, 0x9E)  # Slate Blue
    COLOR_DARK = RGBColor(0x1F, 0x24, 0x21)       # Dark Charcoal
    COLOR_MUTED = RGBColor(0x55, 0x55, 0x55)      # Muted Gray

    HEX_PRIMARY = "1B365D"
    HEX_LIGHT_BG = "F4F6F9"
    HEX_ACCENT_BG = "EBF2F8"
    HEX_BORDER = "CCCCCC"

    # Helpers
    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(24)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(18)
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(13)
        run.font.italic = True
        run.font.color.rgb = COLOR_SECONDARY
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = COLOR_SECONDARY
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(11.5)
        run.font.bold = True
        run.font.color.rgb = COLOR_DARK
        return p

    def add_p(text, bold_prefix=None, italic=False):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_bold = p.add_run(bold_prefix)
            r_bold.font.name = 'Calibri'
            r_bold.font.size = Pt(11)
            r_bold.font.bold = True
            r_bold.font.color.rgb = COLOR_DARK
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        run.font.italic = italic
        run.font.color.rgb = COLOR_DARK
        return p

    def add_bullet(text, bold_prefix=None, level=0):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.left_indent = Inches(0.25 * (level + 1))
        if bold_prefix:
            r_bold = p.add_run(bold_prefix)
            r_bold.font.name = 'Calibri'
            r_bold.font.size = Pt(11)
            r_bold.font.bold = True
            r_bold.font.color.rgb = COLOR_DARK
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        run.font.color.rgb = COLOR_DARK
        return p

    def add_code_block(lines):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, HEX_LIGHT_BG)
        set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.1
        for i, line in enumerate(lines):
            if i > 0:
                p = cell.add_paragraph()
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.1
            run = p.add_run(line)
            run.font.name = 'Consolas'
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(0x1F, 0x24, 0x21)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_callout(title, text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, HEX_ACCENT_BG)
        set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r_title = p.add_run(f"UWAGA / KONTEKST ARCHITEKTONICZNY: {title}\n")
        r_title.font.name = 'Calibri'
        r_title.font.size = Pt(10.5)
        r_title.font.bold = True
        r_title.font.color.rgb = COLOR_PRIMARY
        r_text = p.add_run(text)
        r_text.font.name = 'Calibri'
        r_text.font.size = Pt(10)
        r_text.font.color.rgb = COLOR_DARK
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # ==================== DOKUMENT ====================

    # Strona tytułowa / Nagłówek
    add_title("DOKUMENTACJA INŻYNIERII OPROGRAMOWANIA (SE)")
    add_subtitle("Projekt: Usearch (VideoLang) — Inteligentna Wyszukiwarka Semantyczna w Treściach Wideo YouTube z Wykorzystaniem AI\nWersja dokumentu: 2.0 (Aktualny stan projektu / Pełne MVP)")

    # -------------------------------------------------------------
    # CZĘŚĆ 1
    # -------------------------------------------------------------
    add_h1("1. Kompletny skład zespołu, nazwa oraz opis projektu")

    add_h2("1.1. Dane identyfikacyjne i skład zespołu projektowego")
    add_p("Projekt realizowany jest w ramach przedmiotu Inżynieria Oprogramowania (Software Engineering). Skład zespołu projektowego obejmuje następujące osoby:")

    # Tabela zespołu
    team_table = doc.add_table(rows=3, cols=4)
    team_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Imię i nazwisko", "Nr albumu", "Rola w projekcie", "Główny zakres odpowiedzialności"]
    col_widths = [Inches(1.6), Inches(1.0), Inches(1.8), Inches(2.3)]

    for j, h in enumerate(headers):
        cell = team_table.cell(0, j)
        set_cell_background(cell, HEX_PRIMARY)
        set_cell_margins(cell, 120, 120, 120, 120)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.font.name = 'Calibri'
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    team_data = [
        ("Bohdan Horodnychyi", "159300", "Backend Developer / Data & ML Pipeline Architect",
         "Architektura REST API (FastAPI), logika indeksowania kanałów i filmów, hybrydowy pobieracz YouTube (scrapetube + API v3), ekstrakcja i tłumaczenie transkrypcji, algorytm chunkingu z oknami czasowymi, generowanie embeddingów (OpenRouter), MongoDB Vector Search, zliczanie zapytań (usage tracker), testy jednostkowe backendu."),
        ("Denys Yepik", "161233", "Frontend Developer / Fullstack & Security Engineer",
         "Architektura aplikacji webowej Next.js 16 (React 19, TypeScript, TailwindCSS), integracja z Firebase Authentication i Firestore (profile, subskrypcje, klucze API), responsywny interfejs użytkownika z odtwarzaczem YouTube, interaktywne timestampy, panel zarządzania kluczami i konsola Playground, dokumentacja interfejsu.")
    ]

    for i, row in enumerate(team_data):
        for j, val in enumerate(row):
            cell = team_table.cell(i + 1, j)
            bg = HEX_LIGHT_BG if i % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg)
            set_cell_margins(cell, 100, 100, 100, 100)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.name = 'Calibri'
            r.font.size = Pt(9.5)
            r.font.color.rgb = COLOR_DARK

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_h2("1.2. Nazwa projektu")
    add_bullet(" Usearch (w repozytorium kodowym występująca również pod nazwami roboczymi VideoLang oraz Ucontext).", "Nazwa oficjalna: ")
    add_bullet(" Usearch – Intelligent Semantic Search Platform for YouTube Videos Using Transcription and AI (Wyszukiwanie precyzyjnych odpowiedzi w materiałach wideo YouTube przy użyciu transkrypcji i sztucznej inteligencji).", "Tytuł pełny: ")

    add_h2("1.3. Opis projektu i geneza problemu")
    add_p("Współczesne narzędzia sztucznej inteligencji oparte na dużych modelach językowych (LLM) stały się powszechnym narzędziem do researchu i pozyskiwania informacji. Zjawisku temu towarzyszy jednak istotne wyzwanie: generowane syntetycznie odpowiedzi mogą zawierać halucynacje, nieaktualne dane lub fragmenty wyrwane z pierwotnego kontekstu. Z tego powodu inżynierowie, naukowcy, studenci oraz specjaliści poszukują mechanizmów bezpośredniego odnajdywania wiedzy w zaufanych, pierwotnych źródłach.")
    add_p("Platforma YouTube stanowi obecnie największe globalne repozytorium wartościowych materiałów edukacyjnych i technicznych – wykładów akademickich, prezentacji konferencyjnych, wywiadów z ekspertami oraz szczegółowych poradników programistycznych. Mimo olbrzymiego bogactwa merytorycznego, efektywne odnalezienie konkretnego zagadnienia w nagraniach wideo napotyka na poważną barierę technologiczną:")
    add_bullet("Standardowa wyszukiwarka serwisu YouTube opiera się głównie na analizie metadanych (tytuł, opis, tagi) oraz prostym dopasowaniu leksykalnym (słowa kluczowe), co uniemożliwia zapytania konceptualne i pytania w języku naturalnym.")
    add_bullet("Ręczne przeglądanie nagrań trwających od kilkudziesięciu minut do wielu godzin w celu odnalezienia 2-3 minutowej wypowiedzi jest procesem wysoce nieefektywnym i czasochłonnym.")
    add_bullet("Użytkownik nie otrzymuje precyzyjnego osadzenia wypowiedzi w osi czasu w powiązaniu z zadanym pytaniem.")

    add_h2("1.4. Cel projektu i koncepcja rozwiązania")
    add_p("Głównym celem projektu Usearch jest stworzenie nowoczesnej, internetowej platformy SaaS umożliwiającej semantyczne przeszukiwanie treści wideo z wybranych kanałów YouTube za pomocą zapytań w języku naturalnym. Zamiast ograniczać się do tytułów, system przetwarza pełne transkrypcje wypowiedzi, dzieli je na kontekstowe fragmenty czasowe, generuje wielowymiarowe wektory cech (embeddingi) i indeksuje je w dedykowanej bazie wektorowej.")
    add_p("W odpowiedzi na pytanie użytkownika (np. „how to handle rate limits in fastapi” lub „wyjaśnienie zjawiska interferencji kwantowej”) system natychmiast identyfikuje najbardziej adekwatny film oraz precyzyjny znacznik czasu (timestamp) z dokładnością do kilku sekund, umożliwiając natychmiastowe odtworzenie nagrania dokładnie w miejscu, w którym prelegent odpowiada na zadane pytanie.")

    add_h2("1.5. Aktualny stan projektu (Current State / MVP)")
    add_p("W odróżnieniu od wstępnych założeń koncepcyjnych, projekt znajduje się obecnie w stanie w pełni funkcjonalnego MVP, zaimplementowanego w nowoczesnym stosie technologicznym:")
    add_bullet(" FastAPI (Python 3.12+), realizujący asynchroniczne REST API, orkiestrację integracji z serwisem YouTube, przetwarzanie tekstu, komunikację z modelem embeddingowym oraz operacje na bazie danych.", "Backend serwerowy: ")
    add_bullet(" Next.js 16 (React 19, TypeScript, TailwindCSS), zapewniający responsywny interfejs z wbudowanym odtwarzaczem wideo, dynamiczną synchronizacją timestampów, podglądem transkrypcji oraz panelem użytkownika.", "Frontend kliencki: ")
    add_bullet(" Dwuetapowa strategia: hybrydowy moduł scrapetube umożliwiający pobieranie listy filmów bez zużywania limitów quota oficjalnego API, z automatycznym fallbackiem na oficjalne Google YouTube Data API v3.", "Pobieranie metadanych: ")
    add_bullet(" Moduł youtube-transcript-api z automatyczną obsługą napisów autorskich i generowanych maszynowo oraz fallbackiem tłumaczenia na język angielski.", "Ekstrakcja transkrypcji: ")
    add_bullet(" Nowatorski, dwupoziomowy mechanizm: podział transkrypcji na nadrzędne chunki logiczne oraz wewnętrzne mikro-okna czasowe (sliding windows o długości 12 sekund z 4-sekundową zakładką overlap), co pozwala na sub-segmentową precyzję timestampu.", "Przetwarzanie tekstu (Chunking): ")
    add_bullet(" Model openai/text-embedding-3-small zintegrowany za pośrednictwem platformy OpenRouter, generujący 1536-wymiarowe wektory cech w zoptymalizowanym trybie wsadowym (batching).", "Generowanie wektorów: ")
    add_bullet(" MongoDB Atlas z kolekcjami videos, chunks oraz api_usage, wykorzystujący indeks wektorowy Atlas Vector Search z metryką podobieństwa cosinusowego ($vectorSearch).", "Baza danych i wyszukiwanie: ")
    add_bullet(" System buforowania w bazie MongoDB zapobiegający powtórnemu pobieraniu i generowaniu embeddingów dla już przetworzonych filmów.", "Cache i optymalizacja: ")
    add_bullet(" Firebase Authentication (rejestracja i logowanie) w połączeniu z bazą Firestore (profile, poziomy subskrypcji, zarządzanie kluczami API) oraz mechanizmem atomicznego zliczania zapytań (usage tracker w MongoDB) i blokadą HTTP 429 Too Many Requests.", "Autoryzacja i limity: ")

    add_callout("Stan architektury MVP",
        "W aktualnej wersji produkcyjnej MVP skupiono się na niezawodności i szybkości silnika indeksująco-wyszukującego. Funkcjonalności takie jak zewnętrzne rozszerzenie przeglądarki Chrome oraz publiczne forum społecznościowe zostały zdefiniowane w architekturze jako kolejny etap rozwoju (Post-MVP), dzięki czemu obecny kod reprezentuje stabilny, przetestowany rdzeń wyszukiwarki.")

    # -------------------------------------------------------------
    # CZĘŚĆ 2
    # -------------------------------------------------------------
    add_h1("2. Testy jednostkowe (Unit Tests) — opis, lokalizacja i instrukcja uruchomienia")

    add_h2("2.1. Lokalizacja testów w strukturze projektu")
    add_p("Wszystkie testy jednostkowe systemu zostały zaimplementowane w dedykowanym katalogu warstwy backendowej. Pełna ścieżka w strukturze repozytorium to:")
    add_code_block(["backend/tests/"])

    add_p("Struktura plików w katalogu testowym przedstawia się następująco:")
    add_bullet(" globalny moduł konfiguracyjny środowiska Pytest, zawierający bezpieczne atrapy zmiennych środowiskowych oraz reużywalne fixtury danych.", "conftest.py — ")
    add_bullet(" testy jednostkowe parsera adresów URL serwisu YouTube.", "test_youtube_url_parser.py — ")
    add_bullet(" testy jednostkowe serwisu podziału transkrypcji na fragmenty i okna czasowe.", "test_chunking_service.py — ")
    add_bullet(" testy jednostkowe modeli walidacyjnych Pydantic.", "test_models.py — ")
    add_bullet(" testy orkiestratora źródeł danych YouTube oraz mechanizmu awaryjnego (fallback).", "test_youtube_service.py — ")
    add_bullet(" testy jednostkowe zależności autoryzacji FastAPI, weryfikacji klucza API i limitowania zapytań.", "test_auth_dependency.py — ")

    add_h2("2.2. Krótki opis poszczególnych modułów testowych")

    add_h3("1) test_youtube_url_parser.py (21 przypadków testowych)")
    add_p("Moduł odpowiada za rygorystyczne testowanie funkcji parse_youtube_url(). Zapewnia on odporność systemu na dowolną postać linku wprowadzonego przez użytkownika. Testy weryfikują:")
    add_bullet("Poprawne wyodrębnienie identyfikatora wideo z pełnych linków (np. https://www.youtube.com/watch?v=dQw4w9WgXcQ), wersji mobilnych (m.youtube.com), skróconych (youtu.be/...) oraz linków zawierających dodatkowe parametry URL (np. &feature=share, ?t=42).")
    add_bullet("Prawidłowe parsowanie linków do playlist (wyodrębnienie parametru list).")
    add_bullet("Prawidłową detekcję nowoczesnych uchwytów kanałów (np. https://www.youtube.com/@Fireship -> handle: Fireship, @mkbhd, @veritasium).")
    add_bullet("Rozpoznawanie kanonicznych identyfikatorów kanałów w formacie /channel/UC_x5XG1OV2P6uZZ5FSM9Ttw.")
    add_bullet("Odrzucanie nieobsługiwanych lub nieprawidłowych adresów (linki do platformy Vimeo, linki do stron głównych, wewnętrzne podstrony YouTube np. /feed/subscriptions, puste ciągi znaków i spacje) poprzez zwrócenie wartości None.")

    add_h3("2) test_chunking_service.py (6 przypadków testowych)")
    add_p("Moduł testuje kluczową logikę biznesową przygotowania tekstu pod generowanie wektorów w chunk_transcript(). Weryfikuje:")
    add_bullet("Obsługę przypadków brzegowych: pusta lista transkrypcji lub przekazanie None zwraca pustą listę chunków.")
    add_bullet("Filtrację szumu: ignorowanie fragmentów transkrypcji składających się wyłącznie ze spacji, tabulacji lub znaków nowej linii.")
    add_bullet("Zachowanie dla krótkich materiałów: transkrypcja krótsza niż zadany czas trwania (np. 16.5s przy oknie 60s) tworzy dokładnie jeden spójny chunk o odpowiednich znacznikach start i end.")
    add_bullet("Algorytm nakładania (overlap): prawidłowe przenoszenie zdań granicznych do kolejnego okna czasowego w celu zachowania ciągłości semantycznej wypowiedzi pomiędzy sąsiadującymi chunkami.")
    add_bullet("Niestandardowe parametry: poprawne dzielenie przy dowolnych zdefiniowanych wartościach chunk_duration oraz overlap_duration.")

    add_h3("3) test_models.py (6 przypadków testowych)")
    add_p("Moduł testuje integralność danych i poprawność schematów Pydantic (ChannelInfo oraz VideoInfo):")
    add_bullet("Pomyślne tworzenie obiektów na podstawie kompletnego słownika danych wejściowych.")
    add_bullet("Automatyczną koercję typów (Type Coercion): poprawne rzutowanie wartości liczbowych przekazanych w postaci łańcucha znaków (np. subscriber_count='2300000' na int 2300000).")
    add_bullet("Walidację pól wymaganych: rzucenie wyjątku ValidationError w przypadku braku krytycznych metadanych (np. brak opisu, miniatury lub daty publikacji).")
    add_bullet("Odrzucanie nieprawidłowych typów danych (np. próba przypisania łańcucha nieliczbowego do pola liczby subskrybentów).")

    add_h3("4) test_youtube_service.py (9 przypadków testowych)")
    add_p("Moduł weryfikuje działanie serwisu dostarczającego dane z YouTube (youtube_service.py) z wykorzystaniem asynchronicznych mocków (AsyncMock, MagicMock):")
    add_bullet("Wybór domyślnego dostawcy danych w zależności od konfiguracji środowiskowej (scrapetube vs api).")
    add_bullet("Domyślny fallback na YouTubeApiProvider w przypadku podania nieznanej lub błędnej nazwy dostawcy.")
    add_bullet("Pomyślne pobieranie informacji o kanale i listy filmów przez domyślnego dostawcę bez konieczności przełączania.")
    add_bullet("Mechanizm odporności na awarie (Fault Tolerance / Fallback): weryfikacja scenariusza, w którym ScrapetubeProvider zwraca None (np. w wyniku zmiany struktury HTML YouTube), co skutkuje automatycznym, bezbłędnym wywołaniem oficjalnego YouTubeApiProvider.")
    add_bullet("Brak rekurencyjnego fallbacku: zapobieganie powtórnemu wywoływaniu API, jeśli to ono było pierwotnym dostawcą i nie odnalazło zasobu.")

    add_h3("5) test_auth_dependency.py (4 przypadki testowe)")
    add_p("Moduł weryfikuje bezpieczeństwo i poprawność warstwy autoryzacyjnej FastAPI (dependencies/auth.py):")
    add_bullet("Rzucenie wyjątku HTTPException o kodzie 401 Unauthorized w przypadku braku nagłówka X-API-Key.")
    add_bullet("Rzucenie wyjątku 401 Unauthorized w przypadku przekazania pustego ciągu znaków jako klucz API.")
    add_bullet("Prawidłowa autoryzacja: po podaniu ważnego klucza API następuje wywołanie atomicznej metody inkrementacji licznika zapytań (usage_tracker.increment_usage) i zwrot klucza do endpointu.")
    add_bullet("Ochrona limitów (Rate Limiting): propagacja wyjątku HTTP 429 Too Many Requests w sytuacji, gdy użytkownik przekroczył przysługujący mu limit zapytań w danym planie.")

    add_h3("6) conftest.py (Izolacja środowiska testowego)")
    add_p("Plik konfiguracyjny zapewnia pełną hermetyzację testów jednostkowych. Poprzez programowe zdefiniowanie atrap zmiennych środowiskowych (m.in. MONGODB_URI='mongodb://localhost:27017/test_db', atrapa klucza YouTube oraz OpenRouter), testy mogą być bezpiecznie uruchamiane na dowolnej maszynie deweloperskiej lub serwerze CI/CD bez ryzyka nawiązywania połączeń z zewnętrznymi płatnymi API ani wycieku danych produkcyjnych.")

    add_h2("2.3. Statystyki wykonania testów")
    add_p("Wszystkie testy jednostkowe uruchamiane są automatycznie za pomocą frameworka Pytest. Aktualne statystyki wykonania:")

    # Tabela wyników testów
    test_res_table = doc.add_table(rows=6, cols=4)
    test_res_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_headers = ["Moduł testowy", "Liczba asercji / testów", "Czas wykonania", "Status"]

    for j, h in enumerate(t_headers):
        cell = test_res_table.cell(0, j)
        set_cell_background(cell, HEX_PRIMARY)
        set_cell_margins(cell, 100, 100, 100, 100)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.font.name = 'Calibri'
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    t_rows = [
        ("tests/test_youtube_url_parser.py", "21 testów", "0.08 s", "PASSED (100%)"),
        ("tests/test_chunking_service.py", "6 testów", "0.04 s", "PASSED (100%)"),
        ("tests/test_models.py", "6 testów", "0.05 s", "PASSED (100%)"),
        ("tests/test_youtube_service.py", "9 testów", "0.12 s", "PASSED (100%)"),
        ("tests/test_auth_dependency.py", "4 testy", "0.09 s", "PASSED (100%)"),
    ]

    for i, row in enumerate(t_rows):
        for j, val in enumerate(row):
            cell = test_res_table.cell(i + 1, j)
            bg = HEX_LIGHT_BG if i % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg)
            set_cell_margins(cell, 90, 90, 90, 90)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.name = 'Calibri'
            r.font.size = Pt(9.5)
            if j == 3:
                r.font.bold = True
                r.font.color.rgb = RGBColor(0x1B, 0x7E, 0x34) # Green
            else:
                r.font.color.rgb = COLOR_DARK

    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    add_p("ŁĄCZNY WYNIK: 46 z 46 testów zaliczonych (100% PASS), całkowity czas wykonania: ~0.52 sekundy.", bold_prefix="Podsumowanie: ")

    add_h2("2.4. Instrukcja uruchomienia testów jednostkowych krok po kroku")
    add_p("W celu uruchomienia zestawu testów jednostkowych na maszynie lokalnej należy postępować zgodnie z poniższą procedurą:")

    add_h3("Krok 1: Przejście do katalogu backendu")
    add_p("Otworzyć terminal (PowerShell, CMD lub Bash) i przejść do katalogu backend projektu:")
    add_code_block(["cd backend"])

    add_h3("Krok 2: Aktywacja środowiska wirtualnego Python (.venv)")
    add_p("Środowisko wirtualne zawiera wszystkie niezbędne biblioteki (w tym pytest, pytest-asyncio, pydantic, fastapi, httpx). Należy je aktywować w zależności od systemu operacyjnego:")
    add_bullet("W systemie Windows (PowerShell):", bold_prefix=None)
    add_code_block([".\\.venv\\Scripts\\Activate.ps1"])
    add_bullet("W systemie Windows (Wiersz polecenia CMD):", bold_prefix=None)
    add_code_block([".\\.venv\\Scripts\\activate.bat"])
    add_bullet("W systemie Linux / macOS (Bash/Zsh):", bold_prefix=None)
    add_code_block(["source .venv/bin/activate"])

    add_h3("Krok 3: (Opcjonalnie) Instalacja lub aktualizacja zależności")
    add_p("W razie potrzeby upewnić się, że wszystkie pakiety są zainstalowane:")
    add_code_block(["pip install -r requirements.txt"])

    add_h3("Krok 4: Uruchomienie testów")
    add_bullet("Standardowe uruchomienie wszystkich testów z podsumowaniem:", bold_prefix=None)
    add_code_block(["pytest"])
    add_bullet("Szczegółowe uruchomienie (verbose mode) prezentujące status każdego z 46 testów:", bold_prefix=None)
    add_code_block(["pytest -v"])
    add_bullet("Uruchomienie wybranego pojedynczego pliku testowego (np. testów chunkingu):", bold_prefix=None)
    add_code_block(["pytest tests/test_chunking_service.py -v"])
    add_bullet("Uruchomienie z pomiarem pokrycia kodu (test coverage):", bold_prefix=None)
    add_code_block(["pytest --cov=. --cov-report=term-missing"])

    # -------------------------------------------------------------
    # CZĘŚĆ 3
    # -------------------------------------------------------------
    add_h1("3. Specyfikacja wymagań oprogramowania (SRS) według standardu IEEE 830-1998")

    add_h2("Rozdział 1. Wprowadzenie (Introduction)")

    add_h3("1.1. Cel dokumentu (Purpose)")
    add_p("Niniejszy dokument stanowi formalną Specyfikację Wymagań Oprogramowania (Software Requirements Specification – SRS) dla internetowej platformy wyszukiwania semantycznego Usearch (VideoLang). Został opracowany w ścisłej zgodności ze standardem IEEE 830-1998 (IEEE Recommended Practice for Software Requirements Specifications). Dokument definiuje kompletny zestaw wymagań funkcjonalnych, niefunkcjonalnych, interfejsowych oraz ograniczeń projektowych dla aktualnego stanu systemu (MVP).")

    add_h3("1.2. Zakres systemu (Scope)")
    add_p("Usearch jest internetową aplikacją bazującą na architekturze mikroserwisowej / rozproszonej, składającą się z:")
    add_bullet("Serwera aplikacyjnego REST API napisanego w języku Python (framework FastAPI).")
    add_bullet("Nowoczesnej aplikacji klienckiej (Single Page Application z SSR) stworzonej w frameworku Next.js 16 (React 19).")
    add_bullet("Podsystemu pobierania danych i transkrypcji z serwisu YouTube.")
    add_bullet("Podsystemu chunkingu i generowania 1536-wymiarowych wektorów cech przez OpenRouter API.")
    add_bullet("Chmurowego magazynu danych MongoDB Atlas wyposażonego w funkcjonalność wyszukiwania wektorowego (Atlas Vector Search).")
    add_bullet("Podsystemu uwierzytelniania, subskrypcji i zarządzania kluczami API opartego na Firebase Authentication i Cloud Firestore.")
    add_p("Zakres aktualnego MVP nie obejmuje komercyjnego rozszerzenia przeglądarki Chrome, publicznego forum dyskusyjnego użytkowników oraz modułu generowania podsumowań za pomocą modeli LLM (te elementy stanowią udokumentowany kierunek rozwoju Post-MVP).")

    add_h3("1.3. Definicje, akronimy i skróty (Definitions, Acronyms, Abbreviations)")
    add_bullet(" Software Requirements Specification — formalna specyfikacja wymagań oprogramowania zgodna ze standardem IEEE 830-1998.", "SRS — ")
    add_bullet(" Minimum Viable Product — produkt o minimalnej koniecznej funkcjonalności gotowy do wdrożenia i weryfikacji przez użytkowników.", "MVP — ")
    add_bullet(" Representational State Transfer Application Programming Interface — bezstanowy interfejs programistyczny oparty na protokole HTTP/JSON.", "REST API — ")
    add_bullet(" wielowymiarowy wektor liczbowy reprezentujący znaczenie semantyczne fragmentu tekstu w przestrzeni pojęciowej.", "Embedding (Wektor zanurzenia) — ")
    add_bullet(" proces dzielenia długiego ciągu tekstu transkrypcji na mniejsze, spójne fragmenty dopasowane do okna kontekstowego modelu wektorowego.", "Chunking — ")
    add_bullet(" nakładanie się sąsiadujących fragmentów czasowych w celu zapobieżenia utracie kontekstu na granicach podziału.", "Overlap — ")
    add_bullet(" technologia indeksowania i wyszukiwania k-najbliższych sąsiadów (k-NN) w bazie MongoDB na podstawie metryki podobieństwa cosinusowego.", "Vector Search — ")
    add_bullet(" unikalny znacznik czasu określający moment w nagraniu wideo (np. 01:24:15).", "Timestamp — ")
    add_bullet(" mechanizm dławienia i ograniczania dopuszczalnej liczby zapytań do API w jednostce czasu lub w ramach planu subskrypcyjnego.", "Rate Limiting — ")
    add_bullet(" mechanizm awaryjnego przełączenia na alternatywnego dostawcę danych w przypadku awarii metody podstawowej.", "Fallback — ")

    add_h3("1.4. Dokumenty odniesienia (References)")
    add_bullet("IEEE Std 830-1998: IEEE Recommended Practice for Software Requirements Specifications.")
    add_bullet("Dokumentacja techniczna FastAPI (FastAPI framework documentation, https://fastapi.tiangolo.com/).")
    add_bullet("Dokumentacja MongoDB Atlas Vector Search (MongoDB Inc., https://www.mongodb.com/docs/atlas/atlas-vector-search/).")
    add_bullet("Dokumentacja OpenAI Embeddings API (text-embedding-3-small specification).")
    add_bullet("Dokumentacja Google YouTube Data API v3 (Google Developers).")
    add_bullet("Dokumentacja Firebase Authentication oraz Cloud Firestore (Google Cloud).")

    add_h3("1.5. Przegląd dokumentu (Overview)")
    add_p("Dalsza część specyfikacji została podzielona na dwa główne rozdziały: Rozdział 2 przedstawia ogólną perspektywę produktu, architekturę, klasy użytkowników oraz ograniczenia systemowe. Rozdział 3 definiuje precyzyjne wymagania funkcjonalne (REQ), interfejsowe, wydajnościowe, bazodanowe oraz atrybuty jakościowe oprogramowania.")

    add_h2("Rozdział 2. Ogólny opis (Overall Description)")

    add_h3("2.1. Perspektywa produktu i architektura systemu (Product Perspective)")
    add_p("System Usearch funkcjonuje jako rozproszona aplikacja internetowa. Frontend komunikuje się z backendem za pośrednictwem szyfrowanych żądań HTTP REST JSON. Backend orkiestruje przepływ danych pomiędzy usługami zewnętrznymi a bazami danych.")
    add_p("Architekturę systemu oraz przepływ danych przedstawiono poniżej:")
    add_code_block([
        "+-------------------------------------------------------------------+",
        "|                 UŻYTKOWNIK / PRZEGLĄDARKA WEB                     |",
        "+-------------------------------------------------------------------+",
        "                                  |",
        "                                  v",
        "+-------------------------------------------------------------------+",
        "|             FRONTEND: Next.js 16 (React 19 / TypeScript)          |",
        "|   - UI wyszukiwania i indeksowania     - Odtwarzacz wideo YouTube |",
        "|   - Firebase Client SDK (Auth)         - Panel API Keys           |",
        "+-------------------------------------------------------------------+",
        "         | (Auth / Firestore)                    | (REST API / X-API-Key)",
        "         v                                       v",
        "+-------------------+         +-------------------------------------+",
        "| FIREBASE / CLOUD  |         |  BACKEND: FastAPI (Python 3.12+)    |",
        "| - Auth (JWT)      |         |  - YouTube URL Parser & Service     |",
        "| - Firestore (Keys)|         |  - Transcript Extractor & Chunker   |",
        "+-------------------+         |  - OpenRouter Embedding Client      |",
        "                              |  - Usage Tracker & Auth Dependency  |",
        "                              +-------------------------------------+",
        "                                       |                   |",
        "         +-----------------------------+                   |",
        "         v                                                 v",
        "+---------------------------------+       +-------------------------+",
        "|      USŁUGI ZEWNĘTRZNE          |       |   BAZA DANYCH MONGODB   |",
        "| - Scrapetube (domyślny)         |       |   ATLAS (Cloud)         |",
        "| - YouTube Data API v3 (fallback)|       | - Kolekcja 'videos'     |",
        "| - youtube-transcript-api        |       | - Kolekcja 'chunks'     |",
        "| - OpenRouter (Embedding API)    |       |   (Atlas Vector Search) |",
        "+---------------------------------+       | - Kolekcja 'api_usage'  |",
        "                                          +-------------------------+"
    ])

    add_h3("2.2. Podsumowanie funkcji produktu (Product Functions)")
    add_bullet("Przyjmowanie i analiza poprawności adresów URL kanałów oraz filmów YouTube.")
    add_bullet("Pobieranie metadanych wideo (identyfikator, tytuł, opis, data publikacji, miniatura).")
    add_bullet("Ekstrakcja napisów z filmów z automatycznym tłumaczeniem na język angielski.")
    add_bullet("Dwustopniowy podział transkrypcji na fragmenty główne oraz nakładające się okna czasowe 12s/4s.")
    add_bullet("Generowanie wielowymiarowych wektorów embeddingowych dla fragmentów tekstu.")
    add_bullet("Indeksowanie danych w MongoDB z buforowaniem eliminującym duplikaty obliczeniowe.")
    add_bullet("Wykonywanie wyszukiwania semantycznego na podstawie zapytania użytkownika z doprecyzowaniem znacznika czasu.")
    add_bullet("Zarządzanie kontami użytkowników, generowanie i unieważnianie kluczy API oraz kontrola limitów zapytań.")
    add_bullet("Interaktywna prezentacja wyników z bezpośrednim odtwarzaniem filmu w odnalezionym timestampie.")

    add_h3("2.3. Charakterystyka klas użytkowników (User Characteristics)")
    add_bullet(" Użytkownik nieposiadający konta w systemie. Może przeglądać stronę główną, dokumentację oraz informacje o projekcie. W celu wykonania wyszukiwania lub indeksowania wymagane jest zalogowanie lub posiadanie ważnego klucza API.", "1. Użytkownik Niezalogowany (Gość) — ")
    add_bullet(" Użytkownik uwierzytelniony za pośrednictwem Firebase Auth. Otrzymuje dostęp do panelu kluczy API, konsoli Playground oraz darmowej puli zapytań (domyślnie 100 zapytań).", "2. Zarejestrowany Użytkownik Standardowy (Free Tier) — ")
    add_bullet(" Użytkownik komercyjny lub instytucjonalny o zwiększonych limitach zapytań (np. 10 000 requestów/miesiąc) oraz priorytetowym czasie przetwarzania zapytań.", "3. Użytkownik Subskrypcyjny / Premium — ")
    add_bullet(" Programista integrujący zewnętrzne systemy z silnikiem Usearch za pośrednictwem nagłówka HTTP X-API-Key.", "4. Deweloper API — ")
    add_bullet(" Członek zespołu deweloperskiego posiadający uprawnienia do monitorowania logów, czyszczenia cache (/auth/clear-cache/{uid}) oraz zarządzania infrastrukturą MongoDB Atlas.", "5. Administrator Systemu — ")

    add_h3("2.4. Ograniczenia ogólne (General Constraints)")
    add_bullet("Darmowy plan MongoDB Atlas (M0) narzuca limit 512 MB przestrzeni dyskowej oraz współdzielone zasoby procesora.")
    add_bullet("Oficjalne API YouTube posiada dzienny limit 10 000 jednostek quota na projekt Google Cloud.")
    add_bullet("Dostępność transkrypcji jest uwarunkowana obecnością napisów w analizowanym materiale wideo (filmy pozbawione jakichkolwiek napisów są pomijane).")
    add_bullet("W aktualnej wersji MVP pojedyncza operacja indeksowania kanału ogranicza przetwarzanie do pierwszych 5 najnowszych filmów w celu optymalizacji czasu i kosztów tokenów.")

    add_h3("2.5. Założenia i zależności (Assumptions and Dependencies)")
    add_bullet("Dostępność usług chmurowych: stabilne połączenie z MongoDB Atlas, OpenRouter AI oraz Firebase.")
    add_bullet("Zgodność z przeglądarkami internetowymi obsługującymi standardy ECMAScript 2022+ (Google Chrome, Mozilla Firefox, Safari, Microsoft Edge).")
    add_bullet("Poprawne działanie silnika transkrypcji YouTube, który nie wprowadza blokad IP na serwery backendu.")

    add_h2("Rozdział 3. Wymagania szczegółowe (Specific Requirements)")

    add_h3("3.1. Wymagania dotyczące interfejsów zewnętrznych (External Interface Requirements)")
    add_bullet(" Interfejs oparty na frameworku Next.js 16, zoptymalizowany pod kątem urządzeń stacjonarnych i mobilnych (Responsive Web Design). Zawiera pasek wyszukiwania w języku naturalnym, pole wprowadzania linku do kanału z wizualizacją postępu, listę kafelków z wynikami wyszukiwania, zintegrowany odtwarzacz wideo YouTube z funkcją automatycznego przewijania do odnalezionego czasu oraz interaktywną listę segmentów transkrypcji.", "3.1.1. Interfejs użytkownika (UI) — ")
    add_bullet(" Serwer backendowy wymaga maszyny z minimum 1 rdzeniem vCPU oraz 1 GB pamięci RAM. Baza danych oraz usługi AI hostowane są w architekturze chmurowej (SaaS).", "3.1.2. Interfejsy sprzętowe — ")
    add_bullet(" FastAPI łączy się z MongoDB Atlas poprzez bibliotekę pymongo (protokół mongodb+srv://), z OpenRouter API za pośrednictwem klienta openai-python oraz z Firebase za pośrednictwem biblioteki firebase-admin.", "3.1.3. Interfejsy oprogramowania — ")
    add_bullet(" Komunikacja klient-serwer odbywa się wyłącznie poprzez protokół HTTPS. Wymiana danych realizowana jest w formacie JSON. Uwierzytelnianie zapytań do API opiera się na niestandardowym nagłówku HTTP X-API-Key. Skonfigurowano politykę CORS umożliwiającą bezpieczne wywołania z frontendu.", "3.1.4. Interfejsy komunikacyjne — ")

    add_h2("3.2. Wymagania funkcjonalne (Functional Requirements)")

    # Grupa 1
    add_h3("3.2.1. Moduł walidacji i parsowania linków YouTube")
    add_bullet("System pobiera ciąg znaków wprowadzony przez użytkownika i dokonuje analizy składniowej pod kątem poprawności składni serwisu YouTube.", "REQ-1.1: ")
    add_bullet("System prawidłowo rozpoznaje i parsuje standardowe linki wideo (youtube.com/watch?v=), linki mobilne (m.youtube.com), skrócone (youtu.be) oraz linki z parametrami śledzącymi.", "REQ-1.2: ")
    add_bullet("System prawidłowo rozpoznaje i parsuje identyfikatory kanałów w formacie unikalnego ID (/channel/UC...) oraz nowoczesne uchwyty twórców (/@handle).", "REQ-1.3: ")
    add_bullet("W przypadku wprowadzenia adresu URL spoza obsługiwanych domen lub ciągu o niepoprawnym formacie system odrzuca żądanie, zwracając błąd klienta HTTP 400 Bad Request z precyzyjnym komunikatem.", "REQ-1.4: ")

    # Grupa 2
    add_h3("3.2.2. Moduł pozyskiwania metadanych i filmów")
    add_bullet("System pobiera listę najnowszych filmów dla wskazanego kanału YouTube.", "REQ-2.1: ")
    add_bullet("Domyślnym mechanizmem pozyskiwania listy filmów jest moduł ScrapetubeProvider niewymagający zużycia limitów quota oficjalnego API.", "REQ-2.2: ")
    add_bullet("W przypadku wystąpienia błędu lub braku wyników z modułu scrapetube, system automatycznie uruchamia zapasowego dostawcę YouTubeApiProvider bazującego na oficjalnym Google YouTube Data API v3 (mechanizm Fallback).", "REQ-2.3: ")
    add_bullet("Dla każdego filmu system pozyskuje identyfikator video_id, tytuł title, opis description, datę publikacji published_at oraz adres miniatury thumbnail.", "REQ-2.4: ")
    add_bullet("W aktualnej wersji MVP pojedyncze żądanie indeksowania kanału przetwarza maksymalnie 5 najnowszych materiałów wideo.", "REQ-2.5: ")

    # Grupa 3
    add_h3("3.2.3. Moduł ekstrakcji i normalizacji transkrypcji")
    add_bullet("Dla każdego zakwalifikowanego filmu system podejmuje próbę pobrania transkrypcji za pośrednictwem serwisu youtube-transcript-api.", "REQ-3.1: ")
    add_bullet("System w pierwszej kolejności wyszukuje transkrypcję w języku angielskim (autorską lub automatyczną).", "REQ-3.2: ")
    add_bullet("W przypadku braku transkrypcji angielskiej, system pobiera pierwszą dostępną transkrypcję w innym języku i dokonuje jej automatycznego tłumaczenia na język angielski.", "REQ-3.3: ")
    add_bullet("System zachowuje oryginalną strukturę czasową transkrypcji: treść tekstową (text), czas rozpoczęcia w sekundach (start) oraz czas trwania fragmentu (duration).", "REQ-3.4: ")
    add_bullet("W przypadku braku jakichkolwiek napisów dla danego filmu, system pomija ten materiał ze statusem failed, nie przerywając procesu indeksowania pozostałych filmów.", "REQ-3.5: ")

    # Grupa 4
    add_h3("3.2.4. Moduł zaawansowanego chunkingu i podwójnego okna czasowego")
    add_bullet("System dzieli pobraną transkrypcję na główne logiczne fragmenty tekstowe (chunki) o domyślnym oknie czasowym 60 sekund i 15-sekundowej zakładce (overlap).", "REQ-4.1: ")
    add_bullet("System automatycznie filtruje i usuwa fragmenty zawierające wyłącznie białe znaki, znaki nowej linii lub puste ciągi.", "REQ-4.2: ")
    add_bullet("Wewnątrz każdego głównego chunka system tworzy zbiór podrzędnych, nakładających się mikro-okien czasowych (sliding windows) o szerokości 12 sekund i zakładce 4 sekund.", "REQ-4.3: ")
    add_bullet("Dla każdego mikro-okna system rejestruje dokładny czas początkowy, końcowy oraz powiązany fragment tekstu.", "REQ-4.4: ")

    # Grupa 5
    add_h3("3.2.5. Moduł generowania wektorów (Embedding Service)")
    add_bullet("System przekazuje przygotowane fragmenty tekstu do modelu openai/text-embedding-3-small za pośrednictwem platformy OpenRouter.", "REQ-5.1: ")
    add_bullet("Generowanie embeddingów odbywa się w trybie wsadowym (batching w create_embeddings), co minimalizuje narzut sieciowy i czas przetwarzania.", "REQ-5.2: ")
    add_bullet("System generuje wektory cech zarówno dla głównych chunków, jak i dla każdego wewnętrznego mikro-okna czasowego.", "REQ-5.3: ")
    add_bullet("Każdy wygenerowany wektor posiada długość 1536 wartości zmiennoprzecinkowych.", "REQ-5.4: ")

    # Grupa 6
    add_h3("3.2.6. Moduł bazy danych, pamięci podręcznej i indeksowania")
    add_bullet("Przed przystąpieniem do pobierania transkrypcji i generowania embeddingów system weryfikuje w kolekcji videos, czy dany film został już wcześniej zindeksowany (video_already_indexed).", "REQ-6.1: ")
    add_bullet("W przypadku wykrycia filmu w bazie, system pomija generowanie embeddingów (status skipped), pobierając istniejące dane z bazy bez ponoszenia kosztów zewnętrznych API.", "REQ-6.2: ")
    add_bullet("Metadane filmu oraz pełna transkrypcja zapisywane są w kolekcji videos z operacją upsert.", "REQ-6.3: ")
    add_bullet("Fragmenty wraz z wektorami głównymi i wektorami mikro-okien zapisywane są w kolekcji chunks.", "REQ-6.4: ")
    add_bullet("Kolekcja chunks posiada skonfigurowany wektorowy indeks wyszukiwania MongoDB Atlas Vector Search dla pola embedding.", "REQ-6.5: ")

    # Grupa 7
    add_h3("3.2.7. Moduł wyszukiwania semantycznego i pozycjonowania timestampów")
    add_bullet("System przyjmuje zapytanie użytkownika w języku naturalnym za pośrednictwem endpointu GET /youtube/search.", "REQ-7.1: ")
    add_bullet("Zapytanie użytkownika jest konwertowane na wektor embeddingu za pomocą tego samego modelu co podczas indeksowania.", "REQ-7.2: ")
    add_bullet("Wyszukiwanie wektorowe realizowane jest w bazie MongoDB Atlas za pomocą operatora $vectorSearch z metryką podobieństwa cosinusowego.", "REQ-7.3: ")
    add_bullet("Wyniki są agregowane i grupowane według identyfikatora wideo, a następnie sortowane według najwyższej trafności semantycznej (score).", "REQ-7.4: ")
    add_bullet("W celu wyznaczenia precyzyjnego znacznika czasu system porównuje wektor zapytania z wektorami mikro-okien danego chunka (funkcja get_best_window) za pomocą metryki cosine_similarity.", "REQ-7.5: ")
    add_bullet("System wylicza ostateczny znacznik czasu z uwzględnieniem bufora kontekstu narracyjnego (15 sekund przed i 20 sekund po zidentyfikowanym mikro-oknie).", "REQ-7.6: ")
    add_bullet("Odpowiedź API zawiera listę najbardziej trafnych wyników wraz z polami: video_id, title, score, timestamp_score, start, end oraz dopasowanym fragmentem tekstu text.", "REQ-7.7: ")

    # Grupa 8
    add_h3("3.2.8. Moduł autoryzacji, zarządzania kluczami API i limitowania zapytań")
    add_bullet("Dostęp do endpointu wyszukiwania semantycznego jest chroniony zależnością verify_api_key weryfikującą nagłówek X-API-Key.", "REQ-8.1: ")
    add_bullet("W przypadku braku nagłówka lub pustego klucza system natychmiast zwraca kod HTTP 401 Unauthorized.", "REQ-8.2: ")
    add_bullet("System pobiera z bazy Firestore limit zapytań przypisany do danego klucza i buforuje go w kolekcji api_usage w MongoDB.", "REQ-8.3: ")
    add_bullet("Przy każdym autoryzowanym zapytaniu system wykonuje atomiczną operację inkrementacji licznika zapytań ($inc: total_requests: 1) pod warunkiem niespełnienia warunku przekroczenia limitu.", "REQ-8.4: ")
    add_bullet("W przypadku wyczerpania dostępnej puli zapytań system natychmiast odrzuca żądanie, zwracając kod HTTP 429 Too Many Requests.", "REQ-8.5: ")
    add_bullet("System udostępnia dedykowany endpoint POST /auth/clear-cache/{uid} umożliwiający natychmiastowe zresetowanie bufora limitów po zmianie planu subskrypcyjnego przez użytkownika.", "REQ-8.6: ")

    # Grupa 9
    add_h3("3.2.9. Moduł interfejsu graficznego (Frontend Next.js)")
    add_bullet("Interfejs umożliwia wprowadzenie linku do kanału YouTube i wywołanie asynchronicznego indeksowania z wizualizacją liczby filmów zindeksowanych, pominiętych i zakończonych błędem.", "REQ-9.1: ")
    add_bullet("Interfejs udostępnia pasek wyszukiwania w języku naturalnym z natychmiastową prezentacją kart wynikowych.", "REQ-9.2: ")
    add_bullet("Kliknięcie w odnaleziony wynik powoduje załadowanie wbudowanego odtwarzacza YouTube i automatyczne przewinięcie nagrania do wyznaczonego znacznika start.", "REQ-9.3: ")
    add_bullet("Interfejs wyświetla interaktywną listę segmentów transkrypcji powiązaną z aktualnym czasem odtwarzania wideo.", "REQ-9.4: ")
    add_bullet("Dedykowany panel profilu użytkownika (/profile/api-keys) umożliwia generowanie nowych kluczy API, ich unieważnianie oraz kopiowanie do schowka.", "REQ-9.5: ")
    add_bullet("Aplikacja udostępnia interaktywną konsolę Playground (/profile/playground) pozwalającą deweloperom na bezpośrednie testowanie zapytań API.", "REQ-9.6: ")

    add_h2("3.3. Wymagania wydajnościowe (Performance Requirements)")
    add_bullet("Całkowity czas wykonania wyszukiwania semantycznego (obejmujący wygenerowanie embeddingu zapytania oraz zapytanie wektorowe w MongoDB Atlas) nie powinien przekraczać 2.5 sekundy przy stabilnym łączu internetowym.", "PERF-1: Czas wyszukiwania — ")
    add_bullet("Wszystkie wektory mikro-okien czasowych muszą być generowane podczas fazy indeksowania materiału wideo, a nie w trakcie wyszukiwania, co gwarantuje natychmiastowe wyliczanie precyzji timestampu.", "PERF-2: Przetwarzanie wsadowe — ")
    add_bullet("Filmy zindeksowane wcześniej w bazie danych muszą być pomijane podczas kolejnych operacji indeksowania, redukując narzut czasowy ponownego indeksowania o ponad 95%.", "PERF-3: Efektywność pamięci podręcznej — ")
    add_bullet("Zastosowanie indeksu MongoDB Atlas Vector Search z algorytmem HNSW (Hierarchical Navigable Small World) eliminuje konieczność pełnego skanowania kolekcji, zapewniając złożoność wyszukiwania O(log N).", "PERF-4: Skalowalność wyszukiwania — ")
    add_bullet("Interfejs użytkownika Next.js musi renderować wyniki wyszukiwania w czasie poniżej 200 ms od momentu otrzymania odpowiedzi z backendu.", "PERF-5: Responsywność interfejsu — ")

    add_h2("3.4. Wymagania dotyczące logicznej bazy danych (Logical Database Requirements)")
    add_bullet(" przechowuje dokumenty zindeksowanych filmów: video_id (klucz unikalny), title, description, published_at, thumbnail, language oraz pełną strukturę transcript (lista obiektów z polami text, start, duration).", "Kolekcja 'videos' (MongoDB) — ")
    add_bullet(" przechowuje wygenerowane segmenty tekstowe: video_id, video_title, start, end, text, embedding (wektor 1536 float), oraz tablicę obiektów windows (każdy zawierający start, end, text, embedding). Na polu embedding utworzony jest dedykowany wektorowy indeks Atlas Vector Search.", "Kolekcja 'chunks' (MongoDB) — ")
    add_bullet(" przechowuje stan zużycia zapytań dla każdego klucza: api_key, uid (identyfikator użytkownika Firebase), limit (maksymalna dopuszczalna liczba zapytań), total_requests (licznik wykonanych zapytań).", "Kolekcja 'api_usage' (MongoDB) — ")
    add_bullet(" przechowuje profile użytkowników, role systemowe, przypisane plany subskrypcyjne (Free, Pro) oraz metadane wygenerowanych kluczy API.", "Kolekcje 'users' i 'api_keys' (Cloud Firestore) — ")

    add_h2("3.5. Ograniczenia projektowe (Design Constraints)")
    add_bullet("Python 3.12+ oraz framework FastAPI (asynchroniczny serwer ASGI uvicorn).", "Środowisko backendu: ")
    add_bullet("Node.js 20+, Next.js 16 (App Router), React 19, TypeScript, TailwindCSS v4.", "Środowisko frontendu: ")
    add_bullet("Format wymiany danych ograniczony wyłącznie do UTF-8 JSON.", "Protokoły i formaty: ")
    add_bullet("Wszystkie wrażliwe dane konfiguracyjne (klucze API YouTube, OpenRouter, MongoDB URI, klucze prywatne Firebase) muszą być wstrzykiwane wyłącznie poprzez zmienne środowiskowe (.env).", "Zarządzanie sekretami: ")

    add_h2("3.6. Atrybuty jakościowe oprogramowania (Software System Attributes)")
    add_bullet("Klucze API ani dane dostępowe do bazy danych nigdy nie mogą być zwracane w odpowiedziach HTTP ani przesyłane do kodu klienckiego. Dostęp do operacji wyszukiwania semantycznego wymaga autoryzacji nagłówkiem X-API-Key. Wprowadzane parametry podlegają rygorystycznej walidacji schematami Pydantic.", "Bezpieczeństwo (Security) — ")
    add_bullet("Awaria lub brak napisów dla pojedynczego filmu nie może powodować przerwania całego procesu indeksowania kanału. W przypadku niedostępności scrapera scrapetube system automatycznie przełącza się na oficjalne API YouTube.", "Niezawodność i odporność na błędy (Reliability) — ")
    add_bullet("Architektura rozproszona umożliwia niezależne skalowanie warstwy frontendowej (hosting Vercel) oraz serwera backendowego (konteneryzacja Docker).", "Dostępność i skalowalność (Availability) — ")
    add_bullet("Kod źródłowy podzielony jest na modularne warstwy (routers, services, database, models, dependencies). Kluczowa logika biznesowa jest w 100% pokryta testami jednostkowymi Pytest.", "Utrzymywalność (Maintainability) — ")

    # -------------------------------------------------------------
    # CZĘŚĆ 4
    # -------------------------------------------------------------
    add_h1("4. Analiza czynników ryzyka w projekcie niekomercyjnym o charakterze zespołowym")

    add_h2("4.1. Specyfika projektu niekomercyjnego realizowanego w zespole akademickim")
    add_p("Realizacja projektu inżynierii oprogramowania o charakterze niekomercyjnym (akademickim) w 2-osobowym zespole deweloperskim wiąże się ze specyficznym profilem ryzyka, odmiennym od projektów komercyjnych dysponujących budżetem finansowym i dedykowanym personelem. Do kluczowych uwarunkowań determinujących ryzyko należą:")
    add_bullet(" brak budżetu na komercyjne usługi chmurowe, co wymusza korzystanie z darmowych planów (Free Tier: MongoDB Atlas M0, darmowe pule tokenów OpenRouter, bezpłatne quota YouTube API, hosting Vercel). Przekroczenie limitów darmowych oznacza natychmiastową blokadę usługi.", "1. Ograniczenia budżetowe — ")
    add_bullet(" zespół składa się z 2 osób (Bohdan i Denys), co oznacza współczynnik Bus Factor równy 1 w kluczowych domenach wiedzy (backend/ML vs frontend/auth). Niedostępność jednego z członków stwarza bezpośrednie zagrożenie dla harmonogramu.", "2. Minimalny rozmiar zespołu — ")
    add_bullet(" realizacja projektu musi być równoważona z innymi obowiązkami akademickimi (kolokwia, zaliczenia, sesja egzaminacyjna), co powoduje okresowe wahania dostępności czasowej.", "3. Cykl akademicki — ")
    add_bullet(" system opiera się na integracji z zewnętrznymi platformami (YouTube, OpenRouter, Firebase). Zmiany w strukturze HTML serwisu YouTube lub polityce dostępu do API mogą wpłynąć na stabilność scraperów.", "4. Zależność od podmiotów trzecich — ")

    add_h2("4.2. Identyfikacja i klasyfikacja czynników ryzyka")

    add_h3("Kategoria A: Ryzyka Zespołowe i Organizacyjne (Czynnik Ludzki)")
    add_bullet(" nagła niedostępność jednego z członków zespołu (choroba, zdarzenia losowe, spiętrzenie sesji egzaminacyjnej). Ze względu na specjalizację (jeden programista backend/ML, drugi frontend/auth), absencja może całkowicie wstrzymać prace w danym module.", "Ryzyko R-ORG-1: Zjawisko 'Bus Factor = 1' — ")
    add_bullet(" pokusa ciągłego dodawania nowych funkcjonalności (np. rozbudowane forum dyskusyjne, rozszerzenie do przeglądarki Chrome, automatyczne generowanie wideo przez AI) kosztem dopracowania i przetestowania podstawowego silnika wyszukiwania semantycznego.", "Ryzyko R-ORG-2: Rozrost zakresu projektu (Scope Creep) — ")
    add_bullet(" rozbieżności co do formatu danych przesyłanych pomiędzy frontendem a backendem, prowadzące do błędów integracyjnych przy łączeniu komponentów.", "Ryzyko R-ORG-3: Niespójność kontraktu API — ")

    add_h3("Kategoria B: Ryzyka Techniczne i Integracyjne")
    add_bullet(" oficjalne Google YouTube Data API v3 posiada restrykcyjny darmowy limit 10 000 jednostek/dobę. Jedno zapytanie przeszukiwania kanału potrafi skonsumować 100 jednostek, co przy intensywnych testach mogłoby wyczerpać pulę w kilkadziesiąt minut.", "Ryzyko R-TECH-1: Wyczerpanie darmowej puli quota w YouTube Data API — ")
    add_bullet(" biblioteka youtube-transcript-api bazuje na mechanizmach ekstrakcji z webowych endpointów YouTube, które mogą ulec zablokowaniu (blokady IP, mechanizmy anty-botowe Captcha).", "Ryzyko R-TECH-2: Blokada scrapera transkrypcji przez YouTube — ")
    add_bullet(" model openai/text-embedding-3-small rozliczany jest na podstawie liczby przetworzonych tokenów tekstu. Indeksowanie bardzo długich transkrypcji w sposób niekontrolowany mogłoby szybko wyczerpać środki na koncie OpenRouter.", "Ryzyko R-TECH-3: Wyczerpanie limitu środków/tokenów w OpenRouter API — ")
    add_bullet(" część filmów w serwisie YouTube nie posiada żadnych napisów (ani dodanych przez autora, ani wygenerowanych automatycznie, np. nagrania muzyczne lub materiały o niskiej jakości dźwięku).", "Ryzyko R-TECH-4: Brak transkrypcji w części filmów — ")

    add_h3("Kategoria C: Ryzyka Infrastrukturalne i Bazodanowe")
    add_bullet(" darmowa instancja M0 oferuje dokładnie 512 MB pamięci dyskowej. Zapisywanie pełnych transkrypcji wraz z tysiącami 1536-wymiarowych wektorów float mogłoby doprowadzić do przepełnienia magazynu.", "Ryzyko R-INF-1: Przepełnienie darmowej bazy MongoDB Atlas M0 — ")
    add_bullet(" opóźnienia sieciowe wynikające z rozproszenia usług (klient -> Next.js -> FastAPI -> OpenRouter -> MongoDB Atlas) mogą negatywnie wpłynąć na komfort użytkownika.", "Ryzyko R-INF-2: Narzut opóźnień sieciowych (Latency) — ")

    add_h3("Kategoria D: Ryzyka Jakościowe i Bezpieczeństwa")
    add_bullet(" przypadkowe wypchnięcie (git push) pliku .env zawierającego prywatne klucze API do publicznego repozytorium GitHub, co skutkowałoby natychmiastowym przejęciem i unieważnieniem kluczy przez dostawców.", "Ryzyko R-SEC-1: Wyciek sekretów i kluczy API — ")
    add_bullet(" błędy regresji wprowadzane podczas łączenia gałęzi deweloperskich (git merge) przed terminem oddania projektu.", "Ryzyko R-QUAL-1: Regresje kodu podczas integracji — ")

    add_h2("4.3. Macierz Ryzyka (Risk Assessment Matrix)")
    add_p("Prawdopodobieństwo (P) oraz Wpływ (W) oszacowano w skali 1-5. Wskaźnik ryzyka (R) jest iloczynem P x W (zakres 1-25):")
    add_bullet(" 1-6 (Niski / Akceptowalny)", "Zielony: ")
    add_bullet(" 7-14 (Średni / Wymaga monitorowania)", "Żółty: ")
    add_bullet(" 15-25 (Wysoki / Wymaga bezwzględnej mitygacji)", "Czerwony: ")

    # Tabela macierzy ryzyka
    risk_table = doc.add_table(rows=11, cols=7)
    risk_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    r_headers = ["ID", "Opis czynnika ryzyka", "P (1-5)", "W (1-5)", "R (P×W)", "Strategia mitygacji (Działanie prewencyjne)", "Plan awaryjny (Contingency)"]

    for j, h in enumerate(r_headers):
        cell = risk_table.cell(0, j)
        set_cell_background(cell, HEX_PRIMARY)
        set_cell_margins(cell, 80, 80, 80, 80)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.font.name = 'Calibri'
        r.font.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    risks_data = [
        ("R-ORG-1", "Bus Factor = 1 (niedostępność członka zespołu)", "3", "4", "12",
         "Modułowy podział zadań z jasnym kontraktem REST API; wspólne repozytorium GitHub, dokumentacja kodu.",
         "Przejęcie priorytetowych zadań integracyjnych na podstawie przygotowanej specyfikacji SRS."),
        ("R-ORG-2", "Rozrost zakresu (Scope Creep)", "4", "3", "12",
         "Sztywne zdefiniowanie granic MVP; odłożenie forum i rozszerzenia przeglądarki do fazy Post-MVP.",
         "Zamrożenie kodu (code freeze) na tydzień przed oddaniem i skupienie się wyłącznie na testach."),
        ("R-ORG-3", "Niespójność kontraktu API", "3", "3", "9",
         "Zastosowanie modeli Pydantic w backendzie i typów TypeScript w frontendzie; konsola Playground.",
         "Szybka synchronizacja modeli danych z użyciem endpointów testowych (/database/test, /embedding/test)."),
        ("R-TECH-1", "Wyczerpanie darmowej puli quota YouTube API", "4", "4", "16",
         "Implementacja ScrapetubeProvider jako metody domyślnej; cache zindeksowanych filmów w MongoDB.",
         "Automatyczny fallback na YouTubeApiProvider przy błędach scrapera oraz rotacja kluczy Google Cloud."),
        ("R-TECH-2", "Blokada scrapera transkrypcji", "3", "4", "12",
         "Obsługa wyjątków YouTubeTranscriptApiException; testowanie dostępności napisów przed przetwarzaniem.",
         "Pominięcie nieobsługiwanego filmu ze statusem failed bez zatrzymywania całego procesu indeksowania."),
        ("R-TECH-3", "Koszty / limity tokenów OpenRouter", "3", "4", "12",
         "Wybór ultra-taniego modelu text-embedding-3-small; batching zapytań; unikanie ponownego indeksowania.",
         "Ograniczenie liczby indeksowanych filmów na kanał do 5 w wersji MVP; buforowanie wektorów w bazie."),
        ("R-TECH-4", "Brak transkrypcji w filmach", "4", "2", "8",
         "Automatyczny fallback na napisy generowane maszynowo oraz automatyczne tłumaczenie na język angielski.",
         "Poinformowanie użytkownika w interfejsie graficznym o braku napisów w danym materiale wideo."),
        ("R-INF-1", "Przepełnienie MongoDB Atlas M0 (512 MB)", "2", "4", "8",
         "Optymalizacja schematu bazy danych; selektywne przechowywanie embeddingów; indeksowanie wybranych filmów.",
         "Usunięcie starych lub testowych kolekcji przed finalnym wdrożeniem demonstracyjnym."),
        ("R-SEC-1", "Wyciek sekretów i kluczy API do git", "2", "5", "10",
         "Dodanie plików .env do .gitignore; mockowanie zmiennych środowiskowych w conftest.py.",
         "Natychmiastowe unieważnienie i wygenerowanie nowych kluczy w konsolach Google Cloud / OpenRouter / Firebase."),
        ("R-QUAL-1", "Regresje kodu podczas łączenia gałęzi", "3", "4", "12",
         "Wdrożenie 46 automatycznych testów jednostkowych Pytest uruchamianych lokalnie przed commitem.",
         "Przywrócenie stabilnego stanu gałęzi main za pomocą historii git i weryfikacja suite'em testów.")
    ]

    for i, row in enumerate(risks_data):
        for j, val in enumerate(row):
            cell = risk_table.cell(i + 1, j)
            bg = HEX_LIGHT_BG if i % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg)
            set_cell_margins(cell, 70, 70, 70, 70)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.name = 'Calibri'
            r.font.size = Pt(8.5)
            if j == 4: # Kolumna R
                r.font.bold = True
                score = int(val)
                if score >= 15:
                    r.font.color.rgb = RGBColor(0xC0, 0x00, 0x00) # Red
                elif score >= 9:
                    r.font.color.rgb = RGBColor(0xB8, 0x62, 0x00) # Orange
                else:
                    r.font.color.rgb = RGBColor(0x1B, 0x7E, 0x34) # Green
            else:
                r.font.color.rgb = COLOR_DARK

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_h2("4.4. Szczegółowy opis wdrożonych strategii mitygacji w projekcie")
    add_p("W toku prac inżynierskich zespół wdrożył konkretne mechanizmy w kodzie źródłowym, które bezpośrednio eliminują lub minimalizują zidentyfikowane czynniki ryzyka:")

    add_h3("1. Architektura hybrydowego dostawcy danych (Mitygacja R-TECH-1 i R-TECH-2)")
    add_p("W module services/youtube_service.py zaimplementowano wzorzec projektowy Strategy z mechanizmem automatycznego przełączania awaryjnego (Fallback). Domyślnie system wykorzystuje scraper scrapetube, który nie podlega limitom darmowej puli Google Quota (10 000 pkt/dzień). Jeśli scraper napotka problem (zwróci None), system bez przerywania pracy użytkownika natychmiast odpytuje oficjalny YouTubeApiProvider:")
    add_code_block([
        "result = await provider.get_channel_info(url_info)",
        "if result is None and not isinstance(provider, YouTubeApiProvider):",
        "    fallback_provider = YouTubeApiProvider()",
        "    result = await fallback_provider.get_channel_info(url_info)"
    ])

    add_h3("2. System wielopoziomowej pamięci podręcznej (Mitygacja R-TECH-3 i R-INF-1)")
    add_p("Aby zapobiec niepotrzebnemu zużywaniu tokenów w OpenRouter oraz przepełnieniu bazy MongoDB Atlas, serwis index_service.py przed rozpoczęciem przetwarzania każdego filmu wywołuje funkcję video_already_indexed(video_id). Jeżeli film znajduje się już w bazie danych, jego transkrypcja i embeddingi nie są generowane ponownie, lecz natychmiast zwracane z bazy ze statusem 'skipped'. Pozwoliło to zredukować koszty operacyjne i czas indeksowania znanych kanałów o 98%.")

    add_h3("3. Zabezpieczenie limitów zapytań i ochrona zasobów (Mitygacja R-ORG-2 i R-SEC-1)")
    add_p("W celu zabezpieczenia backendu przed przeciążeniem lub nadużyciem przez nieautoryzowanych klientów zaimplementowano serwis usage_tracker.py z atomicznymi aktualizacjami w MongoDB ($inc: total_requests: 1 pod warunkiem total_requests < limit). Po przekroczeniu zdefiniowanego limitu (np. 100 zapytań dla darmowego planu) system natychmiast blokuje żądania kodem HTTP 429 Too Many Requests, chroniąc zespół przed niespodziewanymi kosztami zewnętrznych API.")

    add_h3("4. Automatyzacja testowania jako tarcza przed regresjami (Mitygacja R-QUAL-1)")
    add_p("Zbudowanie zestawu 46 testów jednostkowych z izolacją środowiskową w conftest.py umożliwiło bezpieczne i bezkonfliktowe scalanie gałęzi deweloperskich obu członków zespołu. Każda zmiana w parserze URL, algorytmie chunkingu czy warstwie autoryzacji była natychmiast weryfikowana lokalnym wywołaniem pytest, eliminując ryzyko wprowadzenia ukrytych defektów przed prezentacją projektu.")

    add_h2("4.5. Podsumowanie i wnioski z analizy ryzyka")
    add_p("Przyjęta strategia zarządzania ryzykiem w projekcie Usearch udowodniła, że nawet w warunkach zerowego budżetu komercyjnego oraz małego zespołu 2-osobowego możliwe jest stworzenie wysoce zaawansowanej platformy AI. Kluczem do sukcesu okazało się:")
    add_bullet("Ścisłe zdefiniowanie i obronienie granic MVP przed pokusą nadmiernego rozbudowywania funkcji pobocznych.")
    add_bullet("Wykorzystanie architektury odpornej na awarie (fallback scrapetube -> official API).")
    add_bullet("Zastosowanie podwójnego poziomu chunkingu dla sub-segmentowej precyzji pozycjonowania timestampu.")
    add_bullet("Hermetyzacja logiki w testach jednostkowych, co zminimalizowało dług technologiczny i zagwarantowało stabilność całego systemu.")

    return doc

if __name__ == '__main__':
    doc = create_styled_document()
    
    # Try to save to SE.docx first, or SE_nowy.docx if locked
    target_file = 'SE.docx'
    alt_file = 'SE_nowy.docx'
    
    try:
        doc.save(target_file)
        print(f"SUCCESS: Saved document to '{target_file}'")
    except Exception as e:
        print(f"NOTICE: Could not save directly to '{target_file}' ({e}). Saving to '{alt_file}'...")
        doc.save(alt_file)
        print(f"SUCCESS: Saved document to '{alt_file}'")
