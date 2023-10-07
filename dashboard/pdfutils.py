from django.conf import settings


from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Spacer
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.tables import Table, TableStyle, colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from pypdf import PdfReader, PdfWriter


LIST_STYLE = TableStyle(
    [
        ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
        ('ALIGN', (2,1), (-1,-1), 'RIGHT'),
        ('FONTNAME', (2,-1), (-1,-1), 'Courier-Bold'),
    ]
)

DEFAULT_STYLE = getSampleStyleSheet()
STYLE = ParagraphStyle(
    "title",
    fontSize=14,
    parent=DEFAULT_STYLE["Heading2"],
    alignment=1
)
STYLE2 = ParagraphStyle(
    "name",
    fontSize=12,
    alignment=1
)


def draw(stakeholder_name, title, rows):
    from io import BytesIO, StringIO

    width, height = A4

    buffer = BytesIO()
    elements = []

    c = SimpleDocTemplate(
        buffer, pagesize=A4
    )
    
    p = Paragraph(title, STYLE)
    elements.append(p)
    p = Paragraph(stakeholder_name, STYLE2)
    elements.append(p)
    elements.append(Spacer(1, 50))

    table = Table(rows)
    table.setStyle(LIST_STYLE)
    elements.append(table)

    c.build(elements)

    buffer.seek(0)

    new_pdf = PdfReader(buffer)
    existing_pdf = PdfReader(open(settings.BASE_DIR / "dashboard/static/documents/Papel-timbrado-Produto-Marginal.pdf", "rb"))

    tmp = BytesIO()
    output = PdfWriter()
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])

    output.add_page(page)

    output.write(tmp)

    tmp.seek(0)
    return tmp
    