# importing the necessary libraries
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import candidate, education, employment

# defining the function to convert an HTML file to a PDF file


def html_to_pdf(template_src, context):
    template = get_template(template_src)
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
