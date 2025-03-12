import gspread
import os
from celery import shared_task
from google.oauth2 import service_account
from .models import StudentApplication
from students.models import Student

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
    if len(data) <= 1:  # Only headers (1 row) or empty sheet (0 rows)
        print("No new data to fetch - only headers or empty sheet.")
        return "No new data to fetch."

    for entry in data:
        prn = entry.get('PRN')
        student = Student.objects.filter(prn=prn).exists()
        StudentApplication.objects.create(
            prn=prn,
            erp=entry.get('ERP ID'),
            first_name=entry.get('First Name'),
            last_name=entry.get('Last Name'),
            subject=entry.get('Subject'),
            message=entry.get('Description'),
            student = Student.objects.get(prn=prn) if student else None
        )

    # Clear Google Sheet after successfully saving data
    sheet.delete_rows(2, len(data) + 1)

    return "Data fetched and saved successfully."
