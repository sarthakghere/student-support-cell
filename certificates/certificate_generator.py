from docxtpl import DocxTemplate
import os
from django.conf import settings

def generate_transfer_certificate(student_data, backlogs):
    template_path = os.path.join(settings.MEDIA_ROOT, 'document_templates/TC_Template.docx')
    output_dir = os.path.join(settings.MEDIA_ROOT, 'generated_documents')
    os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists

    template = DocxTemplate(template_path)

    # Extract details from student_data
    name = student_data.get("name")
    prn = student_data.get("prn")
    gender = student_data.get("gender").lower()
    fathers_name = student_data.get("fathers_name")
    course = student_data.get("course").upper()
    course_start = int(student_data.get("course_start"))
    course_end = int(student_data.get("course_end"))

    batch = f"{course_start} - {course_end}"
    years = course_end - course_start
    salutation = "Mr." if gender == 'male' else "Ms."
    relation = "S/O" if gender == 'male' else "D/O"
    pronoun_him_her = "him" if gender == "male" else "her"
    pronoun_his_her = "his" if gender == "male" else "her"

    # Prepare backlog data
    backlog_details = []
    if backlogs:
        for subject, backlog_semester, passing_semester in backlogs:
            backlog_details.append({
                'subject': subject,
                'backlog_semester': backlog_semester,
                'passing_semester': passing_semester
            })
        semester_description = f"6th" if years == 3 else f"8th" if years == 4 else ""
    else:
        semester_description = ""

    # Replacement data
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
        "semester_description": f"The details of his backlog papers up to {semester_description} semester are as follows:" if backlogs else "",
    }

    # Render the document
    template.render(context)

    # Save the generated document
    output_path = os.path.join(output_dir, f"{name}_{prn}_TC.docx")
    template.save(output_path)

    return output_path