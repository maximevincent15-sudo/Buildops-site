#!/usr/bin/env python3
"""
Génère les 6 pages « par type d'équipement » du site (une recherche Google
= une page) : extincteurs, RIA, BAES, désenfumage, portes coupe-feu,
colonnes sèches.

Les listes de contrôle, opérations, caractéristiques et observations
reprennent celles de l'application (family_templates, operations.ts,
identification.ts), reformulées et raccourcies.

Usage : python3 scripts/generate-equipment-pages.py   (depuis la racine du site)
Règles de formulation : jamais « conforme / certifié / agréé / au format »
APSAD ou NF ; « s'appuie sur la règle APSAD R4 » est autorisé.
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://firovia.fr"
LASTMOD = "2026-11-10"


def fr(text: str) -> str:
    """Texte visible : échappé, espaces insécables avant : ; ? ! et dans « »."""
    t = html.escape(text, quote=False)
    t = re.sub(r" ([:;?!])", r"&nbsp;\1", t)
    t = t.replace("« ", "«&nbsp;").replace(" »", "&nbsp;»")
    # Repères (EXT-04, CS-01…) jamais coupés en fin de ligne
    t = re.sub(r"\b([A-Z]{2,4}-\d{2})\b", r'<span style="white-space:nowrap">\1</span>', t)
    return t


FAMILIES = [
    {
        "slug": "logiciel-verification-extincteurs",
        "tag": "Extincteurs",
        "nav": "Extincteurs",
        "h1": ("Logiciel de vérification", "des extincteurs"),
        "title": "Logiciel de vérification d'extincteurs — Firovia",
        "desc": "Vérifiez vos extincteurs sur téléphone : scan de l'étiquette, liste de contrôle, rapport signé et registre envoyés au client. Dès 49 € HT par technicien.",
        "intro": "Vos techniciens font la vérification sur leur téléphone, extincteur par extincteur. À la fin de la visite, le client signe, puis le rapport et le registre partent tout seuls. Plus rien à ressaisir le soir au bureau.",
        "noun": "extincteur", "nouns": "extincteurs", "le": "l'extincteur", "chaque": "chaque extincteur",
        "ref": "La liste de contrôle s'appuie sur la règle APSAD R4.",
        "checklist": [
            "Emplacement, signalisation et accès dégagé",
            "Fixation murale et support en bon état",
            "Plombage intact et goupille présente",
            "Manomètre dans la zone verte",
            "Pesée conforme",
            "Tuyau, diffuseur et gâchette en bon état",
            "Étiquette de vérification apposée",
        ],
        "ops": ["Vérification", "Recharge", "Maintenance additionnelle", "Remplacement"],
        "obs": ["Recharge à prévoir", "Plombage refait", "Goupille remplacée", "Manomètre hors zone verte"],
        "attrs": "l'agent extincteur (eau pulvérisée, poudre ABC, CO2, mousse…), la capacité (6 L, 9 kg, 2 kg…) et le type de pression (permanente ou auxiliaire)",
        "extra": ("Année de réforme", "Firovia affiche l'année de réforme de chaque appareil : 20 ans après la mise en service pour les extincteurs à eau et à poudre. Ceux qui l'ont atteinte apparaissent en rouge dans l'inventaire, pour préparer le devis de remplacement."),
        "mock": {"rep": "EXT-04", "fam": "Extincteurs", "zone": "Accueil", "loc": "Hall, près des ascenseurs", "meta": "Eau pulvérisée + additif 6 L · Sicli · 2019"},
        "faq_specific": ("Firovia calcule-t-il l'année de réforme des extincteurs ?", "Oui. À partir de l'année de mise en service, Firovia affiche l'année de réforme : 20 ans pour les extincteurs à eau et à poudre (pas de durée fixée pour le CO2). Les appareils concernés ressortent en rouge dans l'inventaire."),
        "apsad": "R4",
        "blog": ("/blog/qr-code-extincteur-etiquette-maintenance", "le guide des étiquettes QR code sur les extincteurs"),
    },
    {
        "slug": "logiciel-verification-ria",
        "tag": "RIA",
        "nav": "RIA",
        "h1": ("Logiciel de vérification", "des RIA"),
        "title": "Logiciel de vérification des RIA — Firovia",
        "desc": "Vérification des RIA sur téléphone : liste de contrôle, essai de mise en eau, résultat par poste, rapport signé et registre envoyés au client.",
        "intro": "Poste par poste, le technicien coche la liste de contrôle du robinet d'incendie armé sur son téléphone, note l'essai de mise en eau et ajoute une photo si besoin. Le rapport signé part au client à la fin de la visite.",
        "noun": "RIA", "nouns": "RIA", "le": "le RIA", "chaque": "chaque RIA",
        "ref": "La liste de contrôle s'appuie sur la règle APSAD R5.",
        "checklist": [
            "Signalisation visible et accès dégagé",
            "Coffret ou niche en bon état",
            "Vanne d'arrêt ouverte et opérante",
            "Dévidoir qui tourne librement",
            "Tuyau sans coupure ni pliure",
            "Lance : jet plein, jet diffusé et arrêt",
            "Essai de mise en eau, puis purge",
        ],
        "ops": ["Vérification", "Réparation", "Remplacement"],
        "obs": ["Pression insuffisante", "Fuite au raccord", "Joint remplacé", "Tuyau à remplacer"],
        "attrs": "le diamètre (DN 19, DN 25, DN 33), la longueur du tuyau et le type de pose (fixe, pivotant, en armoire)",
        "extra": ("RIA et extincteurs dans la même visite", "Sur un site, les RIA et les extincteurs se contrôlent pendant la même visite, chacun avec sa liste de contrôle. Le rapport les présente type par type."),
        "mock": {"rep": "RIA-02", "fam": "RIA", "zone": "Bâtiment B", "loc": "Couloir RDC, près de l'escalier", "meta": "DN 25 · 30 m · Pivotant"},
        "faq_specific": ("Peut-on contrôler les RIA et les extincteurs dans la même visite ?", "Oui. Une visite peut couvrir plusieurs types d'équipements. Chaque appareil a sa propre liste de contrôle, et le rapport les regroupe par type."),
        "apsad": "R5",
        "blog": None,
    },
    {
        "slug": "logiciel-maintenance-baes",
        "tag": "BAES",
        "nav": "BAES",
        "h1": ("Logiciel de maintenance", "des BAES"),
        "title": "Logiciel de maintenance des BAES — Firovia",
        "desc": "Maintenance des BAES sur téléphone : essai, autonomie, pictogramme, batterie à changer. Rapport signé et registre envoyés au client à la fin de la visite.",
        "intro": "Sur un site, il y a souvent des dizaines de blocs. Le technicien les retrouve par zone, note l'essai et l'autonomie, signale une batterie à changer, puis passe au suivant. Le rapport part signé à la fin de la visite.",
        "noun": "bloc", "nouns": "BAES", "le": "le bloc", "chaque": "chaque bloc",
        "ref": "La liste de contrôle est pensée pour la norme NF C 71-800.",
        "checklist": [
            "Voyant de présence secteur allumé",
            "Essai de fonctionnement (autotest SATI ou test manuel)",
            "Autonomie en cas de coupure secteur",
            "Pictogramme d'évacuation visible",
            "Diffuseur propre et en bon état",
            "Fixation solide",
        ],
        "ops": ["Vérification", "Remplacement batterie", "Remplacement"],
        "obs": ["Batterie à remplacer", "Test SATI échoué", "Pictogramme remplacé", "Diffuseur nettoyé"],
        "attrs": "le type (évacuation, ambiance, BAEH, bloc portatif), la technologie (standard, SATI, adressable) et le flux lumineux",
        "extra": ("Les gros parcs", "Sur un site de plusieurs centaines de blocs, le technicien filtre par zone ou par étage, cherche un repère ou un emplacement, et affiche seulement ce qui « reste à contrôler »."),
        "mock": {"rep": "BAES-12", "fam": "BAES", "zone": "Niveau 1", "loc": "Sortie escalier est", "meta": "Évacuation · SATI · 45 lm"},
        "faq_specific": ("Les BAES à autotest (SATI) sont-ils pris en compte ?", "Oui. La technologie de chaque bloc est notée dans sa fiche (standard, SATI, adressable), et la liste de contrôle prévoit l'essai par autotest ou par test manuel."),
        "apsad": None,
        "blog": None,
    },
    {
        "slug": "logiciel-maintenance-desenfumage",
        "tag": "Désenfumage",
        "nav": "Désenfumage",
        "h1": ("Logiciel de maintenance", "du désenfumage"),
        "title": "Logiciel de maintenance du désenfumage — Firovia",
        "desc": "Vérification des exutoires, ouvrants et volets de désenfumage sur téléphone, même sans réseau en toiture. Rapport signé et registre envoyés au client.",
        "intro": "En toiture ou dans une cage d'escalier, il n'y a souvent pas de réseau. Le technicien déclenche, vérifie l'ouverture et la fermeture, et note le résultat sur son téléphone. Tout est gardé dans l'appareil et part au retour du réseau.",
        "noun": "appareil", "nouns": "appareils de désenfumage", "le": "l'appareil", "chaque": "chaque exutoire",
        "ref": "La liste de contrôle s'appuie sur la règle APSAD R17.",
        "checklist": [
            "Ouverture de secours testée en réel",
            "Fermeture complète après l'essai",
            "Commande qui fonctionne (treuil, cartouche CO2, électrique)",
            "Course d'ouverture dégagée",
            "Amenées d'air dégagées",
            "Signalisation de la commande lisible",
        ],
        "ops": ["Vérification", "Remplacement cartouche", "Réparation", "Remplacement"],
        "obs": ["Vérin à remplacer", "Obstruction retirée", "Commande électrique en défaut", "Volet à recalibrer"],
        "attrs": "le type (exutoire en toiture, ouvrant de façade, volet ou clapet, ventilateur, commande ou treuil), la commande (manuelle, pneumatique CO2, électrique) et la surface utile",
        "extra": ("Canton par canton", "Les zones du site suivent votre découpage, par exemple un canton ou une travée. Le rapport range les appareils dans l'ordre de passage, zone après zone."),
        "mock": {"rep": "DSF-07", "fam": "Désenfumage", "zone": "Canton 2", "loc": "Entrepôt, côté quai", "meta": "Exutoire (toiture) · CO2 · 1,2 m²"},
        "faq_specific": ("Ça marche vraiment sans réseau, en toiture ?", "Oui. Les contrôles, les photos, « Tout conforme » et même la clôture du rapport se font sans réseau. Tout est gardé dans le téléphone et envoyé dès que le réseau revient."),
        "apsad": "R17",
        "blog": ("/blog/verification-desenfumage-annuelle", "ce que contrôle la vérification annuelle du désenfumage"),
    },
    {
        "slug": "logiciel-portes-coupe-feu",
        "tag": "Portes coupe-feu",
        "nav": "Portes coupe-feu",
        "h1": ("Logiciel de contrôle", "des portes coupe-feu"),
        "title": "Logiciel de contrôle des portes coupe-feu — Firovia",
        "desc": "Contrôle des portes coupe-feu sur téléphone : refermeture, ferme-porte, joints, retenue magnétique, degré coupe-feu par porte. Rapport signé envoyé au client.",
        "intro": "Chaque porte a sa fiche : degré coupe-feu, nombre de vantaux, type de fermeture. Le technicien vérifie la refermeture, le ferme-porte et les joints, règle ce qui doit l'être et le note. Le rapport part signé à la fin de la visite.",
        "noun": "porte", "nouns": "portes coupe-feu", "le": "la porte", "chaque": "chaque porte",
        "ref": "La liste de contrôle reprend les points de la vérification annuelle d'une porte coupe-feu.",
        "checklist": [
            "Refermeture complète et autonome",
            "Ferme-porte et vitesse de fermeture réglés",
            "Joints intumescents en place",
            "Retenue magnétique qui fonctionne",
            "Aucune cale qui maintient la porte ouverte",
            "Ouverture possible en poussant",
            "Signalisation présente",
        ],
        "ops": ["Vérification", "Réglage", "Réparation", "Remplacement"],
        "obs": ["Ferme-porte à régler", "Joints remplacés", "Cale retirée, client informé", "Retenue magnétique en défaut"],
        "attrs": "le degré coupe-feu (EI 30, EI 60, EI 90, EI 120, E 30), l'ouverture (battante, va-et-vient, coulissante, rideau), le nombre de vantaux et la fermeture (ferme-porte, ventouse, ressort, motorisée)",
        "extra": ("Une cale sous une porte ?", "Le technicien la signale comme anomalie, avec une photo. Elle apparaît dans le rapport, dans les points à traiter, et peut devenir un devis en un clic si une pièce est à changer."),
        "mock": {"rep": "PCF-03", "fam": "Portes coupe-feu", "zone": "Sous-sol", "loc": "Accès parking", "meta": "EI 60 · Battante · 2 vantaux"},
        "faq_specific": ("Le degré coupe-feu de chaque porte est-il noté ?", "Oui. La fiche de chaque porte garde son degré coupe-feu (EI 30, EI 60…), son type d'ouverture, son nombre de vantaux et son type de fermeture. Le technicien les retrouve à chaque visite."),
        "apsad": None,
        "blog": None,
    },
    {
        "slug": "logiciel-colonnes-seches",
        "tag": "Colonnes sèches",
        "nav": "Colonnes sèches",
        "h1": ("Logiciel de vérification", "des colonnes sèches"),
        "title": "Logiciel de vérification des colonnes sèches — Firovia",
        "desc": "Vérification des colonnes sèches sur téléphone : raccords, vannes de niveau, signalisation, essai de mise en charge. Rapport signé envoyé au client.",
        "intro": "Une colonne sèche, c'est un raccord en façade et une prise à chaque étage. Le technicien suit la colonne niveau par niveau, coche les points de contrôle et note l'essai. Le rapport part signé à la fin de la visite.",
        "noun": "colonne", "nouns": "colonnes sèches", "le": "la colonne", "chaque": "chaque colonne",
        "ref": "La liste de contrôle reprend les points de la vérification annuelle d'une colonne sèche.",
        "checklist": [
            "Accès depuis la voie des pompiers et signalisation",
            "Raccords de façade et bouchons en place",
            "Coffret d'alimentation bien fixé",
            "Prise accessible et signalée à chaque niveau",
            "Vannes de niveau qui s'ouvrent et se ferment",
            "Essai de mise en charge, puis vidange",
        ],
        "ops": ["Vérification", "Réparation"],
        "obs": ["Bouchon remplacé", "Raccord à changer", "Vanne à réviser", "Signalisation refaite"],
        "attrs": "le diamètre (DN 65 ou DN 100) et le nombre de prises, c'est-à-dire d'étages desservis",
        "extra": ("Avec les autres équipements", "Les colonnes sèches d'un immeuble se contrôlent dans la même visite que les extincteurs ou les BAES. Chaque colonne a son repère (CS-01, CS-02…) et sa zone."),
        "mock": {"rep": "CS-01", "fam": "Colonnes sèches", "zone": "Bâtiment A", "loc": "Façade rue, côté entrée", "meta": "DN 65 · 6 prises"},
        "faq_specific": ("Peut-on suivre plusieurs colonnes sur un même immeuble ?", "Oui. Chaque colonne a son repère et sa zone (bâtiment, cage d'escalier). Le rapport les liste une par une, avec le résultat de chacune."),
        "apsad": None,
        "blog": None,
    },
]


def faq_items(f):
    if f["apsad"]:
        q1 = ("Un logiciel peut-il être certifié APSAD ?",
              f"Non. Un logiciel n'est ni certifié ni agréé APSAD : ce sont votre entreprise et votre travail qui peuvent l'être. La liste de contrôle des {f['nouns']} s'appuie sur la règle APSAD {f['apsad']}, et vos registres sont prêts pour vos audits.")
    else:
        q1 = ("La liste de contrôle est-elle modifiable ?",
              f"Oui. Firovia propose une liste de contrôle pour les {f['nouns']}, et vous pouvez créer vos propres listes dans les paramètres, pour coller à vos contrats.")
    return [
        q1,
        f["faq_specific"],
        (f"Comment reprendre la liste des {f['nouns']} de mes clients ?",
         "Avec l'import Excel en libre-service, ou dans « Parc du site » : vous collez le tableau copié dans un ancien rapport (Word, PDF ou Excel) et les colonnes sont reconnues. La reprise faite par nos soins est sur devis."),
        ("Faut-il installer une application ?",
         "Non. Firovia s'ouvre dans le navigateur du téléphone (iPhone ou Android) et s'ajoute à l'écran d'accueil. Les contrôles s'enregistrent même sans réseau."),
    ]


CSS = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
:root{
  --bg:#F2F3F5;--bg2:#E6E8EC;--bg3:#D8DCE4;
  --ink:#1C2130;--ink2:#5A6070;--ink3:#9AA0AE;
  --acc:#3A5CA8;--acc2:#5578C8;--acc-lt:#E8EEF8;
  --wht:#F8F9FB;
  --brd:rgba(28,33,48,.10);--brd2:rgba(28,33,48,.18);
  --grn:#2E7D5E;--grn-lt:#D4EDE5;
  --org:#C45A1A;--org-lt:#F5E0D0;
  --r:10px;--rlg:18px;
}
html{scroll-behavior:smooth;}
html,body{font-family:'Inter',sans-serif;background:var(--bg);color:var(--ink);line-height:1.6;}
h1,h2,h3,h4{font-family:'Syne',sans-serif;letter-spacing:-.5px;}
a{text-decoration:none;color:inherit;cursor:pointer;}

#topnav{position:fixed;top:0;left:0;right:0;z-index:999;display:flex;align-items:center;justify-content:space-between;padding:.85rem 4%;background:rgba(242,243,245,.95);backdrop-filter:blur(14px);border-bottom:.5px solid var(--brd);}
.logo{display:flex;align-items:center;gap:9px;cursor:pointer;}
.logo-txt{font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:800;color:var(--ink);}
.logo-txt span{color:var(--acc);}
.nav-links{display:flex;gap:1.8rem;list-style:none;}
.nav-links a{font-size:.88rem;color:var(--ink2);font-weight:500;}
.nav-links a:hover{color:var(--ink);}
.nav-r{display:flex;gap:.6rem;align-items:center;}
.btn-sm{display:inline-block;white-space:nowrap;padding:.48rem 1.1rem;border-radius:100px;font-size:.85rem;font-weight:500;cursor:pointer;border:1px solid var(--brd2);background:transparent;color:var(--ink);transition:background .15s;}
.btn-sm:hover{background:var(--bg2);}
.btn-sm.acc{background:var(--acc);color:white;border-color:var(--acc);}
.btn-sm.acc:hover{background:var(--acc2);}

main{padding-top:80px;padding-bottom:80px;}
.container{max-width:1040px;margin:0 auto;padding:0 4%;}
.crumbs{font-size:.78rem;color:var(--ink3);padding-top:28px;}
.crumbs a{color:var(--ink2);}
.crumbs a:hover{color:var(--acc);}

.hero{padding:28px 0 56px;border-bottom:1px solid var(--brd);}
.hero-grid{display:grid;grid-template-columns:1.15fr .85fr;gap:48px;align-items:center;}
.hero-tag{display:inline-flex;align-items:center;gap:6px;font-size:.78rem;font-weight:600;color:var(--grn);background:var(--grn-lt);padding:6px 14px;border-radius:100px;margin-bottom:22px;letter-spacing:.4px;text-transform:uppercase;}
.hero-tag::before{content:"";display:inline-block;width:6px;height:6px;background:var(--grn);border-radius:50%;}
.hero h1{font-size:clamp(1.8rem,3.5vw,2.55rem);font-weight:800;line-height:1.12;margin-bottom:18px;}
.hero h1 span{color:var(--acc);}
.hero-sub{font-size:1.05rem;color:var(--ink2);max-width:560px;margin-bottom:26px;}
.hero-cta{display:flex;gap:10px;flex-wrap:wrap;align-items:center;}
.btn{display:inline-block;padding:.8rem 1.4rem;border-radius:100px;font-size:.95rem;font-weight:600;border:1px solid var(--brd2);transition:background .15s;}
.btn.acc{background:var(--acc);color:white;border-color:var(--acc);}
.btn.acc:hover{background:var(--acc2);}
.btn:hover{background:var(--bg2);}
.btn.acc:hover{background:var(--acc2);}
.hero-note{font-size:.8rem;color:var(--ink3);margin-top:12px;}

/* Maquette de la fenêtre de contrôle (données d'exemple) */
.phone{width:290px;margin:0 auto;border-radius:38px;background:#151B2B;padding:10px;box-shadow:0 30px 60px rgba(28,33,48,.18);}
.phone-screen{background:#FAFAFB;border-radius:30px;padding:18px 14px 16px;font-family:'Inter',sans-serif;}
.pm-head{display:flex;align-items:center;gap:8px;font-size:.82rem;font-weight:700;color:var(--ink);}
.pm-rep{background:var(--acc-lt);color:var(--acc);font-size:.72rem;font-weight:700;padding:2px 7px;border-radius:6px;}
.pm-x{margin-left:auto;color:var(--ink3);font-weight:400;font-size:1.1rem;line-height:1;}
.pm-loc{margin-top:10px;background:white;border:1px solid var(--brd);border-radius:10px;padding:8px 10px;font-size:.8rem;color:var(--ink);line-height:1.35;}
.pm-loc b{font-weight:700;}
.pm-meta{font-size:.7rem;color:var(--ink2);margin-top:4px;}
.pm-label{font-size:.62rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--ink3);margin:12px 0 6px;}
.pm-list{list-style:none;display:flex;flex-direction:column;gap:5px;}
.pm-list li{display:flex;align-items:center;gap:8px;font-size:.72rem;color:var(--ink);background:white;border:1px solid var(--brd);border-radius:8px;padding:6px 8px;line-height:1.3;}
.pm-list li span{margin-left:auto;font-size:.62rem;font-weight:700;padding:2px 7px;border-radius:100px;background:var(--grn-lt);color:var(--grn);white-space:nowrap;}
.pm-list li.todo span{background:var(--bg2);color:var(--ink2);}
.pm-chips{display:flex;flex-wrap:wrap;gap:5px;}
.pm-chips span{font-size:.66rem;font-weight:600;padding:4px 9px;border-radius:100px;border:1px solid var(--brd2);color:var(--ink2);background:white;}
.pm-chips span.on{background:var(--grn);border-color:var(--grn);color:white;}
.pm-chips.ops span.on{background:var(--acc);border-color:var(--acc);}
.pm-save{margin-top:14px;background:var(--acc);color:white;text-align:center;font-size:.78rem;font-weight:600;border-radius:100px;padding:9px;}
.pm-caption{text-align:center;font-size:.72rem;color:var(--ink3);margin-top:12px;}

.section{padding:52px 0;border-bottom:1px solid var(--brd);}
.section-num{display:inline-block;font-family:'Syne',sans-serif;font-size:.78rem;font-weight:700;color:var(--acc);letter-spacing:1.2px;margin-bottom:8px;text-transform:uppercase;}
.section h2{font-size:1.65rem;font-weight:800;margin-bottom:18px;line-height:1.2;max-width:720px;}
.section p{color:var(--ink2);margin-bottom:14px;font-size:.95rem;max-width:760px;}
.section p strong{color:var(--ink);font-weight:600;}
.section ul.dots{list-style:none;margin:14px 0;max-width:760px;}
.section ul.dots li{position:relative;padding-left:24px;color:var(--ink2);font-size:.92rem;margin-bottom:8px;}
.section ul.dots li::before{content:"";position:absolute;left:0;top:.55rem;width:8px;height:8px;background:var(--grn);border-radius:50%;}
.section ul.dots li strong{color:var(--ink);font-weight:600;}

.steps{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin-top:24px;}
.step{background:white;border:1px solid var(--brd);border-radius:var(--rlg);padding:22px 24px;}
.step-n{display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:50%;background:var(--acc-lt);color:var(--acc);font-family:'Inter',sans-serif;font-weight:700;font-size:.85rem;margin-bottom:10px;}
.step h3{font-family:'Inter',sans-serif;font-size:1rem;font-weight:700;letter-spacing:0;margin-bottom:8px;}
.step p{font-size:.88rem;margin-bottom:8px;}
.step ul{list-style:none;margin-top:6px;}
.step ul li{font-size:.85rem;color:var(--ink2);padding:5px 0 5px 22px;position:relative;border-top:1px solid var(--brd);}
.step ul li:first-child{border-top:none;}
.step ul li::before{content:"";position:absolute;left:2px;top:.75rem;width:9px;height:5px;border-left:2px solid var(--grn);border-bottom:2px solid var(--grn);transform:rotate(-45deg);}
.tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;}
.tags span{font-size:.75rem;font-weight:600;padding:4px 10px;border-radius:100px;background:var(--bg2);color:var(--ink2);}
.ref{font-size:.82rem;color:var(--ink3);margin-top:10px;}

.callout{background:white;border:1px solid var(--brd);border-left:4px solid var(--acc);border-radius:var(--r);padding:18px 22px;margin:22px 0 0;font-size:.92rem;color:var(--ink2);max-width:760px;}
.callout strong{color:var(--ink);}

.contact-box{background:var(--ink);color:white;border-radius:var(--rlg);padding:34px;}
.contact-box h2{color:white;font-size:1.45rem;margin-bottom:8px;}
.contact-box p{color:rgba(255,255,255,.75);margin-bottom:18px;max-width:none;}
.contact-box .links{display:flex;gap:18px;flex-wrap:wrap;margin-bottom:0;}
.contact-box a{color:white;font-weight:600;border-bottom:1px solid rgba(255,255,255,.4);}
.contact-box a:hover{border-bottom-color:white;}

.faq{max-width:780px;}
.faq details{background:white;border:1px solid var(--brd);border-radius:var(--r);padding:16px 20px;margin-bottom:10px;}
.faq summary{cursor:pointer;font-weight:600;font-size:.95rem;color:var(--ink);list-style:none;display:flex;justify-content:space-between;gap:12px;}
.faq summary::-webkit-details-marker{display:none;}
.faq summary::after{content:"+";color:var(--acc);font-weight:700;}
.faq details[open] summary::after{content:"−";}
.faq details p{margin:10px 0 0;font-size:.9rem;}

.others{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:18px;}
.others a{background:white;border:1px solid var(--brd);border-radius:var(--r);padding:14px 16px;font-size:.9rem;font-weight:600;color:var(--ink);transition:border-color .15s,transform .15s;}
.others a:hover{border-color:var(--acc);transform:translateY(-1px);}
.others a span{display:block;font-size:.78rem;font-weight:400;color:var(--ink2);margin-top:2px;}

footer{background:var(--ink);color:rgba(255,255,255,.6);padding:36px 4%;font-size:.82rem;}
footer .container{display:flex;justify-content:space-between;flex-wrap:wrap;gap:16px;}
footer a{color:rgba(255,255,255,.6);transition:color .15s;}
footer a:hover{color:white;}
.fnav{display:flex;gap:18px;flex-wrap:wrap;}
.fnav-eq{width:100%;display:flex;gap:18px;flex-wrap:wrap;padding-top:14px;border-top:1px solid rgba(255,255,255,.08);}

@media (max-width:860px){
  .nav-links{display:none;}
  .hero-grid{grid-template-columns:1fr;gap:36px;}
  .steps{grid-template-columns:1fr;}
  .others{grid-template-columns:1fr 1fr;}
  .section{padding:38px 0;}
  .contact-box{padding:26px 20px;}
}
@media (max-width:480px){
  .others{grid-template-columns:1fr;}
  .phone{width:268px;}
  .nav-r{gap:.4rem;}
  .nav-r .btn-sm{padding:.42rem .8rem;font-size:.8rem;}
  .section h2{font-size:1.35rem;}
  .hero h1{font-size:1.75rem;}
}
"""


