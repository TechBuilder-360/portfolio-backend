from django.conf import settings
from django.template.response import TemplateResponse
from xhtml2pdf import pisa
import os
from io import BytesIO, StringIO
from PyPDF2 import PdfFileReader, PdfFileWriter
import uuid


def resolve_links(url, rel):
    """
    Used by xhtml2pdf to resolve links to resources.

    Links are first checked against STATIC_ROOT; if they fail to resolve,
    we assume they're relative to MEDIA_ROOT.
    """
    url = url.replace('../', settings.STATIC_URL) if url.startswith('../') else url

    # First, try to resolve resources to STATIC_ROOT:
    url = url.replace(settings.STATIC_URL, 'portfolio/static/')
    path = os.path.join(settings.PROJECT_BASE, *url.split('/'))

    if not os.path.exists(path):
        # This is probably some user-uploaded media, so use MEDIA_ROOT:
        url = url.replace(settings.MEDIA_URL, '')
        path = os.path.join(settings.MEDIA_ROOT, *url.split('/'))

    return path


def render_pdf(template, context, pwd=None):
    """
    Generates a PDF from the supplied template and context data.

    Optionally, encrypts the generated PDF file, and protects it with
    the password specified by `pwd`.
    """

    # from organization.apps import get_company_config
    # context['company_logo'] = get_company_config('logo')
    # context['company_name'] = get_company_config('name', 'Add Company Name in Configuration')

    outfile = BytesIO()
    pdf = pisa.CreatePDF(template.render(context), outfile, link_callback=resolve_links)

    if pdf.err:
        outfile = StringIO('Error generating PDF:<br />\n<pre>%s</pre>' % pdf.err)
    elif pwd:
        # If `pwd` was specified, use it to encrypt the PDF:
        wr, rdr = PdfFileWriter(), PdfFileReader(outfile)
        for page in rdr.pages:
            wr.addPage(page)
        wr.encrypt(pwd, use_128bit=True)
        outfile = StringIO()
        wr.write(outfile)
    return outfile.getvalue()


class PdfResponse(TemplateResponse):
    """Generates a PDF from the supplied template."""

    def __init__(self, request, template, context=None, filename=None, status=None, current_app=None, inline=False):
        super(PdfResponse, self).__init__(request, template, context, content_type='application/pdf',
                                          status=status)

        filename = uuid.uuid4().hex if not filename else filename
        filename = ('%s.pdf' % filename) if not filename.endswith('.pdf') else filename
        if not inline:
            self['Content-Disposition'] = 'attachment; filename=%s' % filename

    @property
    def rendered_content(self):
        """Renders the template and context to generate the PDF."""
        return render_pdf(self.resolve_template(self.template_name),
                          self.resolve_context(self.context_data))
