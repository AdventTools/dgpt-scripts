# dgpt — Diplome și planșe pentru *Din grijă pentru tine*

Generator PPTX pentru campania de educație și prevenție medicală [**Din grijă pentru tine**](https://dingrijapentrutine.ro/), inițiată de Biserica Adventistă de Ziua a Șaptea din România.

Pentru fiecare ediție a evenimentului (un weekend, într-un oraș diferit), organizatorii au nevoie de:
- O **diplomă personalizată** pentru fiecare medic și asistent care participă voluntar.
- O **diplomă pentru invitați** (oficialități: primar, manager spital, senator, etc.).
- O **planșă** pentru fiecare cabinet medical din locația evenimentului (cu numele medicului care îl deservește).

Scriptul citește 3 fișiere Excel cu listele participanților și generează în câteva secunde toate PPTX-urile, gata de tipărit.

---

## Cuprins

- [Cerințe](#cerințe)
- [Instalare](#instalare)
- [Folosire — meniu interactiv](#folosire--meniu-interactiv)
- [Format date](#format-date)
- [Adaptare pentru evenimentul tău](#adaptare-pentru-evenimentul-tău)
- [Cum funcționează](#cum-funcționează)

---

## Cerințe

- Python 3.10 sau mai nou
- macOS, Windows sau Linux
- PowerPoint, Keynote, sau LibreOffice Impress (pentru deschiderea PPTX-urilor)

---

## Instalare

```bash
git clone https://github.com/AdventTools/dgpt-scripts.git
cd dgpt-scripts
python3 -m venv .venv
```

Activează mediul virtual:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (cmd)
.venv\Scripts\activate.bat
```

Instalează dependențele:

```bash
pip install -r requirements.txt
```

---

## Folosire — meniu interactiv

```bash
python run.py
```

```
  GENERARE
    1) Genereaza TOT (planse + toate diplomele)
    2) Genereaza doar planse cabinete
    3) Genereaza doar diplome (medici + asistente + diverse)

  DATE
    4) Editeaza data/medici.xlsx
    5) Editeaza data/asistenti.xlsx
    6) Editeaza data/alte_diplome.xlsx
    7) Editeaza data/event_detail.xlsx (data + locatie)
    8) Editeaza template-uri

  IESIRI / GIT
    o) Deschide folderul output/
    g) Commit + push pe GitHub
    0) Iesire