def li(items, cls=""):
    return "".join(f"<li{cls}>{fr(i)}</li>" for i in items)


def mockup(f):
    m = f["mock"]
    items = f["checklist"][:5]
    on = ' class="on"'
    rows = "".join(
        "<li>" + fr(i) + "<span>OK</span></li>"
        for k, i in enumerate(items)
    )
    ops = "".join("<span" + (on if k == 0 else "") + ">" + fr(o) + "</span>" for k, o in enumerate(f["ops"]))
    return f"""<div class="phone" aria-hidden="true">
        <div class="phone-screen">
          <div class="pm-head"><span class="pm-rep">{fr(m['rep'])}</span>{fr(m['fam'])}<span class="pm-x">×</span></div>
          <div class="pm-loc"><b>{fr(m['zone'])}</b> · {fr(m['loc'])}<div class="pm-meta">{fr(m['meta'])}</div></div>
          <div class="pm-label">Liste de contrôle</div>
          <ul class="pm-list">{rows}</ul>
          <div class="pm-label">Verdict</div>
          <div class="pm-chips"><span class="on">Conforme</span><span>À surveiller</span><span>À réformer</span></div>
          <div class="pm-label">Opérations réalisées</div>
          <div class="pm-chips ops">{ops}</div>
          <div class="pm-save">Enregistrer et suivant</div>
        </div>
      </div>
      <p class="pm-caption">Fenêtre de contrôle d'un appareil (données d'exemple)</p>"""


