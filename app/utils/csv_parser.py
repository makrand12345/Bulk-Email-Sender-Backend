import csv
import io

def parse_recipient_csv(file_content: bytes):
    """Parses CSV with headers: email, user_type"""
    decoded_file = file_content.decode('utf-8')
    io_string = io.StringIO(decoded_file)
    reader = csv.DictReader(io_string)
    
    recipients = []
    for row in reader:
        if "email" in row and "user_type" in row:
            recipients.append({
                "email": row["email"].strip(),
                "user_type": row["user_type"].strip()
            })
    return recipients