```

Pentru prima rulare:

1. Lasă `run.py` să copieze exemplele pentru tine — la prima rulare îți propune. Sau manual:
   ```
   cp examples/*.xlsx data/   # macOS / Linux
   copy examples\*.xlsx data\ # Windows (cmd)
   ```
2. Editează `data/event_detail.xlsx` cu data + orașul ediției curente (opțiunea **7**).
3. Editează template-urile din `templates/` și înlocuiește placeholderele `[Nume Președinte]`, `[Nume Director Departament]`, `[Nume Director Sănătate]` cu numele reale ale semnatarilor (opțiunea **8**).
4. Completează listele de medici, asistenți și diverși invitați (opțiunile **4–6**).
5. Generează tot (opțiunea **1**).

Rezultatele apar în `output/`:
- `Planse_cabinete.pptx`
- `Diplome_medici.pptx`
- `Diplome_asistenti.pptx`
- `Diplome_diverse.pptx` (doar dacă `data/alte_diplome.xlsx` există)

> Poți rula și fără meniu: `python src/generate_planse.py`, `python src/generate_diplome.py`.

---

## Format date

Toate fișierele sunt **Excel (.xlsx)**, o singură foaie pe fișier, header pe rândul 1.

### `data/medici.xlsx`

| cabinet | nume |
|---|---|
| Audiologie | Dr. Exemplu Unu |
| Cardiologie | Dr. Exemplu Doi |
| Stomatologie | Dr. Exemplu Trei |
| *(gol)* | Dr. Exemplu Patru |

- O linie per (cabinet, medic). Dacă un medic e la 2 cabinete, scrii 2 rânduri.
- Coloana `nume` include titulatura (`Dr.`, `Prof. Dr.`, `Conf. Dr.`).
- Dacă `cabinet` e gol, medicul primește doar diplomă (nu și planșă).
- Diacritice românești suportate (ă, â, î, ș, ț).

### `data/asistenti.xlsx`

| nume |
|---|
| Asistent Exemplu Unu |
| Asistent Exemplu Doi |

- O linie per asistent. Fără titulatură. Format: `Prenume Nume`.

### `data/alte_diplome.xlsx` (opțional — pentru invitați / oficialități)

| titulatura | nume |
|---|---|
| Primar | Exemplu Unu |
| Manager | Exemplu Doi |
| Senator | Exemplu Trei |

- Pe diplomă apare: `{titulatura} {nume}`.
- Dacă fișierul lipsește, secțiunea e sărită.

### `data/event_detail.xlsx`

| data | locatie |
|---|---|
| DD-DD luna AAAA | Oras |

Apare pe fiecare diplomă: „desfășurat în perioada `{data}`, `{locatie}`”.

---

## Adaptare pentru evenimentul tău

Înainte de prima utilizare, editează template-urile din `templates/` să reflecte organizația și semnatarii tăi:

### `templates/model_diploma.pptx`

Conține 4 placeholdere pe care **trebuie** să le înlocuiești manual în PowerPoint:
- `Dr. Nume Prenume` (Shape 0) — se înlocuiește automat de script per slide, nu o atinge
- `[Nume Președinte]`
- `[Nume Director Departament]`
- `Dr. [Nume Director Sănătate]`

Restul textului (titlul diplomei, mențiunea proiectului, etc.) îl poți schimba liber.

### `templates/Planse.pptx`

Conține placeholderele `{{medic}}` și `{{cabinet}}` — se înlocuiesc automat, nu le atinge. Restul (fontul Impact, logo, layout) îl poți personaliza.

### Pentru fiecare ediție

Modifici doar:
1. **`data/event_detail.xlsx`** — data + orașul
2. **`data/medici.xlsx`** — lista medicilor cu cabinetele lor
3. **`data/asistenti.xlsx`** — lista asistenților
4. **`data/alte_diplome.xlsx`** — invitați / oficialități (dacă e cazul)

Apoi rulezi `python run.py` → opțiunea **1**.

---

## Cum funcționează

**generate_planse.py** citește `data/medici.xlsx` și pentru fiecare pereche (cabinet, medic) clonează slide-ul template din `Planse.pptx`, înlocuind placeholderele `{{medic}}` și `{{cabinet}}`. Fontul Impact (80pt medic, 115pt cabinet) e respectat când textul încape pe un rând; altfel se scalează automat (min 28pt).

**generate_diplome.py** citește `data/event_detail.xlsx`, `data/medici.xlsx` (dedup după nume), `data/asistenti.xlsx` și, dacă există, `data/alte_diplome.xlsx`. Pentru fiecare persoană clonează slide-ul din `model_diploma.pptx` și înlocuiește Shape 0 (numele) și Shape 2 (perioada + orașul). Fontul Calibri (max 36pt, min 20pt) se auto-scalează.

---

## Structură proiect

```
dgpt-scripts/
├── data/                       Listele tale reale (gitignored)
│   ├── medici.xlsx
│   ├── asistenti.xlsx
│   ├── alte_diplome.xlsx
│   └── event_detail.xlsx       (data + locație)
├── examples/                   Exemple cu nume fictive (urcă pe git)
├── templates/                  Template-urile PPTX
├── output/                     PPTX-urile generate (gitignored)
├── src/
│   ├── pptx_utils.py
│   ├── generate_planse.py
│   └── generate_diplome.py
├── run.py                      Meniu interactiv
├── finalize.py                 Commit + push pe GitHub
├── requirements.txt
└── README.md
```

---

## Licență

MIT — folosește, modifică, distribuie cum vrei.

---

*Dezvoltat de Samy Balasa pentru* [Din grijă pentru tine](https://dingrijapentrutine.ro/) *— Biserica Adventistă de Ziua a Șaptea din România.*
