"""
Helpers comuni pentru generate_planse.py si generate_diplome.py.

Continut:
- masurare latime text (auto-fit font)
- clonare slide (cu remapare rel-uri pentru imagini)
- constante namespace OOXML
"""
import copy
import os
from pathlib import Path

from lxml import etree

# ─────────────────────────────────────────────────────────────────
# CAI PROIECT (relative la fisier, nu la CWD)
# ─────────────────────────────────────────────────────────────────
ROOT          = Path(__file__).resolve().parent.parent
DATA          = ROOT / 'data'
TEMPLATES_DIR = ROOT / 'templates'
OUTPUT_DIR    = ROOT / 'output'

# ─────────────────────────────────────────────────────────────────
# NAMESPACE OOXML
# ─────────────────────────────────────────────────────────────────
NS_A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS_R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NSMAP = {'a': NS_A, 'p': NS_P, 'r': NS_R}

# ─────────────────────────────────────────────────────────────────
# MASURARE TEXT (pentru auto-fit font)
# ─────────────────────────────────────────────────────────────────
try:
    from PIL import ImageFont as _PIL_Font
    _PIL_OK = True
except ImportError:
    _PIL_OK = False


def find_font(candidates):
    """Returneaza prima cale existenta dintr-o lista de candidati, sau None."""
    for p in candidates:
        if os.path.isfile(p):
            return p
    return None


IMPACT_PATH = find_font([
    '/System/Library/Fonts/Supplemental/Impact.ttf',
    '/Library/Fonts/Impact.ttf',
    os.path.expanduser('~/Library/Fonts/Impact.ttf'),
    r'C:\Windows\Fonts\Impact.ttf',
])

CALIBRI_PATH = find_font([
    '/Library/Fonts/Microsoft/Calibri.ttf',
    os.path.expanduser('~/Library/Fonts/Calibri.ttf'),
    '/Library/Fonts/Calibri.ttf',
    r'C:\Windows\Fonts\Calibri.ttf',
    # fallback aproximativ:
    '/Library/Fonts/Arial.ttf',
    '/System/Library/Fonts/Helvetica.ttc',
])


def text_width_pt(text: str, size_pt: float, font_path: str, fallback_ratio: float) -> float:
    """
    Latimea textului in puncte la dimensiunea size_pt.
    Foloseste Pillow daca e disponibil; altfel aproximeaza cu fallback_ratio * size_pt per caracter.
    """
    if _PIL_OK and font_path:
        try:
            REF = 200
            font = _PIL_Font.truetype(font_path, REF)
            bbox = font.getbbox(text)
            w_ref = bbox[2] - bbox[0]
            if w_ref > 0:
                return w_ref * size_pt / REF
        except Exception:
            pass
    return len(text) * fallback_ratio * size_pt


def auto_font_pt(text: str, max_pt: int, min_pt: int, box_w_pt: float,
                 font_path: str, fallback_ratio: float) -> int:
    """Cea mai mare dimensiune (pt intregi) la care textul incape intr-o latime data."""
    if not text.strip():
        return max_pt
    pt = max_pt
    while pt > min_pt:
        if text_width_pt(text, pt, font_path, fallback_ratio) <= box_w_pt:
            break
        pt -= 1
    return max(pt, min_pt)


# ─────────────────────────────────────────────────────────────────
# CLONARE SLIDE (cu remapare rel-uri)
# ─────────────────────────────────────────────────────────────────

def clone_slide(prs, template_slide):
    """
    Adauga un slide nou clonat din template_slide. Remapeaza rel-urile
    (imagini, hyperlink-uri) ca sa nu se rupa referintele in XML.
    """
    layout    = template_slide.slide_layout
    new_slide = prs.slides.add_slide(layout)

    # Sterge shape-urile default
    for shape in list(new_slide.shapes):
        shape._element.getparent().remove(shape._element)

    # Copiaza rel-urile (mai putin layout-ul, care exista deja)
    rid_map = {}
    for rel in template_slide.part.rels.values():
        if 'notesSlide' in rel.reltype or 'slideLayout' in rel.reltype:
            continue
        if rel.is_external:
            new_rid = new_slide.part.rels.get_or_add_ext_rel(rel.reltype, rel.target_ref)
        else:
            new_rid = new_slide.part.rels._add_relationship(rel.reltype, rel.target_part)
        rid_map[rel.rId] = new_rid

    # Copiaza shape-urile si remapeaza rId-urile
    for shape in template_slide.shapes:
        new_el = copy.deepcopy(shape._element)
        for el in new_el.iter():
            for attr_name, attr_val in list(el.attrib.items()):
                if attr_name.startswith(f'{{{NS_R}}}') and attr_val in rid_map:
                    el.set(attr_name, rid_map[attr_val])
        new_slide.shapes._spTree.append(new_el)

    return new_slide


# ─────────────────────────────────────────────────────────────────
# XML HELPERS
# ─────────────────────────────────────────────────────────────────

def clean_rpr(rpr, sz_hundredths: int):
    """Cloneaza un <a:rPr> curat (fara err/dirty) cu dimensiunea sz data."""
    new_rpr = copy.deepcopy(rpr)
    new_rpr.set('sz', str(sz_hundredths))
    for attr in ('err', 'dirty'):
        if attr in new_rpr.attrib:
            del new_rpr.attrib[attr]
    return new_rpr


def set_paragraph_single_run(para, text: str, sz_hundredths: int = None):
    """
    Inlocuieste continutul paragrafului cu un singur run continand `text`.
    Pastreaza formatarea din primul run existent. Daca sz_hundredths e dat,
    setam dimensiunea (in sutimi de punct).
    """
    existing_runs = para.findall(f'{{{NS_A}}}r')
    if not existing_runs:
        return

    ref_rpr = existing_runs[0].find(f'{{{NS_A}}}rPr')

    new_r = etree.SubElement(para, f'{{{NS_A}}}r')
    if ref_rpr is not None:
        new_rpr = copy.deepcopy(ref_rpr)
        if sz_hundredths is not None:
            new_rpr.set('sz', str(sz_hundredths))
        for attr in ('err', 'dirty'):
            if attr in new_rpr.attrib:
                del new_rpr.attrib[attr]
        new_r.insert(0, new_rpr)
    t_el = etree.SubElement(new_r, f'{{{NS_A}}}t')
    t_el.text = text
    para.remove(new_r)

    # Sterge tot ce era inainte (run-uri si line-breaks)
    for r in list(para.findall(f'{{{NS_A}}}r')):
        para.remove(r)
    for br in list(para.findall(f'{{{NS_A}}}br')):
        para.remove(br)

    # Insereaza noul run inainte de endParaRPr daca exista
    end_rpr = para.find(f'{{{NS_A}}}endParaRPr')
    if end_rpr is not None:
        idx = list(para).index(end_rpr)
        para.insert(idx, new_r)
        if sz_hundredths is not None:
            end_rpr.set('sz', str(sz_hundredths))
        for attr in ('err', 'dirty'):
            if attr in end_rpr.attrib:
                del end_rpr.attrib[attr]
    else:
        para.append(new_r)
