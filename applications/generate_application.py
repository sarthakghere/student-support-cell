from docxtpl import DocxTemplate
from django.conf import settings
import os
from docx2pdf import convert

def generate(application_data):
    # Paths
    template_path = os.path.join(settings.MEDIA_ROOT, 'document_templates/Application_Template.docx')
    output_dir = os.path.join(settings.MEDIA_ROOT, 'generated_documents')
    os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists

    # Extract details from application_data
    prn = application_data.get("prn")
    erp = application_data.get("erp")
    first_name = application_data.get("first_name")
    last_name = application_data.get("last_name")
    subject = application_data.get("subject")
    message = application_data.get("message")
    date = application_data.get("date")

    # Replacement data for the document
    context = {
        "prn": prn,
        "erp": erp,
        "first_name": first_name,
        "last_name": last_name,
        "subject": subject,
        "message": message,
        "date": date

    }

    # Generate DOCX
    template = DocxTemplate(template_path)
    docx_path = os.path.join(output_dir, f'Application_{prn}.docx')
    template.render(context)
    template.save(docx_path)

    return docx_path