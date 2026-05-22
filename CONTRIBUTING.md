# Cum contribui la dgpt-scripts

Mulțumim că vrei să ajuți! Acest ghid explică pașii simpli pentru a propune modificări.

---

## Ce poți propune

- **Corecții de bug-uri** — ceva nu merge sau dă rezultat greșit
- **Funcționalități noi** — un tip nou de diplomă, o opțiune nouă în meniu, suport pentru altă limbă
- **Îmbunătățiri de documentație** — README, exemple, comentarii în cod
- **Cod mai curat / refactor** — păstrând comportamentul existent

Înainte de a începe o modificare mare (peste 50 linii), te rugăm să deschizi întâi un **Issue** ca să discutăm abordarea.

---

## Workflow (fork → PR)

### 1. Fork

Pe pagina repo-ului [AdventTools/dgpt-scripts](https://github.com/AdventTools/dgpt-scripts), apasă butonul **Fork** (sus-dreapta). Vei avea o copie pe contul tău: `utilizatorul-tau/dgpt-scripts`.

### 2. Clone & branch

```bash
git clone https://github.com/utilizatorul-tau/dgpt-scripts.git
cd dgpt-scripts
git checkout -b descrie-modificarea-ta
```

Numește branch-ul descriptiv: `fix-encoding-asistenti`, `feat-export-pdf`, `docs-readme-windows`.

### 3. Modifică și testează

- Instalează dependențele: `pip install -r requirements.txt`
- Fă modificările
- Rulează `python run.py` și verifică că funcționează cu exemplele din `examples/`
- Dacă schimbi format de date sau API, actualizează `README.md`

### 4. Commit & push

```bash
git add .
git commit -m "scurt: descriere modificare"
git push origin descrie-modificarea-ta
```

### 5. Pull Request

Pe pagina fork-ului tău apare butonul **Compare & pull request**. Apasă-l, completează formularul (apare automat) și trimite.

**Bifează "Allow edits from maintainers"** — asta îmi permite să fac mici corecții direct pe branch-ul tău dacă e cazul, fără să te rog tu să le faci.

---

## Ce se întâmplă după

Eu (maintainer-ul) verific PR-ul tău. Posibile rezultate:

- **Acceptare integrală** → merge în `main`, mulțumesc!
- **Cer modificări** → comentez pe linii, tu modifici, dai push pe același branch (PR se actualizează automat)
- **Acceptare parțială** → folosesc cherry-pick pe commit-urile bune, sau te rog să divizezi PR-ul
- **Refuz** → cu explicații. Nu te supăra, nu e personal. Uneori scope-ul proiectului nu se potrivește cu ideea.

---

## Reguli de cod

- Python 3.10+
- Stil: nimic special, dar respectă convențiile fișierului unde lucrezi
- Comentarii și mesaje `print()` fără diacritice (convenție istorică)
- Documentația și README în română (sau bilingv ro/en)
- **NU urca pe git fișiere cu nume reale** (`data/`, `temp/` sunt în `.gitignore` — verifică `git status` înainte de commit)

---

## Întrebări?

Deschide un Issue sau scrie pe [discuții](https://github.com/AdventTools/dgpt-scripts/discussions) (dacă sunt activate). Răspund când pot.

Mulțumesc!
