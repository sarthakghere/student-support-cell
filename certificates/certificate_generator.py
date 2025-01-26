from docxtpl import DocxTemplate
import os
from django.conf import settings

def generate_bonafide_certificate(student_data, backlogs):
    template_path = os.path.join(settings.MEDIA_ROOT, 'document_templates/Bonafide_Template.docx')
    output_dir = os.path.join(settings.MEDIA_ROOT, 'generated_documents')
    os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists

    template = DocxTemplate(template_path)

    # Extract details from student_data
    prn = student_data.get("PRN")
    first_name = student_data.get("first_name")
    last_name = student_data.get("last_name")
    gender = student_data.get("gender").lower()
    fathers_name = student_data.get("fathers_name")
    course = student_data.get("course").upper()
    course_start = int(student_data.get("course_start"))
    course_end = int(student_data.get("course_end"))

    name = f"{first_name} {last_name}"
    batch = f"{course_start} - {course_end}"
    years = course_end - course_start
    salutation = "Mr." if gender == 'male' else "Ms."
    relation = "S/O" if gender == 'male' else "D/O"
    pronoun_him_her = "him" if gender == "male" else "her"
    pronoun_his_her = "his" if gender == "male" else "her"

    # Replacement data for the document
    context = {
        "salutation": salutation,
        "name": name,
        "relation": relation,
        "father_name": fathers_name,
        "prn": prn,
        "years": str(years),
        "course": course,
        "batch": batch,
        "course_end": str(course_end),
        "pronoun_him_her": pronoun_him_her,
        "pronoun_his_her": pronoun_his_her,
    }

    # Render the document
    template.render(context)

    # Save the generated document
    output_path = os.path.join(output_dir, f"{name}_{prn}_Bonafide.docx")
    template.save(output_path)

    return output_path