def page(f):
    url = f"{SITE}/{f['slug']}"
    h1a, h1b = f["h1"]
    faqs = faq_items(f)
    others = [o for o in FAMILIES if o["slug"] != f["slug"]]

    ld = [
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "Firovia",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web, iOS, Android (navigateur)",
            "description": f["desc"],
            "url": url,
            "offers": {"@type": "Offer", "price": "49", "priceCurrency": "EUR",
                       "description": "Formule Essentiel, par technicien et par mois, HT (2 techniciens minimum)"},
            "publisher": {"@type": "Organization", "name": "Firovia", "url": f"{SITE}/"},
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Accueil", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": "Fonctionnalités", "item": f"{SITE}/fonctionnalites"},
                {"@type": "ListItem", "position": 3, "name": f["tag"], "item": url},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs
            ],
        },
    ]
    ld_html = "\n".join(
        f'<script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False, indent=2)}\n</script>' for x in ld
    )
    desc_attr = html.escape(f["desc"], quote=True)
    title_attr = html.escape(f["title"], quote=True)
    extra_t, extra_p = f["extra"]
    blog = f'<p>Pour aller plus loin&nbsp;: <a href="{f["blog"][0]}" style="color:var(--acc);font-weight:600">{fr(f["blog"][1])}</a>.</p>' if f["blog"] else ""
    faq_html = "".join(f"<details><summary>{fr(q)}</summary><p>{fr(a)}</p></details>" for q, a in faqs)
    others_html = "".join(
        f'<a href="/{o["slug"]}">{fr(o["nav"])}<span>{fr(o["h1"][0] + " " + o["h1"][1])}</span></a>' for o in others
    ) + '<a href="/fonctionnalites">Toutes les fonctionnalités<span>Planning, devis, factures, contrats…</span></a>'
    eq_footer = "".join(f'<a href="/{o["slug"]}">{fr(o["nav"])}</a>' for o in FAMILIES)

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<link rel="icon" type="image/svg+xml" href="/favicon.svg"/>
<title>{title_attr}</title>
<meta name="description" content="{desc_attr}"/>
<meta name="author" content="Firovia"/>
<link rel="canonical" href="{url}"/>

