from pathlib import Path
from datetime import date

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


COMPETENCES = [
    ("C1", "Recenser et identifier les ressources numériques"),
    ("C2", "Exploiter des référentiels, normes et standards adoptés par le prestataire informatique"),
    ("C3", "Mettre en place et vérifier les niveaux d'habilitation associés à un service"),
    ("C4", "Vérifier les conditions de la continuité d'un service informatique"),
    ("C5", "Gérer des sauvegardes"),
    ("C6", "Vérifier le respect des règles d'utilisation des ressources numériques"),
    ("C7", "Collecter, suivre et orienter des demandes"),
    ("C8", "Traiter des demandes concernant les services réseau, système et applicatif"),
    ("C9", "Traiter des demandes concernant les applications"),
    (
        "C10",
        "Participer à la valorisation de l'image de l'organisation sur les médias numériques "
        "en tenant compte du cadre juridique et des enjeux économiques",
    ),
    ("C11", "Référencer les services en ligne de l'organisation et mesurer leur visibilité"),
    ("C12", "Participer à l'évolution d'un site Web exploitant les données de l'organisation"),
    ("C13", "Analyser les objectifs et les modalités d'organisation d'un projet"),
    ("C14", "Planifier les activités"),
    ("C15", "Évaluer les indicateurs de suivi d'un projet et analyser les écarts"),
    ("C16", "Réaliser les tests d'intégration et d'acceptation d'un service"),
    ("C17", "Déployer un service"),
    ("C18", "Accompagner les utilisateurs dans la mise en place d'un service"),
]


def sanitize_filename(value: str) -> str:
    safe = value.replace("/", "-").replace("\\", "-").replace(":", " -")
    safe = safe.replace("’", "'").replace('"', "")
    return safe


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="DocTitle",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#0A2442"),
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="DocSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#40566E"),
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionTitle",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=colors.HexColor("#113E67"),
            spaceBefore=10,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyTextCustom",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#1F2A36"),
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Meta",
            parent=styles["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=9.5,
            leading=12,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#4F5F70"),
            spaceAfter=4,
        )
    )
    return styles


def bullet_list(items, styles):
    flow_items = [
        ListItem(Paragraph(item, styles["BodyTextCustom"]), leftIndent=8) for item in items
    ]
    return ListFlowable(flow_items, bulletType="bullet", start="circle", leftIndent=14)


def add_header(story, styles, code, label):
    story.append(Paragraph(f"{code} - {label}", styles["DocTitle"]))
    story.append(
        Paragraph(
            "BTS SIO - Dossier de compétences (format portfolio professionnel)",
            styles["DocSubtitle"],
        )
    )
    story.append(Paragraph(f"Date : {date.today().strftime('%d/%m/%Y')}", styles["Meta"]))
    story.append(Spacer(1, 0.2 * cm))


def add_reference_block(story, styles):
    story.append(Paragraph("Documentation officielle", styles["SectionTitle"]))
    refs = [
        "ANSSI - Bonnes pratiques et guides SSI : https://www.ssi.gouv.fr/",
        "CNIL - Référentiels et conformité : https://www.cnil.fr/",
        "ITIL / ISO / standards de services numériques (selon le contexte)",
    ]
    story.append(bullet_list(refs, styles))


def add_context_block(story, styles, code, label):
    story.append(Paragraph("Présentation", styles["SectionTitle"]))
    story.append(
        Paragraph(
            "Dans le cadre des activités de professionnalisation du BTS SIO, cette fiche documente "
            f"la compétence <b>{code}</b> : <i>{label}</i>. La démarche présentée est pensée pour "
            "un environnement d'entreprise (PME/collectivité) avec une approche orientée qualité "
            "de service, sécurité, traçabilité et amélioration continue.",
            styles["BodyTextCustom"],
        )
    )


def add_steps_block(story, styles, code):
    story.append(Paragraph("Étapes de mise en œuvre", styles["SectionTitle"]))
    steps = [
        "1. Analyse du besoin et cadrage du périmètre technique / organisationnel.",
        "2. Collecte des informations, inventaire et qualification des éléments concernés.",
        "3. Mise en œuvre opérationnelle sur les outils et procédures en vigueur.",
        "4. Contrôles, validation avec les parties prenantes et traçabilité des actions.",
        "5. Restitution (compte-rendu, documentation) et pistes d'amélioration.",
    ]
    story.append(bullet_list(steps, styles))

    table_data = [
        ["Phase", "Livrable attendu", "Indicateur de validation"],
        ["Cadrage", "Périmètre défini", "Validation du responsable / tuteur"],
        ["Exécution", "Actions réalisées", "Preuves (tickets, captures, exports)"],
        ["Contrôle", "Vérifications", "Conformité aux exigences"],
        ["Clôture", "Compte-rendu", "Partage / archivage effectué"],
    ]
    tbl = Table(table_data, colWidths=[4.2 * cm, 6.4 * cm, 6.4 * cm])
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#113E67")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9DB2C7")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F4F8FC")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(Spacer(1, 0.2 * cm))
    story.append(tbl)
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(f"Note contexte : ce modèle est applicable à la compétence {code}.", styles["Meta"]))


def add_tools_and_result(story, styles):
    story.append(Paragraph("Outils utilisés", styles["SectionTitle"]))
    tools = [
        "Suite bureautique (Word/Excel/PowerPoint) pour la documentation et la traçabilité.",
        "Outils d'administration système/réseau selon l'environnement (AD, scripts, supervision, ticketing).",
        "Référentiels de sécurité et de qualité de service (ANSSI, CNIL, standards internes).",
    ]
    story.append(bullet_list(tools, styles))

    story.append(Paragraph("Résultat attendu", styles["SectionTitle"]))
    story.append(
        Paragraph(
            "La compétence est considérée maîtrisée lorsque l'action est menée de bout en bout : "
            "besoin compris, exécution structurée, conformité vérifiée, livrables produits et "
            "capitalisation réalisée pour l'équipe.",
            styles["BodyTextCustom"],
        )
    )


def build_pdf(output_path: Path, code: str, label: str, styles):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=1.8 * cm,
        leftMargin=1.8 * cm,
        topMargin=1.6 * cm,
        bottomMargin=1.6 * cm,
        title=f"{code} - {label}",
        author="Nathan GEZAHEGN",
    )
    story = []
    add_header(story, styles, code, label)
    add_reference_block(story, styles)
    add_context_block(story, styles, code, label)
    add_steps_block(story, styles, code)
    story.append(PageBreak())
    add_tools_and_result(story, styles)
    doc.build(story)


def main():
    project_root = Path(__file__).resolve().parent
    out_dir = project_root / "assets" / "competences-pdf"
    styles = build_styles()

    for code, label in COMPETENCES:
        filename = sanitize_filename(f"{code} - {label}.pdf")
        build_pdf(out_dir / filename, code, label, styles)

    print(f"{len(COMPETENCES)} PDF générés dans : {out_dir}")


if __name__ == "__main__":
    main()
