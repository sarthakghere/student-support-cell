from docxtpl import DocxTemplate
import os
from django.conf import settings
import inflect
import re
from students.models import Student

def to_pascal_case(text):
    words = re.split(r'[\s_-]+', text)  # Split by space, underscore, or hyphen
    return ''.join(word.capitalize() for word in words)

def generate_bonafide_certificate(student_data, backlogs: list):
    template_path = os.path.join(settings.MEDIA_ROOT, 'document_templates/Bonafide_Template.docx')
    output_dir = os.path.join(settings.MEDIA_ROOT, 'generated_documents')
    os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists

    template = DocxTemplate(template_path)

    # Extract details from student_data
    prn = student_data.get("PRN")
    full_name = student_data.get("full_name")
    gender = student_data.get("gender")
    fathers_name = student_data.get("fathers_name")
    course = student_data.get("course").upper()
    course_start = int(student_data.get("course_start"))
    course_end = int(student_data.get("course_end"))

    name = f"{full_name}"
    batch = f"{course_start} - {course_end}"
    years = course_end - course_start
    p = inflect.engine()
    years = to_pascal_case(p.number_to_words(years))
    salutation = "Mr." if gender == Student.GenderChoices.MALE else "Ms."
    relation = "S/O" if gender == Student.GenderChoices.MALE else "D/O"
    pronoun_him_her = "him" if gender == Student.GenderChoices.MALE else "her"
    pronoun_his_her = "his" if gender == Student.GenderChoices.MALE else "her"

    # Prepare backlog data
    backlog_details = []

    for x in range(len(backlogs)):
        backlog_details.append({
            'no': f"{x + 1}",
            'subject': backlogs[x].get('subject_name'),
            'backlog_semester': f"{backlogs[x].get('declared_fail')}",
            'passing_semester': f"{backlogs[x].get('declared_pass')}",
        })
        semester_description = f"6th" if years == 3 else f"8th" if years == 4 else ""
    else:
        semester_description = ""

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
        "backlog_details": backlog_details,
        "semester_description": f"The details of {pronoun_his_her} backlog papers up to {semester_description} semester are as follows:" if backlogs else "",
    }

    # Render the document
    template.render(context)

    # Save the generated document
    output_path = os.path.join(output_dir, f"{name}_{prn}_Bonafide.docx")
    template.save(output_path)

    return output_path