<meta property="og:type" content="website"/>
<meta property="og:site_name" content="Firovia"/>
<meta property="og:url" content="{url}"/>
<meta property="og:title" content="{title_attr}"/>
<meta property="og:description" content="{desc_attr}"/>
<meta property="og:image" content="{SITE}/og-image.png"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta property="og:locale" content="fr_FR"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{title_attr}"/>
<meta name="twitter:description" content="{desc_attr}"/>
<meta name="twitter:image" content="{SITE}/og-image.png"/>

{ld_html}

<link href="/fonts/fonts.css" rel="stylesheet"/>
<script defer src="/_vercel/insights/script.js"></script>
<script defer src="/_vercel/speed-insights/script.js"></script>
<style>{CSS}</style>
</head>
<body>

<nav id="topnav">
  <a class="logo" href="/"><div class="logo-txt"><span>Fir</span>ovia</div></a>
  <ul class="nav-links">
    <li><a href="/fonctionnalites">Fonctionnalités</a></li>
    <li><a href="/#pour-qui">Pour qui</a></li>
    <li><a href="/tarifs">Tarifs</a></li>
    <li><a href="/blog">Blog</a></li>
    <li><a href="/#faq">FAQ</a></li>
  </ul>
  <div class="nav-r">
    <a class="btn-sm" href="https://app.firovia.fr/auth">Connexion</a>
    <a class="btn-sm acc" href="/essai-gratuit">Essai gratuit</a>
  </div>
