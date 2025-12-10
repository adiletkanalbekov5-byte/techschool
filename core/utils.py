# core/utils.py
import uuid
from .models import Certificate

def issue_certificate_for_enrollment(enrollment):
    number = str(uuid.uuid4()).replace('-', '')[:12].upper()
    cert = Certificate.objects.create(enrollment=enrollment, cert_number=number)
    return cert
