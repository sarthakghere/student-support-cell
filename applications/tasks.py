import gspread
import os
from celery import shared_task
from google.oauth2 import service_account
from .models import StudentApplication
from students.models import Student, Certificate

@shared_task
def fetch_google_forms_data():
    print("Fetching data from Google Sheet...")
    SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
    SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
    SHEET_NAME = os.getenv('SHEET_NAME')
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,  # Load credentials
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )

    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

    data = sheet.get_all_records()
    
    for entry in data:
        print(entry)
        prn = entry.get('PRN')
        student = Student.objects.filter(prn=prn).exists()
        application_type = entry.get('Application Type')
        if application_type == StudentApplication.ApplicationTypesChoices.GENERAL:
            StudentApplication.objects.create(
                prn=entry.get('PRN'),
                erp=entry.get('ERP ID'),
                first_name= Student.objects.get(prn=prn).user.first_name if student else entry.get('First Name'),
                last_name= Student.objects.get(prn=prn).user.last_name if student else entry.get('Last Name'),
                email= Student.objects.get(prn=prn).user.email if student else entry.get('Email Address'),
                application_type=application_type,
                subject=entry.get('Subject'),
                message=entry.get('Description'),
                student = Student.objects.get(prn=prn) if student else None
            )
        elif application_type == StudentApplication.ApplicationTypesChoices.CERTIFICATE_ISSUE_REQUEST:
            certificate_type_map = {label: code for code, label in Certificate.CertificateTypes.choices}
            certificate_type = certificate_type_map.get(entry.get('Certificate Type'))
            StudentApplication.objects.create(
                prn=entry.get('PRN'),
                erp=entry.get('ERP ID'),
                first_name= Student.objects.get(prn=prn).user.first_name if student else entry.get('First Name'),
                last_name= Student.objects.get(prn=prn).user.last_name if student else entry.get('Last Name'),
                email= Student.objects.get(prn=prn).user.email if student else entry.get('Email Address'),
                application_type=application_type,
                certificate_type=certificate_type,
                student = Student.objects.get(prn=prn) if student else None
            )
            

    # Clear Google Sheet after successfully saving data
    sheet.delete_rows(2, len(data) + 1)

    return "Data fetched and saved successfully."
