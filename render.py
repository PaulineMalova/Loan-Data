from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template


class Render:
    @staticmethod
    def render(html):
        response = BytesIO
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
        if not pdf.err:
            return HttpResponse(
                response.getvalue(), content_type="application/pdf"
            )
        else:
            return HttpResponse("Error rendering PDF", status=400)
