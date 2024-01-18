from django.conf import settings


from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Spacer
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.tables import Table, TableStyle, colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from pypdf import PdfReader, PdfWriter


LIST_STYLE_DEFAULT = TableStyle(
    [
        ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black),
        ('ALIGN', (1,0), (-1,-1), 'RIGHT'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        # ('FONTNAME', (2,-1), (-1,-1), 'Courier-Bold'),
    ]
)

LIST_STYLE_FOOTER = TableStyle(
    [
        ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black),
        ('ALIGN', (1,0), (-1,-1), 'RIGHT'),
        ('FONTSIZE', (0,0), (-1,-2), 8),
        ('LINEABOVE', (0,-1), (-1,-1), 0.25, colors.gray),
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


def create_page(title, stakeholder_name, rows, style=LIST_STYLE_DEFAULT, page=None, page_size=None):
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
    if page and page_size:
        p = Paragraph(f"{page} / {page_size}", STYLE)
        elements.append(p)
    elements.append(Spacer(1, 40))

    table = Table(rows, colWidths=[2.5*inch,1.2*inch,1.3*inch,1.3*inch,1.2*inch])
    table.setStyle(style)
    elements.append(table)

    c.build(elements)

    buffer.seek(0)

    return PdfReader(buffer)

def draw(stakeholder_name, title, header, footer, rows):
    from io import BytesIO, StringIO

    tmp = BytesIO()
    output = PdfWriter()
    page_size = 25
    pages = int(len(rows) / page_size)

    for index in range(0, pages + 1):
        slice_start = index * page_size
        slice_end = (index + 1) * page_size
        table_rows = [header] + rows[slice_start:slice_end]
        if index == pages:
            table_rows.append(footer)

        new_pdf = create_page(
            title,
            stakeholder_name,
            table_rows,
            style=LIST_STYLE_FOOTER if index == pages else LIST_STYLE_DEFAULT,
            page=index+1,
            page_size=pages+1
        )
        existing_pdf = PdfReader(open(settings.BASE_DIR / "dashboard/static/documents/Papel-timbrado-Produto-Marginal.pdf", "rb"))
        page = existing_pdf.pages[0]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)

    output.write(tmp)

    tmp.seek(0)
    return tmp
        