</nav>

<main>
  <div class="container crumbs"><a href="/">Accueil</a> › <a href="/fonctionnalites">Fonctionnalités</a> › {fr(f['tag'])}</div>

  <section class="hero">
    <div class="container hero-grid">
      <div>
        <div class="hero-tag">{fr(f['tag'])}</div>
        <h1>{fr(h1a)}<br><span>{fr(h1b)}</span></h1>
        <p class="hero-sub">{fr(f['intro'])}</p>
        <div class="hero-cta">
          <a class="btn acc" href="/essai-gratuit">Essai gratuit 14 jours</a>
          <a class="btn" href="/demo">Voir la démo (2 min)</a>
        </div>
        <p class="hero-note">{fr("Sans carte bancaire · Dès 49 € HT par technicien et par mois · Sans engagement")}</p>
      </div>
      <div>
      {mockup(f)}
      </div>
    </div>
  </section>

  <section class="section" id="terrain">
    <div class="container">
      <span class="section-num">01 · Sur place</span>
      <h2>{fr(f'Le contrôle se fait sur le téléphone, {f["chaque"]} à son tour')}</h2>
      <div class="steps">
        <div class="step">
          <div class="step-n">1</div>
          <h3>{fr("Retrouver " + f['le'])}</h3>
          <p>{fr(f"Le technicien scanne l'étiquette QR, ou tape le repère ({f['mock']['rep']}) ou l'emplacement. La fiche s'ouvre avec l'emplacement écrit en gros et la photo de repérage.")}</p>
        </div>
        <div class="step">
          <div class="step-n">2</div>
          <h3>Cocher la liste de contrôle</h3>
          <ul>{li(f['checklist'])}</ul>
          <p class="ref">{fr(f['ref'] + " Chaque point se coche « OK » ou « sans objet ».")}</p>
        </div>
        <div class="step">
          <div class="step-n">3</div>
          <h3>Donner le résultat</h3>
          <p>{fr("Conforme, à surveiller ou à réformer. Puis les opérations faites sur place :")}</p>
          <div class="tags">{''.join(f'<span>{fr(o)}</span>' for o in f['ops'])}</div>
          <p style="margin-top:10px">{fr("Une anomalie ? Le technicien note un résumé, l'action recommandée et une priorité.")}</p>
        </div>
        <div class="step">
          <div class="step-n">4</div>
          <h3>Photo et observation</h3>
          <p>{fr("Une photo jointe au contrôle, et une observation en un geste, par exemple :")}</p>
          <div class="tags">{''.join(f'<span>{fr(o)}</span>' for o in f['obs'])}</div>
        </div>
      </div>
      <div class="callout"><strong>Pas de réseau&nbsp;?</strong> {fr("Sous-sol, toiture, local technique : les contrôles et les photos sont gardés dans le téléphone et envoyés dès que le réseau revient.")}</div>
    </div>
  </section>

  <section class="section" id="parc">
    <div class="container">
      <span class="section-num">02 · Le parc du site</span>
      <h2>{fr(f"Une fiche pour {f['chaque']}, retrouvée à chaque visite")}</h2>
      <ul class="dots">
        <li><strong>{fr("Repère et emplacement")}</strong>{fr(f" : {f['mock']['rep']}, la zone (bâtiment, étage, canton…) et l'emplacement précis, avec une photo de repérage.")}</li>
        <li><strong>Caractéristiques</strong>{fr(f" : {f['attrs']}, la marque et l'année.")}</li>
        <li><strong>{fr(extra_t)}</strong>{fr(" : " + extra_p)}</li>
        <li><strong>{fr("Étiquettes QR")}</strong>{fr(" imprimées depuis Firovia sur planches autocollantes A4, avec des cases « Date de passage » à remplir au stylo, au nom de votre entreprise ou du client.")}</li>
        <li><strong>{fr("Reprise de votre parc")}</strong>{fr(" : import Excel en libre-service, ou « Parc du site », où vous collez le tableau d'un ancien rapport pour remplir les zones et les emplacements en une fois.")}</li>
      </ul>
      {blog}
    </div>
  </section>

  <section class="section" id="rapport">
    <div class="container">
      <span class="section-num">03 · Rapport et registre</span>
      <h2>{fr("Le rapport part signé à la fin de la visite")}</h2>
      <ul class="dots">
        <li><strong>{fr("Signature du client")}</strong>{fr(" sur l'écran du téléphone, à la fin de la visite.")}</li>
        <li><strong>{fr("Rapport PDF")}</strong>{fr(f" créé tout seul : le résultat de {f['chaque']}, les anomalies avec photos et les points à traiter.")}</li>
        <li><strong>{fr("Registre nominatif")}</strong>{fr(" découpé par type d'équipement, prêt pour vos audits.")}</li>
        <li><strong>{fr("Envoi par mail")}</strong>{fr(" au client depuis Firovia, sans repasser par le bureau.")}</li>
        <li><strong>{fr("Portail client et lien de partage du registre")}</strong>{fr(" : le responsable du site retrouve ses rapports en ligne.")}</li>
      </ul>
    </div>
  </section>

  <section class="section" id="apres">
    <div class="container">
      <span class="section-num">04 · Après la visite</span>
      <h2>{fr("Les anomalies et la visite suivante sont déjà prêtes")}</h2>
      <ul class="dots">
        <li><strong>{fr("Devis correctif en un clic")}</strong>{fr(" depuis le rapport, avec une ligne par anomalie.")}</li>
        <li><strong>{fr("Visite suivante planifiée automatiquement")}</strong>{fr(" à la clôture du rapport, sur le même site, avec les mêmes appareils.")}</li>
        <li><strong>{fr("Alertes")}</strong>{fr(" : visites qui approchent, sites sans visite prévue, contrats à renouveler.")}</li>
        <li><strong>{fr("Facture de la visite")}</strong>{fr(" préparée depuis le rapport finalisé.")}</li>
      </ul>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="contact-box">
        <h2>{fr(f"Essayez Firovia sur vos {f['nouns']}")}</h2>
        <p>{fr("14 jours d'essai gratuit, sans carte bancaire et sans engagement. 49 € HT par technicien et par mois, dès 98 € HT. Ce tarif vous reste garanti si vous démarrez avant le 31 mars 2027.")}</p>
        <p class="links">
          <a href="/essai-gratuit">Démarrer l'essai gratuit →</a>
          <a href="https://cal.com/firovia">Réserver une démo de 30 minutes →</a>
          <a href="/tarifs">Voir les tarifs →</a>
        </p>
      </div>
    </div>
  </section>

  <section class="section" id="faq">
    <div class="container">
      <span class="section-num">Questions fréquentes</span>
      <h2>{fr(f"Firovia et les {f['nouns']}")}</h2>
      <div class="faq">{faq_html}</div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <span class="section-num">Les autres équipements</span>
      <h2>Firovia suit tout le parc du site</h2>
      <div class="others">{others_html}</div>
    </div>
  </section>
</main>

<footer>
  <div class="container">
    <div>© 2026 Firovia · SIREN 106 429 749 · Logiciel de gestion maintenance sécurité incendie</div>
    <div class="fnav">
      <a href="/fonctionnalites">Fonctionnalités</a>
      <a href="/tarifs">Tarifs</a>
      <a href="/mentions-legales">Mentions légales</a>
      <a href="/cgu">CGU</a>
      <a href="/cgv">CGV</a>
      <a href="/confidentialite">Confidentialité</a>
      <a href="/securite">Sécurité</a>
      <a href="mailto:contact@firovia.fr">Contact</a>
    </div>
    <div class="fnav-eq">{eq_footer}</div>
  </div>
</footer>

<script src="/js/origine.js" defer></script>
</body>
</html>
"""


def main():
    for f in FAMILIES:
        path = os.path.join(ROOT, f["slug"] + ".html")
        with open(path, "w", encoding="utf-8") as out:
            out.write(page(f))
        print("écrit", os.path.relpath(path, ROOT))


if __name__ == "__main__":
    main()
